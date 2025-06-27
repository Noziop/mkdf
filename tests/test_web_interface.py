import pytest
import requests
import subprocess
import time
import os
from mkdf.web.server import find_free_port

@pytest.fixture(scope="module")
def live_server_url():
    port = find_free_port(start_port=9600) # Use a different range for tests
    # Start the Flask app in a separate process
    process = subprocess.Popen(["python3", "-c", 
                                f"from mkdf.web.server import app; app.run(host='0.0.0.0', port={port}, debug=False)"],
                               env={**os.environ, 'FLASK_APP': 'mkdf.web.server'})
    url = f"http://127.0.0.1:{port}"
    
    # Wait for the server to start
    for _ in range(10):
        try:
            requests.get(url)
            break
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
    else:
        pytest.fail("Flask server did not start.")

    yield url
    process.terminate()
    process.wait()

def test_web_server_startup(live_server_url):
    response = requests.get(live_server_url)
    assert response.status_code == 200
    assert "MKDF - Professional Project Creator" in response.text

def test_create_pattern_web(live_server_url):
    pattern = "web_test/{a/,b.txt}"
    response = requests.post(f"{live_server_url}/create_pattern", json={'pattern': pattern})
    assert response.status_code == 200
    data = response.json()
    assert data['success'] == True
    assert "Project structure created successfully!" in data['message']
    # Clean up created files (optional, but good practice for tests)
    # import shutil
    # shutil.rmtree("web_test")

def test_create_template_web(live_server_url):
    project_name = "web_template_test"
    template_type = "simple"
    response = requests.post(f"{live_server_url}/create_template", json={'project_name': project_name, 'template_type': template_type})
    assert response.status_code == 200
    data = response.json()
    assert data['success'] == True
    assert f"Successfully created project '{project_name}' from template '{template_type}'." in data['message']

def test_create_docker_web(live_server_url):
    project_name = "web_docker_test"
    components = ["fastapi", "vue"]
    response = requests.post(f"{live_server_url}/create_docker", json={'project_name': project_name, 'components': components})
    assert response.status_code == 200
    data = response.json()
    assert data['success'] == True
    assert f"Successfully created Docker project '{project_name}' with components {components}." in data['message']
