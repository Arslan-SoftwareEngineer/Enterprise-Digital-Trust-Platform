"""
Enterprise Digital Identity, Trust & Deepfake Detection Platform
Root Entrypoint for Cloud Deployments (Vercel, Render, Railway, etc.)
"""
import os
import sys
import traceback

_root = os.path.dirname(os.path.abspath(__file__))
if _root not in sys.path:
    sys.path.insert(0, _root)

_backend = os.path.join(_root, "backend")
if _backend not in sys.path:
    sys.path.insert(0, _backend)

try:
    from backend.app.main import app
    print("Application initialized successfully.")
except Exception as e:
    print("CRITICAL: Failed to import backend.app.main:", file=sys.stderr)
    traceback.print_exc()
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse

    app = FastAPI(title="Startup Error Handler")
    _err_msg = traceback.format_exc()

    @app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"])
    async def startup_error_fallback(full_path: str):
        return HTMLResponse(
            f"""<!DOCTYPE html>
            <html>
            <head><title>Startup Error</title></head>
            <body style="background:#0d1117;color:#c9d1d9;font-family:sans-serif;padding:30px;">
                <h1 style="color:#f85149;">Application Startup Failure</h1>
                <p>The FastAPI application failed during module initialization with the following exception:</p>
                <pre style="background:#161b22;padding:20px;border-radius:6px;color:#ff7b72;overflow:auto;">{_err_msg}</pre>
            </body>
            </html>""",
            status_code=500
        )

__all__ = ["app"]
