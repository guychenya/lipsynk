import argparse
import base64
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


def load_config():
    """
    Load environment variables from .env if present.
    Required:
      - HF_API_TOKEN: your Hugging Face API token
      - HF_MODEL_ID: image-to-video or avatar model id on Hugging Face
    """
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


def _generate_with_hugging_face(image_path: Path, prompt: str, output_path: Path, api_token: str, model_id: str):
    """
    Call the Hugging Face Inference API for an image-to-video / avatar model.
    """
    api_url = f"https://api-inference.huggingface.co/models/{model_id}"

    with image_path.open("rb") as f:
        image_bytes = f.read()

    headers = {
        "Authorization": f"Bearer {api_token}",
    }

    params = {
        "prompt": prompt,
    }

    response = requests.post(api_url, headers=headers, params=params, data=image_bytes, timeout=600)
    if response.status_code != 200:
        raise RuntimeError(f"HF Inference API error {response.status_code}: {response.text}")

    content_type = response.headers.get("Content-Type", "")
    if "application/json" in content_type:
        data = response.json()
        video_url = data.get("video", {}).get("url") or data.get("output", data)
        print("Model returned JSON response:")
        print(data)
        print("If a video URL is present above, download it manually or extend this script.")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as f:
        f.write(response.content)

    print(f"Saved generated video to: {output_path}")


def _generate_with_openai(image_path: Path, prompt: str, output_path: Path, openai_api_key: str):
    """
    Placeholder for calling the OpenAI video generation API.
    """
    # TODO: Implement actual OpenAI video generation logic here.
    # This will involve using the OpenAI Python client library.
    # Example (conceptual):
    # from openai import OpenAI
    # client = OpenAI(api_key=openai_api_key)
    # response = client.video.generate(image=image_path, prompt=prompt, ...)
    # Handle response to save video to output_path.
    raise NotImplementedError("OpenAI video generation not yet implemented.")


def generate_avatar_video(image_path: Path, prompt: str, output_path: Path):
    """
    Call the appropriate video generation API based on the configured provider.
    """
    api_token, hf_model_id, openai_api_key, video_generation_provider = load_config()

    if video_generation_provider == "HUGGING_FACE":
        _generate_with_hugging_face(image_path, prompt, output_path, api_token, hf_model_id)
    elif video_generation_provider == "OPENAI":
        _generate_with_openai(image_path, prompt, output_path, openai_api_key)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate avatar/video from an image using a Hugging Face Inference API model."
    )
    parser.add_argument(
        "--image",
        required=True,
        help="Path to the avatar image file (e.g. PNG/JPEG).",
    )
    parser.add_argument(
        "--prompt",
        required=True,
        help="Text prompt / description to drive the video generation.",
    )
    parser.add_argument(
        "--output",
        default="output/video.mp4",
        help="Where to save the generated video (if the model returns binary).",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    image_path = Path(args.image)
    output_path = Path(args.output)

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    generate_video_from_image(image_path=image_path, prompt=args.prompt, output_path=output_path)


if __name__ == "__main__":
    main()


