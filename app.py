from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime, timezone
import json

app = FastAPI(title="EC600 T-Box Server")

# Static files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

# HTML templates
templates = Jinja2Templates(
    directory="templates"
)

# Store latest telemetry for each T-Box
devices = {}


# --------------------------------------------------
# Dashboard
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):

    return templates.TemplateResponse(
        request,
        "dashboard.html"
    )


# --------------------------------------------------
# Receive telemetry from EC600
# --------------------------------------------------

@app.post("/api/telemetry")
async def receive_telemetry(request: Request):

    try:

        # Read JSON sent by EC600
        data = await request.json()

        # Get T-Box ID
        tbox_id = data.get("tboxId")

        # Check T-Box ID
        if not tbox_id:

            return {
                "status": "error",
                "message": "tboxId is required"
            }

        # Add server receive time
        data["_server_time"] = datetime.now(
            timezone.utc
        ).isoformat()

        # Store latest data
        devices[tbox_id] = data

        # Print received data in Render logs
        print(
            "Telemetry received:",
            tbox_id
        )

        print(
            json.dumps(
                data,
                indent=2
            )
        )

        # Response to EC600
        return {
            "status": "ok",
            "tboxId": tbox_id
        }

    except Exception as e:

        print(
            "Telemetry error:",
            str(e)
        )

        return {
            "status": "error",
            "message": str(e)
        }


# --------------------------------------------------
# Get all T-Box data
# --------------------------------------------------

@app.get("/api/devices")
async def get_devices():

    return devices


# --------------------------------------------------
# Get one T-Box
# --------------------------------------------------

@app.get("/api/device/{tbox_id}")
async def get_device(tbox_id: str):

    if tbox_id not in devices:

        return {
            "status": "error",
            "message": "Device not found"
        }

    return devices[tbox_id]
