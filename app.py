from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import time

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# ============================================================
# Latest T-Box data
# ============================================================

latest_data = {
    "tboxId": "",
    "data": {},
    "gps": {},
    "received_time": 0
}


# ============================================================
# Dashboard
# ============================================================

@app.get("/")
async def dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "data": latest_data
        }
    )


# ============================================================
# Receive data from EC600
# ============================================================

@app.post("/api/data")
async def receive_data(request: Request):

    global latest_data

    try:

        body = await request.json()

        print("====================================")
        print("NEW EC600 DATA RECEIVED")
        print("====================================")
        print(body)

        # ----------------------------------------------------
        # ACTUAL format sent by the EC600 firmware:
        #
        # {
        #     "sv": "3.0",
        #     "Battery1": {...},
        #     "Battery2": {...},
        #     "IMEI": "...",
        #     "tboxId": "...",
        #     "server_time": 1759518796,
        #     "gps": {...}        <- optional, not sent yet
        # }
        #
        # Everything is flat (no nested "data" key), so we
        # store the whole body as "data" and just pull
        # tboxId/gps back out for convenience.
        # ----------------------------------------------------

        latest_data = {
            "tboxId": body.get("tboxId", ""),
            "data": body,
            "gps": body.get("gps", {}),
            "received_time": time.time()
        }

        return {
            "status": "ok",
            "message": "Data received successfully"
        }

    except Exception as e:

        print("ERROR receiving data:")
        print(str(e))

        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": str(e)
            }
        )


# ============================================================
# API - Get latest data
# ============================================================

@app.get("/api/data")
async def get_data():

    return latest_data


# ============================================================
# Health check
# ============================================================

@app.get("/health")
async def health():

    return {
        "status": "online"
    }
