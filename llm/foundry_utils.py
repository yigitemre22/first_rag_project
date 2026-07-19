import re
import subprocess
import time

def _get_foundry_port()->str|None:

    results=subprocess.run(
        ["foundry","service","status"],
        capture_output=True,
        text=True
    )

    if results.returncode !=0:
        return None
    
    match=re.search(
        r"http://127\.0\.0\.1:(\d+)/openai/status",
        results.stdout,
    )

    if match:
        return match.group(1)
    
    return None

def ensure_foundry_running():

    port=_get_foundry_port()

    if port :
        return port
    
    print("foundry service is not running")
    print("starting foundry service...")

    subprocess.Popen(
        ["foundry","service","start"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    for _ in range(30):

        time.sleep(1)

        port=_get_foundry_port()

        if port :
            print(f"foundry started on port {port}")
            return port
    
    raise RuntimeError(
        "foundry service could not be started"
    )

def get_foundry_base_url():

    port=ensure_foundry_running()

    return f"http://127.0.0.1:{port}/v1"