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
    hf_model_id = os.getenv("HF_MODEL_ID")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    video_generation_provider = os.getenv("VIDEO_GENERATION_PROVIDER", "HUGGING_FACE").upper()

    if video_generation_provider == "HUGGING_FACE":
        if not api_token:
            raise RuntimeError("HF_API_TOKEN is not set for Hugging Face provider.")
        if not hf_model_id:
            raise RuntimeError("HF_MODEL_ID is not set for Hugging Face provider.")
    elif video_generation_provider == "OPENAI":
        if not openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is not set for OpenAI provider.")
    else:
        raise RuntimeError(f"Unknown VIDEO_GENERATION_PROVIDER: {video_generation_provider}. Must be HUGGING_FACE or OPENAI.")

    return api_token, hf_model_id, openai_api_key, video_generation_provider


async def _generate_with_hugging_face_api(image: UploadFile, prompt: str, api_token: str, model_id: str):
    """
    Call the Hugging Face Inference API for an image-to-video / avatar model.
    """
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
        return JSONResponse(content=response.json())

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


async def _generate_with_openai_api(image: UploadFile, prompt: str, openai_api_key: str):
    """
    Placeholder for calling the OpenAI video generation API.
    """
    # TODO: Implement actual OpenAI video generation logic here.
    # This will involve using the OpenAI Python client library.
    # Example (conceptual):
    # from openai import AsyncOpenAI
    # client = AsyncOpenAI(api_key=openai_api_key)
    # response = await client.video.generate(image=image_bytes, prompt=prompt, ...)
    # Handle response to save video or return URL.
    raise NotImplementedError("OpenAI video generation not yet implemented.")


@app.post("/generate")
async def generate(
    image: UploadFile = File(...),
    prompt: str = Form(...),
):
    api_token, hf_model_id, openai_api_key, video_generation_provider = load_config()

    if video_generation_provider == "HUGGING_FACE":
        return await _generate_with_hugging_face_api(image, prompt, api_token, hf_model_id)
    elif video_generation_provider == "OPENAI":
        return await _generate_with_openai_api(image, prompt, openai_api_key)


