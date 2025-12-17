## Avatar video generation via Hugging Face Inference API

This project demonstrates how to call a **Hugging Face–hosted image-to-video / avatar model**
from your own backend so users never see the underlying provider.

It provides:
- **CLI**: `main.py` to generate a video from an image + prompt.
- **HTTP API**: `api.py` (FastAPI) with a `/generate` endpoint.

All calls go to the Hugging Face **Inference API** (remote GPU, no local model download).

### 1. Setup

```bash
cd hf-avatar-video
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configuration

1. Create an account on Hugging Face and generate an **API token** with Inference scope.
2. Pick a suitable **image-to-video / avatar** model that offers Inference API access
   (for example, a talking-head or image-to-video model from the Hub).
3. If using OpenAI, obtain an **API key** from your OpenAI account.
4. Copy `.env.example` to `.env` and set the following variables:

```bash
# Required for Hugging Face video generation
HF_API_TOKEN=your_hf_api_token_here
HF_MODEL_ID=your-model-id-here   # e.g. author/model-name

# Required for OpenAI video generation
OPENAI_API_KEY=your_openai_api_key_here

# Choose your video generation provider: HUGGING_FACE or OPENAI
VIDEO_GENERATION_PROVIDER=HUGGING_FACE
```

You can also export them directly in your shell instead of using `.env`.

### 3. CLI usage

```bash
source .venv/bin/activate
python main.py \
  --image path/to/avatar.png \
  --prompt "A person introducing our product in a friendly way" \
  --output output/video.mp4
```

Depending on the model, the script will either:
- Save a binary video file to `output/video.mp4`, or
- Print JSON with a URL to the generated video (you can then extend the script to download it).

### 4. HTTP API

Run the API locally:

```bash
source .venv/bin/activate
uvicorn api:app --reload --port 8000
```

Call it from your app (example with `curl`):

```bash
curl -X POST http://localhost:8000/generate \
  -F "prompt=Short welcome message" \
  -F "image=@path/to/avatar.png" \
  --output generated_video.mp4
```

Your frontend should call **your** `/generate` endpoint, not Hugging Face directly.

### 5. Git & GitHub

Initialize git and make the first commit:

```bash
cd hf-avatar-video
git init
git add .
git commit -m "Initial avatar video HF Inference project"
```

Create a new repo on GitHub (via the website), then connect and push:

```bash
git remote add origin https://github.com/your-username/your-repo-name.git
git branch -M main
git push -u origin main
```

From this point on, you can integrate `api.py` into your backend and keep users fully abstracted
from the underlying HF/LLM provider.


