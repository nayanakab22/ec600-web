import json
import os
import uuid
from datetime import datetime, timezone

from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

DEVICE_KEY = os.environ.get("DEVICE_KEY", "change-me-device-key")   # same as firmware
API_KEY = os.environ.get("API_KEY", "")                              # for dashboard commands

app = FastAPI(title="EC600 T-Box Server")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

devices = {}        # tboxId -> latest telemetry
pending_cmds = {}   # tboxId -> {"operation", "rid"}
cmd_results = {}    # rid -> result from device

ALLOWED_OPS = {
    "remote_lock_charge", "remote_unlock_charge",
    "remote_lock_nocharge", "remote_unlock_nocharge",
    "data_flush", "reboot",
}


def check_device(key: str):
    if key != DEVICE_KEY:
        raise HTTPException(401, "Bad device key")


def check_admin(key: str):
    if not API_KEY or key != API_KEY:
        raise HTTPException(401, "Unauthorized")


# ---------------- dashboard ----------------
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/api/devices")
async def get_devices():
    return devices


@app.get("/api/device/{tbox_id}")
async def get_device(tbox_id: str):
    if tbox_id not in devices:
        raise HTTPException(404, "Device not found")
    return devices[tbox_id]


# ---------------- device -> server ----------------
@app.post("/api/telemetry")
async def receive_telemetry(request: Request, x_device_key: str = Header(default="")):
    check_device(x_device_key)
    data = await request.json()
    tbox_id = data.get("tboxId")
    if not tbox_id:
        raise HTTPException(400, "tboxId is required")
    data["_server_time"] = datetime.now(timezone.utc).isoformat()
    devices[tbox_id] = data
    return {"status": "ok", "tboxId": tbox_id}


@app.get("/api/device/{tbox_id}/command")
async def device_poll(tbox_id: str, x_device_key: str = Header(default="")):
    """Device polls here. Returns one pending command (then clears it), or {}."""
    check_device(x_device_key)
    return pending_cmds.pop(tbox_id, {})


@app.post("/api/device/{tbox_id}/command/result")
async def device_result(tbox_id: str, request: Request, x_device_key: str = Header(default="")):
    check_device(x_device_key)
    body = await request.json()
    cmd_results[body.get("rid")] = body
    return {"status": "ok"}


# ---------------- dashboard -> device ----------------
@app.post("/api/device/{tbox_id}/command")
async def queue_command(tbox_id: str, request: Request, x_api_key: str = Header(default="")):
    check_admin(x_api_key)
    op = (await request.json()).get("operation")
    if op not in ALLOWED_OPS:
        raise HTTPException(400, "Bad operation")
    rid = uuid.uuid4().hex[:8]
    pending_cmds[tbox_id] = {"operation": op, "rid": rid}
    return {"rid": rid, "queued": True}


@app.get("/api/response/{rid}")
async def get_response(rid: str):
    return cmd_results.get(rid, {"status": "pending"})
