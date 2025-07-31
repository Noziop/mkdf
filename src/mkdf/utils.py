from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import socket
import logging
import subprocess
import ipaddress
import json

console = Console()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def show_error(message: str, suggestion: str = None):
    error_panel = Panel(
        f"❌ {message}\n\n {suggestion}" if suggestion else f"❌ {message}",
        title="Error",
        border_style="red"
    )
    console.print(error_panel)

def create_with_progress(description: str):
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    )

def find_free_port(start_port=1025, max_attempts=500):
    """Find an available port, skipping well-known system ports."""
    if start_port < 1024:
        logging.warning(f"Specified start_port {start_port} is in the system port range (1-1023). Starting search from 1024.")
        start_port = 1024

    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                logging.info(f"Found free port: {port}")
                return port
        except OSError as e:
            logging.debug(f"Port {port} is in use, trying next. Error: {e}")
            continue
    
    logging.error(f"Could not find a free port in the range {start_port}-{start_port + max_attempts}")
    raise RuntimeError(f"No free port found in range {start_port}-{start_port + max_attempts}")


def find_free_subnet(start_octet=18, max_attempts=100, quiet=False):
    """Find an available /16 subnet in the 172.x.0.0 range for Docker networks."""
    existing_subnets = set()
    
    try:
        result = subprocess.run(
            ["docker", "network", "ls", "-q"],
            capture_output=True, text=True, check=True
        )
        network_ids = result.stdout.strip().split()

        if not network_ids:
            logging.info("No existing Docker networks found.")
        else:
            inspect_result = subprocess.run(
                ["docker", "network", "inspect", *network_ids],
                capture_output=True, text=True, check=True
            )
            networks_data = json.loads(inspect_result.stdout)
            if networks_data is None:
                networks_data = []
            
            
            for network in networks_data:
                if 'IPAM' in network and 'Config' in network['IPAM'] and network['IPAM']['Config'] is not None:
                    for config in network['IPAM']['Config']:
                        if 'Subnet' in config and config['Subnet']:
                            try:
                                existing_subnets.add(ipaddress.ip_network(config['Subnet'], strict=False))
                            except ValueError:
                                logging.warning(f"Ignoring invalid subnet from Docker network inspection: {config['Subnet']}")

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        if not quiet:
            logging.warning(f"Could not inspect Docker networks: {e}. Assuming no conflicts and proceeding.")
    except json.JSONDecodeError:
        if not quiet:
            logging.warning("Failed to parse Docker network inspection output.")

    for i in range(max_attempts):
        octet = start_octet + i
        if not (16 <= octet <= 31):
            continue

        subnet_str = f"172.{octet}.0.0/16"
        candidate_subnet = ipaddress.ip_network(subnet_str, strict=False)
        
        if not any(candidate_subnet.overlaps(existing) for existing in existing_subnets):
            if not quiet:
                logging.info(f"Found available subnet: {subnet_str}")
            return subnet_str
            
    logging.error("Failed to find an available Docker subnet.")
    raise RuntimeError("Could not find an available Docker subnet after multiple attempts.")