WAVEMARK-CHATBOT-FRONTEND
=========================
A lightweight Streamlit frontend for the Wavemark chatbot (ERP support). This readme.txt documents what I found in the repository and provides exact, production-friendly instructions to run, configure, debug, and extend the frontend.

Repository snapshot (observed)
-----------------------------
- Main entry: Chat_ui.py — Streamlit app providing the chat UI and backend proxy.
- Top-level files: README.md (short project description), requirements.txt (Python deps).
- Language: Python (Streamlit frontend).

Purpose
-------
This project is a frontend that accepts user chat messages and forwards them to a chatbot backend (the backend service that performs knowledge retrieval / LLM inference is expected to be hosted separately). The UI is implemented in Streamlit (single-file entrypoint `Chat_ui.py`) and meant to be simple, session-scoped, and easy to deploy.

Quick start (developer)
-----------------------
1. Clone the repo:
   git clone https://github.com/dgunda-iu/wavemark-chatbot-frontend.git <https://nam12.safelinks.protection.outlook.com/?url=https%3A%2F%2Fgithub.com%2Fdgunda-iu%2Fwavemark-chatbot-frontend.git&data=05%7C02%7Cdgunda%40iuhealth.org%7Cc15a9a80c42749827c3d08ddfc49a89e%7Cd9d470633f5e4de9bf99f083657fa0fe%7C0%7C0%7C638944115620123069%7CUnknown%7CTWFpbGZsb3d8eyJFbXB0eU1hcGkiOnRydWUsIlYiOiIwLjAuMDAwMCIsIlAiOiJXaW4zMiIsIkFOIjoiTWFpbCIsIldUIjoyfQ%3D%3D%7C40000%7C%7C%7C&sdata=Y3myMjm75X2O01y1B13vzV%2BljAkD7IvOIWKEiPNOtGM%3D&reserved=0> 
   cd wavemark-chatbot-frontend

2. Create and activate a virtual environment (recommended):
   python -m venv .venv
   source .venv/bin/activate     # macOS / Linux
   .venv\Scripts\activate        # Windows

3. Install dependencies:
   pip install -r requirements.txt

4. Configure the backend URL:
   The frontend expects a backend chat API endpoint. Use an environment variable:
   Example:
     export CHATBOT_API_URL="https://your-backend.example.com/api/chat <https://nam12.safelinks.protection.outlook.com/?url=https%3A%2F%2Fyour-backend.example.com%2Fapi%2Fchat&data=05%7C02%7Cdgunda%40iuhealth.org%7Cc15a9a80c42749827c3d08ddfc49a89e%7Cd9d470633f5e4de9bf99f083657fa0fe%7C0%7C0%7C638944115620159588%7CUnknown%7CTWFpbGZsb3d8eyJFbXB0eU1hcGkiOnRydWUsIlYiOiIwLjAuMDAwMCIsIlAiOiJXaW4zMiIsIkFOIjoiTWFpbCIsIldUIjoyfQ%3D%3D%7C40000%7C%7C%7C&sdata=tGQffwJ9Qdzx%2F3TKGDIu4tV5Zt6GiYs4BSDfL%2Bp%2FyHg%3D&reserved=0> "
   (If the app uses a different config key, update accordingly in `Chat_ui.py`.)

5. Run the app locally:
   streamlit run Chat_ui.py
   - Default dev server: http://localhost:8501
   - Use `--server.port` to change the port if needed.

Configuration & environment
---------------------------
- CHATBOT_API_URL (recommended): URL of the backend chat endpoint that receives messages and returns bot responses.
- If your backend streams responses or supports websockets, ensure the frontend's networking logic (in `Chat_ui.py`) matches the backend contract.
- CORS: If the backend is hosted on a different origin, ensure CORS is configured server-side for the frontend host.

Expected behavior
-----------------
- Type user message in the input box, submit, and see bot replies in the conversation pane.
- Chat history is kept in memory per session (typical Streamlit behavior).
- Network errors or backend errors should display an inline error message — see `Chat_ui.py` for the specific error-handling logic.

Production deployment recommendations
------------------------------------
Docker (recommended for consistent deployments):
- Example Dockerfile:
  FROM python:3.10-slim
  WORKDIR /app
  COPY . /app
  RUN pip install --no-cache-dir -r requirements.txt
  EXPOSE 8501
  CMD ["streamlit", "run", "Chat_ui.py", "--server.port=8501", "--server.address=0.0.0.0"]

- Build & run:
  docker build -t wavemark-frontend .
  docker run -e CHATBOT_API_URL="https://..." -p 8501:8501 wavemark-frontend

Streamlit Cloud:
- Connect GitHub repository and deploy. Add CHATBOT_API_URL as a secret or app setting.

Heroku:
- Add a Procfile: `web: streamlit run Chat_ui.py --server.port=$PORT`
- Set config vars including CHATBOT_API_URL.

Security & Ops
--------------
- Do not hard-code API keys or sensitive URLs in the repo. Use environment variables or a secret manager.
- If adding authentication, adopt a standard scheme (JWT/OAuth) and forward tokens from the frontend to backend securely over HTTPS.
- Ensure the backend enforces rate limits and auth checks (frontend cannot and should not be treated as trusted).

Extending the UI
----------------
Suggested practical improvements:
- Add streaming response UI if backend supports SSE/websocket.
- Add file upload for document Q&A (if backend accepts files).
- Add authentication + multi-user session support.
- Persist conversation history (optional) using a small backend store (Redis/Postgres) if session persistence across reloads is required.
- Add automated tests and a simple CI job to run linting and unit tests.

Developer notes
---------------
- The codebase is small and single-file oriented (Chat_ui.py). Consider modularizing if the app grows:
  - `app/` package with `ui.py`, `client.py`, `config.py`
  - Tests in `tests/`
  - CI workflow to run `pytest` and `flake8`/`black` on PRs.

Troubleshooting
---------------
- If the app fails to start:
  - Ensure Streamlit is installed and Python version matches requirements.
  - Run `streamlit run Chat_ui.py` from the repository root.
- Backend connectivity issues:
  - Verify `CHATBOT_API_URL` and network accessibility.
  - Check backend logs and CORS configuration.

Contributing
------------
- Fork → branch → PR. Keep changes small and focused.
- Add a short description in commit messages and link to issue when relevant.
- Format Python code with `black` and lint with `flake8` before opening PRs.

License & credits
-----------------
- The repo does not declare an explicit license file (add one; MIT is a common default for projects like this).
- If you want, I can add a recommended `LICENSE` file text.

Contact / Next steps
--------------------
If you’d like, I can:
- Convert this into `README.md` with Markdown formatting and open a PR-style patch.
- Add a Dockerfile and GitHub Actions CI workflow.
- Inspect `Chat_ui.py` and propose a small refactor to separate networking and UI logic.
