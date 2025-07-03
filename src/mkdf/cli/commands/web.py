
import typer
import uvicorn
from pathlib import Path
import os
import signal
import psutil

from mkdf.web.server import app

web = typer.Typer()

PID_FILE = Path.home() / ".config" / "mkdf" / "web.pid"

def is_server_running():
    if not PID_FILE.exists():
        return False
    try:
        pid = int(PID_FILE.read_text())
        return psutil.pid_exists(pid)
    except (ValueError, psutil.NoSuchProcess):
        return False

from mkdf.utils import find_free_port

@web.command("start")
def start_web_server(
    back_port: int = typer.Option(None, "--back-port", help="Backend port"),
    front_port: int = typer.Option(None, "--front-port", help="Frontend port"),  
    detach: bool = typer.Option(True, "--detach/--no-detach")
):
    from mkdf.web.backend.core.config import Settings
    settings = Settings()
    
    # Gestion intelligente des ports
    if back_port:
        # Port spécifié par user → Scan à partir de ce port si occupé
        backend_port = find_free_port(back_port)
        if backend_port != back_port:
            print(f"⚠️  Port {back_port} occupé, utilise {backend_port} à la place")
    else:
        # Port depuis config.json
        backend_port = find_free_port(settings.web_port_start)
    
    if front_port:
        # Port spécifié par user → Scan à partir de ce port si occupé  
        frontend_port = find_free_port(front_port)
        if frontend_port != front_port:
            print(f"⚠️  Port {front_port} occupé, utilise {frontend_port} à la place")
    else:
        # Port standard frontend
        frontend_port = find_free_port(3000)
    
    print(f"🚀 MKDF Web starting...")
    print(f"📡 Backend:  http://localhost:{backend_port}")
    print(f"🎨 Frontend: http://localhost:{frontend_port}")

    start_dual_servers(backend_port, frontend_port)

def start_dual_servers(backend_port, frontend_port):
    import subprocess
    import threading
    
    # Backend FastAPI
    def run_backend():
        from mkdf.web.backend.main import app
        uvicorn.run(app, host="127.0.0.1", port=backend_port)
    
    # Frontend Vite dev server  
    def run_frontend():
        frontend_dir = Path(__file__).parent.parent.parent / "web" / "frontend"
        subprocess.run([
            "npm", "run", "dev", "--", "--port", str(frontend_port)
        ], cwd=frontend_dir)
    
    # Lance les deux en parallèle
    backend_thread = threading.Thread(target=run_backend)
    frontend_thread = threading.Thread(target=run_frontend)
    
    backend_thread.start()
    frontend_thread.start()
    
    # Attendre les deux
    backend_thread.join()
    frontend_thread.join()

@web.command("stop")
def stop_web_server():
    """Stops the MKDF web server."""
    if not is_server_running():
        print("Server is not running.")
        return

    try:
        pid = int(PID_FILE.read_text())
        os.kill(pid, signal.SIGTERM)
        PID_FILE.unlink()
        print(f"Server with PID {pid} stopped.")
    except (ValueError, FileNotFoundError, ProcessLookupError) as e:
        print(f"Error stopping server: {e}")
        if PID_FILE.exists():
            PID_FILE.unlink()

@web.command("status")
def server_status():
    """Checks the status of the MKDF web server."""
    if is_server_running():
        pid = int(PID_FILE.read_text())
        print(f"Server is running with PID {pid}.")
    else:
        print("Server is not running.")


