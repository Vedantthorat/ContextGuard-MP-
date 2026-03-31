from unittest import result

from fastapi import FastAPI, File, UploadFile, Query
import shutil
import os
from scanner import run_checkov
from ai_agent import get_ai_fix
from agents import run_agents

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"message": "CortexGuard Backend Running 🚀"}

@app.post("/scan/")
async def scan_file(
    file: UploadFile = File(...),
    severity: str = Query(None)
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)



    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = run_checkov(file_path)

    # ✅ Add AI explanation for each issue
    # ✅ Multi-agent processing
    for issue in result["issues"]:
        issue["agent_analysis"] = run_agents(issue)

    # ✅ Step 1: Apply severity filter (if provided)
    if severity:
        filtered = [
            issue for issue in result["issues"]
            if issue["severity"] == severity.upper()
        ]
        result["issues"] = filtered

    # ✅ Step 2: SORT issues by severity (ADD THIS BLOCK HERE)
    severity_order = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}

    result["issues"] = sorted(
        result["issues"],
        key=lambda x: severity_order.get(x["severity"], 0),
        reverse=True
    )

    # ✅ Step 3: Return final result
    return result
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = run_checkov(file_path)

    if severity:
        filtered = [
            issue for issue in result["issues"]
            if issue["severity"] == severity.upper()
        ]
        result["issues"] = filtered

    return result