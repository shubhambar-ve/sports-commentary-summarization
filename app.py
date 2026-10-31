from pathlib import Path
from typing import Literal
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from core import summarize

ROOT = Path(__file__).parent
app = FastAPI(title='Sports Commentary Summarization', version='1.0.0')
app.mount('/static', StaticFiles(directory=ROOT/'static'), name='static')
class Request(BaseModel):
    text: str = Field(min_length=1, max_length=12000)
    engine: Literal['extractive','flan-t5'] = 'flan-t5'
    count: int = Field(default=3, ge=1, le=6)
    max_new_tokens: int = Field(default=80, ge=20, le=160)
    beams: int = Field(default=4, ge=1, le=4)
@app.get('/')
def home(): return FileResponse(ROOT/'static/index.html')
@app.get('/health')
def health(): return {'status':'ok', 'note':'Liveness only; model loads on first LLM request.'}
@app.get('/samples')
def samples():
    import json
    return json.loads((ROOT/'data/samples.json').read_text())
@app.post('/summarize')
def endpoint(req: Request):
    try: return summarize(**req.model_dump())
    except ValueError as e: raise HTTPException(422, str(e)) from e
    except Exception as e:
        import logging
        logging.exception('Model request failed')
        raise HTTPException(503, 'Model unavailable. Check server logs, dependencies and Hugging Face connectivity. Offline baseline remains available.') from e
