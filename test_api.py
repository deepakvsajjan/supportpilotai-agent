from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health():
    r=client.get("/health"); assert r.status_code==200 and r.json()["status"]=="ok"
def test_chat():
    r=client.post("/chat",json={"message":"What is the refund policy?"})
    assert r.status_code==200
    d=r.json(); assert d["answer"] and d["session_id"]
    assert "sample_company_policy.txt" in d["sources"]
def test_blank_message_rejected():
    assert client.post("/chat",json={"message":""}).status_code==422
def test_feedback():
    r=client.post("/feedback",json={"session_id":"test","message":"Helpful answer","rating":5})
    assert r.status_code==200
