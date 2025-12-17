## Lipsynk video generation via Hugging Face Inference API

This project demonstrates how to call a **Hugging Face–hosted image-to-video / avatar model**
from your own backend so users never see the underlying provider.

It provides:
- **CLI**: `main.py` to generate a video from an image + prompt.
- **HTTP API**: `api.py` (FastAPI) with a `/generate` endpoint.

All calls go to the Hugging Face **Inference API** (remote GPU, no local model download).

### 1. Setup

```bash
cd lipsynk
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configuration

To configure the application, you need to set up several environment variables. You can do this by creating a `.env` file in the project root (by copying `.env.example`) and filling in the details, or by exporting them directly in your shell.

Here are the required variables:

-   **`HF_API_TOKEN`**: Your Hugging Face API token.
    -   **How to obtain**: Create a Hugging Face account and generate a token with 'read' access from your [Hugging Face profile settings](https://huggingface.co/settings/tokens).
-   **`HF_MODEL_ID`**: The ID of the Hugging Face model you wish to use.
    -   **How to obtain**: Browse the [Hugging Face Hub](https://huggingface.co/models) for image-to-video or avatar models (e.g., `emilianob/emilianobot-facer-2.0`). The model ID is typically `author/model-name`.
-   **`OPENAI_API_KEY`**: Your OpenAI API key.
    -   **How to obtain**: Obtain your API key from your [OpenAI dashboard](https://platform.openai.com/account/api-keys).
-   **`VIDEO_GENERATION_PROVIDER`**: Specifies which provider to use for video generation.
    -   **Values**: `HUGGING_FACE` or `OPENAI`.

Example `.env` configuration:

```bash
# Required for Hugging Face video generation
HF_API_TOKEN=your_hf_api_token_here
HF_MODEL_ID=your-model-id-here   # e.g. author/model-name

# Required for OpenAI video generation
OPENAI_API_KEY=your_openai_api_key_here

# Choose your video generation provider: HUGGING_FACE or OPENAI
VIDEO_GENERATION_PROVIDER=HUGGING_FACE
```


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
cd lipsynk
git init
git add .
git commit -m "Initial lipsynk HF Inference project"
```

Create a new repo on GitHub (via the website), then connect and push:

```bash
git remote add origin https://github.com/your-username/your-repo-name.git
git branch -M main
git push -u origin main
```

From this point on, you can integrate `api.py` into your backend and keep users fully abstracted
from the underlying HF/LLM provider.

**Note**: If you had previously set up a virtual environment with the old project name, please re-create it by deleting the `.venv` folder and following the setup instructions again to ensure all paths are updated correctly.


