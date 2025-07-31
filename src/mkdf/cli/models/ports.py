from ...utils import find_free_subnet, find_free_port

def get_interactive_port_config():
    """Interactive port configuration"""
    default_subnet = find_free_subnet(quiet=True)
    print("\n=== Port Configuration (press Enter for defaults) ===")
    backend_port = input(f"Backend port [{find_free_port(8000)}]: ").strip() or str(find_free_port(8000))
    frontend_port = input(f"Frontend port [{find_free_port(3000)}]: ").strip() or str(find_free_port(3000))
    subnet = input(f"Docker subnet [{default_subnet}]: ").strip() or default_subnet
    prometheus_port = input(f"Prometheus port [{find_free_port(9090)}]: ").strip() or str(find_free_port(9090))
    grafana_port = input(f"Grafana port [{find_free_port(3001)}]: ").strip() or str(find_free_port(3001))
    traefik_port = input(f"Traefik HTTP port [{find_free_port(8080)}]: ").strip() or str(find_free_port(8080))
    traefik_dashboard_port = input(f"Traefik dashboard port [{find_free_port(8090)}]: ").strip() or str(find_free_port(8090))
    traefik_https_port = input(f"Traefik HTTPS port [{find_free_port(8085)}]: ").strip() or str(find_free_port(8085))

    return {
        'backend': int(backend_port),
        'frontend': int(frontend_port),
        'subnet': subnet,
        'prometheus': int(prometheus_port),
        'grafana': int(grafana_port),
        'traefik': int(traefik_port),
        'traefik_dashboard': int(traefik_dashboard_port),
        'traefik_https_port': int(traefik_https_port),
    }

