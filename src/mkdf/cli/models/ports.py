from ...utils import find_free_subnet

def get_interactive_port_config():
    """Interactive port configuration"""
    default_subnet = find_free_subnet()
    print("\n=== Port Configuration (press Enter for defaults) ===")
    backend_port = input("Backend port [8000]: ").strip() or "8000"
    frontend_port = input("Frontend port [3000]: ").strip() or "3000"
    subnet = input(f"Docker subnet [{default_subnet}]: ").strip() or default_subnet
    prometheus_port = input("Prometheus port [9090]: ").strip() or "9090"
    grafana_port = input("Grafana port [3001]: ").strip() or "3001"
    traefik_port = input("Traefik HTTP port [80]: ").strip() or "80"
    traefik_dashboard_port = input("Traefik dashboard port [8080]: ").strip() or "8080"

    return {
        'backend': int(backend_port),
        'frontend': int(frontend_port),
        'subnet': subnet,
        'prometheus': int(prometheus_port),
        'grafana': int(grafana_port),
        'traefik': int(traefik_port),
        'traefik_dashboard': int(traefik_dashboard_port),
    }

