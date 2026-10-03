from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates")

latest_data = {
    "tboxId": None,
    "data": {}
}


@app.get("/")
async def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "data": latest_data
        }
    )


@app.post("/api/data")
async def receive_data(request: Request):

    global latest_data

    try:
        body = await request.json()

        latest_data = body

        print("Received T-Box data:")
        print(body)

        return {
            "status": "ok"
        }

    except Exception as e:

        print("ERROR:", e)

        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": str(e)
            }
        )


@app.get("/api/data")
async def get_data():
    return latest_data
