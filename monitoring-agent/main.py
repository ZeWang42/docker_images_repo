import os
import time
import threading
from pathlib import Path

import requests
from fastapi import FastAPI

app = FastAPI()

# Shared global
latest_metrics = ""

def fetch_metrics():
    global latest_metrics
    apiserver = os.environ.get("KUBERNETES_SERVICE_HOST", "kubernetes.default.svc")
    port = os.environ.get("KUBERNETES_SERVICE_PORT_HTTPS", "443")
    node = os.environ.get("NODE_NAME")
    url = f"https://{apiserver}:{port}/api/v1/nodes/{node}/proxy/metrics/cadvisor"
    token = Path("/var/run/secrets/kubernetes.io/serviceaccount/token").read_text().strip()

    while True:
        try:
            resp = requests.get(url, headers={"Authorization": f"Bearer {token}"}, verify=False, timeout=5)
            if resp.status_code == 200:
                latest_metrics = resp.text
                print(f"✅ updated latest_metrics with {len(latest_metrics)} bytes", flush=True)
            else:
                print(f"⚠️ fetch failed: {resp.status_code}", flush=True)
        except Exception as e:
            print("❌ fetch error:", e, flush=True)
        time.sleep(10)

# start thread immediately
threading.Thread(target=fetch_metrics, daemon=True).start()

@app.get("/raw")
def get_raw():
    return {"raw": latest_metrics[:500]}  # first 500 chars

@app.get("/cpu")
def get_cpu():
    if not latest_metrics:
        return {"cpu_usage": "no data yet"}
    lines = latest_metrics.splitlines()
    cpu_lines = [l for l in lines if "container_cpu" in l]
    return {"cpu_usage": "\n".join(cpu_lines[:50])}  # limit preview

