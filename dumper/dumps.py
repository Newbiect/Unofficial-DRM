import subprocess
import threading
import sys
import os
import signal

def forward_adb_traffic():
    # Forward ADB traffic to MITM proxy
    subprocess.run(["adb", "forward", "tcp:8080", "tcp:8080"])

def start_mitm_proxy():
    # Start MITM proxy
    mitmproxy_cmd = "mitmproxy"
    subprocess.run(mitmproxy_cmd, shell=True, check=False)

def main():
    try:
        # Check if adb is installed
        adb_check = subprocess.run(["adb", "version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if adb_check.returncode != 0:
            print("ADB is not installed or not in PATH.")
            sys.exit(1)

        # Check if mitmproxy is installed
        mitmproxy_check = subprocess.run(["mitmproxy", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if mitmproxy_check.returncode != 0:
            print("mitmproxy is not installed or not in PATH.")
            sys.exit(1)

        print("Forwarding ADB traffic to MITM proxy...")
        forward_thread = threading.Thread(target=forward_adb_traffic)
        forward_thread.start()

        print("Starting MITM proxy...")
        start_mitm_proxy()

    except KeyboardInterrupt:
        print("\nProcess interrupted. Exiting.")
        os.killpg(os.getpgid(forward_thread.pid), signal.SIGTERM)

if __name__ == "__main__":
    main()
