from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from subprocess import check_output
from predict_words import perform_ocr
from typing import Optional

app = FastAPI()

@app.get("/predict_sentnece/")
async def run_script() -> str:
    try:
        # Run the provided script using check_output
        return perform_ocr()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_root():
    return {"message": "Welcome! Use the /run_script/ endpoint to execute a script."}

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Image API")


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8010)
