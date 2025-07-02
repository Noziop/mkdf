
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
def start_web_server(port: int = typer.Option(None, "--port", "-p", help="Port to run the server on."), 
                    detach: bool = typer.Option(True, "--detach/--no-detach", help="Run in detached (background) mode.")):
    """Starts the MKDF web server."""
    if is_server_running():
        print("Server is already running.")
        return

    if port is None:
        port = find_free_port()

    if detach:
        # Background with PID file
        pid = os.fork()
        if pid == 0:
            # Child process
            with open(PID_FILE, "w") as f:
                f.write(str(os.getpid()))
            uvicorn.run(app, host="0.0.0.0", port=port)
        else:
            # Parent process
            print(f"Server started in background with PID {pid} on port {port}.")
    else:
        # Foreground
        uvicorn.run(app, host="0.0.0.0", port=port)

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


