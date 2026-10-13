from pathlib import Path
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
UPLOADS = DATA / "uploads"
UPLOADS.mkdir(exist_ok=True)
POLICY = DATA / "sample_company_policy.txt"

def chunks(text, size=650, overlap=90):
    text = re.sub(r"\\s+", " ", text).strip()
    out, start = [], 0
    while start < len(text):
        end = min(len(text), start + size)
        if end < len(text):
            boundary = text.rfind(" ", start, end)
            if boundary > start + size * .55: end = boundary
        if text[start:end].strip(): out.append(text[start:end].strip())
        if end >= len(text): break
        start = max(start + 1, end - overlap)
    return out

class KB:
    def __init__(self):
        self.items = []
        if not POLICY.exists():
            POLICY.write_text("Returns: request a return within 30 days if unused and in original packaging. Approved refunds normally take 5 to 10 business days. Shipping: standard delivery usually takes 3 to 7 business days after dispatch. Support hours: Monday to Friday, 9 AM to 5 PM local time, excluding public holidays. Order changes: cancellation is only possible before dispatch. Security: never share passwords or OTPs. If policy information is missing, contact a human support representative.", encoding="utf-8")
        self.add_text(POLICY.read_text(encoding="utf-8"), POLICY.name)
    def add_text(self, text, source):
        self.items.extend({"text": c, "source": source} for c in chunks(text))
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2))
        self.matrix = self.vectorizer.fit_transform([x["text"] for x in self.items])
    def add_file(self, path, source):
        if path.suffix.lower() == ".pdf":
            text = "\n".join(p.extract_text() or "" for p in PdfReader(str(path)).pages)
        else: text = path.read_text(encoding="utf-8", errors="ignore")
        if not text.strip(): raise ValueError("No readable text")
        before = len(self.items); self.add_text(text, source); return len(self.items)-before
    def retrieve(self, query, k=3):
        scores = cosine_similarity(self.vectorizer.transform([query]), self.matrix).ravel()
        result = []
        for i in scores.argsort()[::-1][:k]:
            if scores[i] > .03: result.append({**self.items[int(i)], "score": float(scores[i])})
        return result
kb = KB()
