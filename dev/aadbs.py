import subprocess
import json
import xml.etree.ElementTree as ET
import re
import sys
import logging
import time
from colorama import Fore, Style

def setup_logger():
    logging.basicConfig(filename='adb_drm_info.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s')

def check_adb():
    # Check if ADB is installed
    try:
        subprocess.run(['adb', 'version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except FileNotFoundError:
        return False
    return True

def parse_drm_info_xml(drm_output):
    # Parse DRM information from XML format
    drm_info = {}
    root = ET.fromstring(drm_output)
    for child in root:
        drm_info[child.tag] = child.text.strip()
    return drm_info

def parse_drm_info_json(drm_output):
    # Parse DRM information from JSON format
    return json.loads(drm_output)

def get_live_processes(device_serial=None, interval=5):
    try:
        command = ['adb']
        if device_serial:
            command.extend(['-s', device_serial])
        
        print("Capturing live processes (press Ctrl+C to stop)...")
        while True:
            process = subprocess.run(command + ['shell', 'ps'], capture_output=True, check=True, text=True)
            processes_output = process.stdout.strip().split('\n')
            
            print("Live Processes:")
            for line in processes_output[1:]:
                print(line)
            
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Live process capture stopped.")
    except subprocess.CalledProcessError as e:
        handle_adb_error(e)
    except subprocess.TimeoutExpired:
        handle_adb_timeout()

def handle_adb_error(error):
    logging.error(f"ADB command error: {error.stderr}")
    if "not found" in error.stderr:
        print(f"{Fore.RED}Error: 'dumpsys' command not found. Make sure your device supports this command.{Style.RESET_ALL}")
    elif "device unauthorized" in error.stderr:
        print(f"{Fore.RED}Error: Device unauthorized. Please authorize the device for debugging.{Style.RESET_ALL}")
    elif "device offline" in error.stderr:
        print(f"{Fore.RED}Error: Device offline. Make sure the device is connected and reachable.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Error: {error.stderr}{Style.RESET_ALL}")

def handle_adb_timeout():
    logging.error("ADB command timed out.")
    print(f"{Fore.RED}Error: ADB command timed out. Please check your device connection and try again.{Style.RESET_ALL}")

def get_drm_info(device_serial=None, package_name=None, output_format='json', timeout=None, save_to_file=False):
    # Run adb shell commands to get DRM info
    try:
        command = ['adb']
        if device_serial:
            command.extend(['-s', device_serial])
        
        drm_info = {}

        # Query DRM-related system services
        services = ['media.drm', 'media.metrics', 'media.drmserver', 'media.codec', 'media.extractor']
        for service in services:
            process = subprocess.run(command + ['shell', 'dumpsys', service], capture_output=True, check=True, text=True, timeout=timeout)
            service_output = process.stdout
            drm_info[service] = service_output.strip()

        # Query additional Widevine-related packages
        widevine_packages = ['com.android.providers.media', 'com.android.providers.downloads', 'com.widevine.alpha']
        for package in widevine_packages:
            process = subprocess.run(command + ['shell', 'pm', 'dump', package], capture_output=True, check=True, text=True, timeout=timeout)
            package_output = process.stdout
            drm_info[package] = package_output.strip()

        # Query all running processes
        process = subprocess.run(command + ['shell', 'ps'], capture_output=True, check=True, text=True, timeout=timeout)
        drm_info['all_processes'] = process.stdout.strip()

        print("Raw DRM Info:")
        for item, output in drm_info.items():
            print(f"Item: {item}\n{output}\n")  # Print the raw output
        
        if not any(drm_info.values()):
            logging.error("No DRM information retrieved.")
            print(f"{Fore.RED}Error: No DRM information retrieved.{Style.RESET_ALL}")
            return None
        
        if save_to_file:
            filename = f"drm_info_{device_serial}.txt" if device_serial else "drm_info.txt"
            with open(filename, 'w') as f:
                for item, output in drm_info.items():
                    f.write(f"Item: {item}\n{output}\n\n")
                print(f"{Fore.GREEN}DRM information saved to '{filename}'.{Style.RESET_ALL}")
        
        return drm_info
    except subprocess.CalledProcessError as e:
        handle_adb_error(e)
        return None
    except subprocess.TimeoutExpired:
        handle_adb_timeout()
        return None

def parse_timeout(timeout_str):
    try:
        timeout = int(timeout_str)
    except ValueError:
        logging.error("Invalid timeout format specified.")
        print(f"{Fore.RED}Error: Invalid timeout format. Please enter a valid integer value.{Style.RESET_ALL}")
        sys.exit(1)
    return timeout

def list_devices():
    # List connected devices
    try:
        command = ['adb', 'devices', '-l']

        process = subprocess.run(command, capture_output=True, check=True, text=True)
        devices_output = process.stdout
        devices = []
        lines = devices_output.strip().split('\n')[1:]
        for line in lines:
            device_info = line.split()
            if device_info and device_info[1] == 'device':
                devices.append({'serial': device_info[0], 'model': device_info[4], 'manufacturer': device_info[1], 'android_version': device_info[5]})
        return devices
    except subprocess.CalledProcessError as e:
        handle_adb_error(e)
        return []

def get_device_info(device_serial=None):
    # Get detailed device information
    try:
        command = ['adb']
        if device_serial:
            command.extend(['-s', device_serial])
        command.extend(['shell', 'getprop'])

        process = subprocess.run(command, capture_output=True, check=True, text=True)
        device_info = process.stdout
        return device_info
    except subprocess.CalledProcessError as e:
        handle_adb_error(e)
        return None

if __name__ == "__main__":
    setup_logger()

    if not check_adb():
        logging.error("ADB is not installed or not added to system PATH.")
        print(f"{Fore.RED}ADB is not installed or not added to system PATH. Please install ADB and try again.{Style.RESET_ALL}")
        exit()

    print("Checking ADB connection...")
    devices = list_devices()
    if not devices:
        logging.error("No Android device is connected.")
        print(f"{Fore.RED}No Android device is connected. Please connect your Android device via USB and enable USB debugging.{Style.RESET_ALL}")
        exit()

    print(f"{Fore.YELLOW}Connected devices:{Style.RESET_ALL}")
    for idx, device in enumerate(devices, start=1):
        print(f"{idx}. {device['manufacturer']} {device['model']} ({device['android_version']}) - {device['serial']}")

    device_idx = int(input(f"{Fore.YELLOW}Select device number: {Style.RESET_ALL}")) - 1
    selected_device = devices[device_idx]

    device_info = get_device_info(selected_device['serial'])
    if device_info:
        print(f"{Fore.GREEN}Device Information:{Style.RESET_ALL}")
        print(device_info)

    while True:
        package_name = input(f"{Fore.YELLOW}Enter package name (Leave empty to get general DRM info, 'all' to check all packages, 'exit' to quit): {Style.RESET_ALL}").strip()
        if package_name.lower() == 'exit':
            break

        output_format = input(f"{Fore.YELLOW}Enter output format (json/xml): {Style.RESET_ALL}").strip().lower()
        timeout_str = input(f"{Fore.YELLOW}Enter timeout in seconds: {Style.RESET_ALL}").strip()

        timeout = parse_timeout(timeout_str)

        if package_name.lower() == 'all':
            package_name = None

        logging.info(f"Getting DRM/CDM Information for package: {package_name}")
        drm_info = get_drm_info(selected_device['serial'], package_name, output_format, timeout, save_to_file=True)
        if drm_info:
            print(f"{Fore.GREEN}DRM/CDM Information:{Style.RESET_ALL}")
            print(json.dumps(drm_info, indent=4) if output_format == 'json' else ET.tostring(ET.ElementTree(ET.fromstring(json.dumps(drm_info)))).decode())
