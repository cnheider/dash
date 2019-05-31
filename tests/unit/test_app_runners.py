import time
import sys
import requests
import pytest

import dash_html_components as html
import dash


def test_threaded_server_smoke(thread_server):
    app = dash.Dash(__name__)

    app.layout = html.Div(
        [
            html.Button("click me", id="clicker"),
            html.Div(id="output", children="hello thread"),
        ]
    )
    thread_server(app, debug=True, use_reloader=False, use_debugger=True)
    time.sleep(0.2)
    r = requests.get(thread_server.url)
    assert r.status_code == 200, "the threaded server is reachable"
    assert 'id="react-entry-point"' in r.text, "the entrypoint is present"


@pytest.mark.skipif(
    sys.version_info < (3,), reason="requires python3 for process testing"
)
def test_process_server_smoke(process_server):
    process_server("simple_app")
    time.sleep(2.5)
    r = requests.get(process_server.url)
    assert r.status_code == 200, "the server is reachable"
    assert 'id="react-entry-point"' in r.text, "the entrypoint is present"