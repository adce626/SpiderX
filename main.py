from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os
from pydantic import BaseModel
from typing import List, Optional
import asyncio

from spiderx.core import SpiderXCore
from spiderx.models import ScanRequest, ScanResult

app = FastAPI(title="SpiderX", description="Advanced URL Parameter Mining Tool", version="1.0.0")

# Setup static files and templates
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize SpiderX core
spider_core = SpiderXCore()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main SpiderX interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/scan")
async def scan_domains(scan_request: ScanRequest) -> ScanResult:
    """Start URL parameter scanning for domains"""
    try:
        result = await spider_core.scan_domains(scan_request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/scan/{scan_id}/status")
async def get_scan_status(scan_id: str):
    """Get the status of a running scan"""
    try:
        status = spider_core.get_scan_status(scan_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=404, detail="Scan not found")

@app.get("/api/scan/{scan_id}/results")
async def get_scan_results(scan_id: str):
    """Get the results of a completed scan"""
    try:
        results = spider_core.get_scan_results(scan_id)
        return results
    except Exception as e:
        raise HTTPException(status_code=404, detail="Results not found")

@app.get("/api/scan/{scan_id}/download/{format}")
async def download_results(scan_id: str, format: str):
    """Download scan results in specified format (json, txt, csv)"""
    try:
        content, media_type, filename = spider_core.export_results(scan_id, format)
        from fastapi.responses import Response
        return Response(
            content=content,
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail="Results not found")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)