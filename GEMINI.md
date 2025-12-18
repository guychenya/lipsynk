# Project Overview: Lipsynk Video Generation

This project provides a CLI tool and an HTTP API for generating avatar videos using a Hugging Face Inference API model. It acts as a backend proxy, abstracting the underlying Hugging Face API from the end-user or frontend application. The project supports both CLI and HTTP API methods for triggering video generation from an image and a text prompt.

**Key Technologies:**
*   **Python:** Core language.
*   **FastAPI:** For building the HTTP API.
*   **Requests:** For making HTTP requests to the Hugging Face Inference API.
*   **python-dotenv:** For managing environment variables (`.env`).

## Building and Running

### 1. Setup

Clone the repository and set up the Python virtual environment:

```bash
git clone <repository-url>
cd lipsynk
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the project root by copying `.env.example` and fill in your Hugging Face API token and the model ID:

```ini
HF_API_TOKEN=your_hf_api_token_here
HF_MODEL_ID=your-model-id-here   # e.g. author/model-name
```

### 3. CLI Usage

To generate a video using the command-line interface:

```bash
source .venv/bin/activate
python main.py \
  --image path/to/avatar.png \
  --prompt "A person introducing our product in a friendly way" \
  --output output/video.mp4
```

The output will either be a saved video file or a JSON response containing a URL to the generated video, depending on the Hugging Face model's behavior.

### 4. HTTP API Usage

To run the HTTP API locally:

```bash
source .venv/bin/activate
uvicorn api:app --reload --port 8000
```

Then, you can call the `/generate` endpoint with `curl` or any HTTP client:

```bash
curl -X POST http://localhost:8000/generate \
  -F "prompt=Short welcome message" \
  -F "image=@path/to/avatar.png" \
  --output generated_video.mp4
```

The API will return either the generated video file directly or a JSON response with a video URL.

## Development Conventions

*   **Environment Variables:** Configuration is handled via `.env` files and `python-dotenv`.
*   **API Interaction:** The Hugging Face Inference API is accessed using the `requests` library.
*   **Error Handling:** Basic error handling is implemented for API calls and file operations.
*   **Output:** The system handles two types of responses from the Hugging Face API: direct binary video content and JSON containing a video URL.

**Note**: If you had previously set up a virtual environment with the old project name, please re-create it by deleting the `.venv` folder and following the setup instructions again to ensure all paths are updated correctly.

---

## Archival Note

This project has been archived as it does not currently support the user's expected functionality. This note serves as a checkpoint for future reference.