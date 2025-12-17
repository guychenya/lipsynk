import os
from pathlib import Path

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from dotenv import load_dotenv
import requests


app = FastAPI(title="Avatar Video API", version="0.1.0")


def load_config():
    load_dotenv()
    api_token = os.getenv("HF_API_TOKEN")
    model_id = os.getenv("HF_MODEL_ID")
    if not api_token or not model_id:
        raise RuntimeError("HF_API_TOKEN and HF_MODEL_ID must be set (see .env.example).")
    return api_token, model_id


@app.post("/generate")
async def generate(
    image: UploadFile = File(...),
    prompt: str = Form(...),
):
    """
    HTTP endpoint to generate a video from an uploaded image + text prompt.
    Returns either a video file or JSON, depending on the model's response.
    """
    api_token, model_id = load_config()
    api_url = f"https://api-inference.huggingface.co/models/{model_id}"

    image_bytes = await image.read()

    headers = {
        "Authorization": f"Bearer {api_token}",
    }
    params = {"prompt": prompt}

    try:
        response = requests.post(api_url, headers=headers, params=params, data=image_bytes, timeout=600)
    except Exception as exc:
        return JSONResponse(status_code=500, content={"error": f"Request to HF failed: {exc}"})

    if response.status_code != 200:
        return JSONResponse(status_code=response.status_code, content={"error": response.text})

    content_type = response.headers.get("Content-Type", "")
    if "application/json" in content_type:
        # Pass-through JSON so caller can inspect URLs or metadata.
        return JSONResponse(content=response.json())

    # Binary video: save to a temp file and return
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True, parents=True)
    output_path = output_dir / "api_generated_video.mp4"
    with output_path.open("wb") as f:
        f.write(response.content)

    return FileResponse(
        output_path,
        media_type=content_type or "video/mp4",
        filename="generated_video.mp4",
    )


