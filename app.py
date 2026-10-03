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
        # Expected format:
        #
        # {
        #     "tboxId": "...",
        #     "data": {
        #         "sv": "3.0",
        #         "Battery1": {...},
        #         "Battery2": {...}
        #     },
        #     "gps": {...}
        # }
        # ----------------------------------------------------

        latest_data = {
            "tboxId": body.get("tboxId", ""),
            "data": body.get("data", {}),
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
