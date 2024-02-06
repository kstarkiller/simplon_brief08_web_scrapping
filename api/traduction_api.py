from fastapi import FastAPI, Query
from urllib.parse import quote
import uvicorn
import httpx

app = FastAPI()

@app.get("/translate/")
async def translate(text: str, source_lang: str = "auto", target_lang: str = "en"):
    encoded_text = quote(text)
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_lang}&tl={target_lang}&dt=t&q={encoded_text}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            translated_text = ''.join([i[0] for i in data[0]])
            return {"translated_text": translated_text}
        else:
            return {"error": "Failed to fetch translation"}
        
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)