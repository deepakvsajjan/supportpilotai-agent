from pathlib import Path
from uuid import uuid4
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.schemas import ChatRequest, FeedbackRequest
from app.knowledge import kb, UPLOADS
from app.llm import answer
from app import storage

ROOT = Path(__file__).resolve().parent.parent
app = FastAPI(title="SupportPilot AI", description="Customer support RAG portfolio project")
app.mount("/static", StaticFiles(directory=ROOT/"static"), name="static")
@app.on_event("startup")
def startup(): storage.init()
@app.get("/", response_class=HTMLResponse)
def home(): return (ROOT/"static"/"index.html").read_text(encoding="utf-8")
@app.get("/health")
def health():
    from app.config import OPENAI_API_KEY
    return {"status":"ok", "llm_configured":bool(OPENAI_API_KEY)}
@app.post("/chat")
def chat(req: ChatRequest):
    q=req.message.strip()
    if not q: raise HTTPException(422, "Message cannot be blank")
    sid=req.session_id or str(uuid4())
    found=kb.retrieve(q)
    text,mode=answer(q,found)
    sources=list(dict.fromkeys(x["source"] for x in found))
    storage.save(sid,"user",q); storage.save(sid,"assistant",text,sources)
    return {"answer":text,"sources":sources,"session_id":sid,"mode":mode}
@app.get("/history/{session_id}")
def get_history(session_id: str): return {"session_id":session_id,"messages":storage.history(session_id)}
@app.post("/feedback")
def feedback(req: FeedbackRequest):
    with storage.connect() as c:
        from datetime import datetime, timezone
        c.execute("INSERT INTO feedback(session_id,message,rating,comment,created_at) VALUES(?,?,?,?,?)",(req.session_id,req.message,req.rating,req.comment,datetime.now(timezone.utc).isoformat()))
    return {"status":"saved"}
@app.post("/documents")
async def upload(file: UploadFile = File(...)):
    suffix=Path(file.filename or "").suffix.lower()
    if suffix not in {".txt",".md",".pdf"}: raise HTTPException(400,"Only TXT, MD and PDF files are supported")
    data=await file.read()
    if len(data)>5*1024*1024: raise HTTPException(413,"Maximum upload size is 5 MB")
    path=UPLOADS/(uuid4().hex+suffix); path.write_bytes(data)
    try: count=kb.add_file(path,Path(file.filename or path.name).name)
    except Exception as e:
        path.unlink(missing_ok=True); raise HTTPException(400,"Could not read document; use a text-based PDF, TXT, or MD file") from e
    return {"filename":file.filename,"chunks_added":count,"message":"Indexed in memory until the server restarts"}
