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
    model_id = os.getenv("HF_MODEL_ID")

    if not api_token:
        raise RuntimeError("HF_API_TOKEN is not set. Create a .env file or set env vars.")
    if not model_id:
        raise RuntimeError("HF_MODEL_ID is not set. Create a .env file or set env vars.")

    return api_token, model_id


def generate_video_from_image(image_path: Path, prompt: str, output_path: Path):
    """
    Call the Hugging Face Inference API for an image-to-video / avatar model.
    This is provider-agnostic; adjust payload according to the chosen model docs.
    """
    api_token, model_id = load_config()

    api_url = f"https://api-inference.huggingface.co/models/{model_id}"

    with image_path.open("rb") as f:
        image_bytes = f.read()

    # Many HF image/video models accept raw binary or base64 in the payload.
    # Here we send binary image plus a JSON header for prompt; you may need to
    # adjust based on the specific model's README.
    headers = {
        "Authorization": f"Bearer {api_token}",
    }

    # Example for binary image + JSON options query string
    params = {
        "prompt": prompt,
    }

    response = requests.post(api_url, headers=headers, params=params, data=image_bytes, timeout=600)
    if response.status_code != 200:
        raise RuntimeError(f"HF Inference API error {response.status_code}: {response.text}")

    # Some models return raw video bytes, others return JSON with a URL.
    content_type = response.headers.get("Content-Type", "")
    if "application/json" in content_type:
        data = response.json()
        # Look for a common field where video URL might be stored
        video_url = data.get("video", {}).get("url") or data.get("output", data)
        print("Model returned JSON response:")
        print(data)
        print("If a video URL is present above, download it manually or extend this script.")
        return

    # Assume binary video content (e.g. mp4/gif/webm)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as f:
        f.write(response.content)

    print(f"Saved generated video to: {output_path}")


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


