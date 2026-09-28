from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime, timezone
import json

app = FastAPI(title="EC600 T-Box Server")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

devices = {}


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )


@app.post("/api/telemetry")
async def receive_telemetry(request: Request):

    try:
        data = await request.json()

        tbox_id = data.get("tboxId")

        if not tbox_id:
            return {
                "status": "error",
                "message": "tboxId is required"
            }

        data["_server_time"] = datetime.now(
            timezone.utc
        ).isoformat()

        devices[tbox_id] = data

        print("Telemetry received:", tbox_id)
        print(json.dumps(data, indent=2))

        return {
            "status": "ok",
            "tboxId": tbox_id
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


@app.get("/api/devices")
async def get_devices():
    return devices


@app.get("/api/device/{tbox_id}")
async def get_device(tbox_id: str):

    if tbox_id not in devices:
        return {
            "status": "error",
            "message": "Device not found"
        }

    return devices[tbox_id]
