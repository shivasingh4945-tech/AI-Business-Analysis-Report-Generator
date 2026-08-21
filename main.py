import io
import os

import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from report_generator import generate_report

load_dotenv()

app = FastAPI(title="AI Business Analysis Report Generator")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def _read_csv(raw: bytes) -> pd.DataFrame:
    return pd.read_csv(io.BytesIO(raw))


def _run_report(df: pd.DataFrame) -> str:
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY is not set. Copy .env.example to .env and add your key.")
    return generate_report(df, groq_api_key)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {"report": None, "error": None})


@app.post("/", response_class=HTMLResponse)
async def upload(request: Request, file: UploadFile = File(...)):
    report = None
    error = None

    if not file.filename or not file.filename.lower().endswith(".csv"):
        error = "File must be a CSV"
    else:
        raw = await file.read()
        try:
            df = _read_csv(raw)
        except Exception as e:
            error = f"Could not read the CSV file: {e}"
        else:
            try:
                report = _run_report(df)
            except Exception as e:
                error = str(e)

    return templates.TemplateResponse(request, "index.html", {"report": report, "error": error})


@app.post("/api/reports")
async def create_report(file: UploadFile = File(...)):
    """JSON API: upload a CSV, get the generated report back as JSON."""
    if not file.filename or not file.filename.lower().endswith(".csv"):
        return JSONResponse(status_code=400, content={"error": "File must be a CSV"})

    raw = await file.read()
    try:
        df = _read_csv(raw)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": f"Could not read the CSV file: {e}"})

    try:
        report = _run_report(df)
    except ValueError as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
    except Exception as e:
        return JSONResponse(status_code=502, content={"error": str(e)})

    return {"report": report}


@app.get("/health")
async def health():
    return {"status": "ok"}
