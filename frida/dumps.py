import argparse
import time
import logging
from modules.devices import Device
from modules.scanner import Scan
from modules.logging import setup_logging

def main():
    # Setup logging
    logging = setup_logging()

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Android Widevine L3 dumper.')
    parser.add_argument('--cdm-version', help='The CDM version of the device e.g. \'14.0.0\'', default='14.0.0')
    parser.add_argument('--function-name', help='The name of the function to hook to retrieve the private key.', default='')
    parser.add_argument('--module-name', nargs='+', type=str, help='The names of the widevine `.so` modules', default=["libwvaidl.so", "libwvhidl.so"])
    args = parser.parse_args()

    # Extract command line arguments
    dynamic_function_name = args.function_name
    cdm_version = args.cdm_version
    module_names = args.module_name

    # Initialize device and scanner
    device = Device(dynamic_function_name, cdm_version, module_names)
    scanner = Scan(device.name)

    # Start scanning processes
    logging.info('Connected to %s', device.name)
    logging.info('Scanning all processes')

    for process in device.enumerate_processes():
        if 'drm' in process.name:
            for library in scanner.find_widevine_process(process.name):
                device.hook_to_process(process.name, library)

    logging.info('Functions hooked, now open the DRM stream test on Bitmovin from your Android device! https://bitmovin.com/demos/drm')

if __name__ == '__main__':
    main()
    while True:
        time.sleep(1000)
