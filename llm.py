from app.config import OPENAI_API_KEY, OPENAI_MODEL
def answer(question, retrieved):
    if not OPENAI_API_KEY:
        if not retrieved:
            return ("I couldn't find enough information in the knowledge base. Please contact a human support representative. This demo cannot access real orders or accounts.", "demo-retrieval")
        excerpts = "\n\n".join("• " + x["text"] for x in retrieved)
        return ("Demo mode (no LLM key configured): these are retrieved policy excerpts, not an LLM-generated answer.\n\n" + excerpts, "demo-retrieval")
    try:
        from openai import OpenAI
        context = "\n\n".join(f"Source: {x['source']}\n{x['text']}" for x in retrieved) or "No relevant context found."
        client = OpenAI(api_key=OPENAI_API_KEY)
        r = client.chat.completions.create(model=OPENAI_MODEL, temperature=.2, messages=[
          {"role":"system","content":"You are a careful customer support assistant. Answer only from the provided context. If it does not answer the question, say you do not know and recommend a human representative. Never invent order status or account details. Never ask for passwords, full card numbers, or OTPs.\n\nCONTEXT:\n"+context},
          {"role":"user","content":question}])
        return (r.choices[0].message.content or "I could not create an answer.", "openai")
    except Exception:
        return ("The LLM service could not be reached. Please try again later. Retrieved sources may still be available below.", "llm-error")
