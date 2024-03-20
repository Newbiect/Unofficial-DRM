import os
import logging
import base64
import frida
from Crypto.PublicKey import RSA
from modules.wv_proto2_pb2 import SignedLicenseRequest
from modules.keybox import Keybox

class Device:
    def __init__(self, dynamic_function_name, cdm_version, module_names):
        self.logger = logging.getLogger(__name__)
        self.saved_keys = {}
        self.widevine_libraries = module_names
        self.usb_device = frida.get_usb_device()
        self.name = self.usb_device.name

        with open('./modules/script.js', 'r', encoding="utf_8") as script:
            self.frida_script = script.read()
        self.frida_script = self.frida_script.replace(r'${DYNAMIC_FUNCTION_NAME}', dynamic_function_name)
        self.frida_script = self.frida_script.replace(r'${CDM_VERSION}', cdm_version)

    def export_key(self, key, client_id):
        save_dir = os.path.join(
            'key_dumps',
            f'{self.name}',
            'private_keys',
            f'{client_id.Token._DeviceCertificate.SystemId}',
            f'{str(key.n)[:10]}'
        )

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        with open(os.path.join(save_dir, 'client_id.bin'), 'wb+') as writer:
            writer.write(client_id.SerializeToString())

        with open(os.path.join(save_dir, 'private_key.pem'), 'wb+') as writer:
            writer.write(key.exportKey('PEM'))
        self.logger.info('Key pairs saved at %s', save_dir)

    def on_message(self, msg, data):
        if 'payload' in msg:
            if msg['payload'] == 'private_key':
                key = RSA.import_key(data)
                if key.n not in self.saved_keys:
                    self.logger.debug(
                        'Retrieved key: \n\n%s\n',
                        key.export_key().decode("utf-8")
                    )
                self.saved_keys[key.n] = key
            elif msg['payload'] == 'device_info':
                self.license_request_message(data)
            elif msg['payload'] == 'message_info':
                self.logger.info(data.decode())

    def license_request_message(self, data):
        self.logger.debug(
            'Retrieved build info: \n\n%s\n',
            base64.b64encode(data).decode('utf-8')
        )
        root = SignedLicenseRequest()
        root.ParseFromString(data)
        public_key = root.Msg.ClientId.Token._DeviceCertificate.PublicKey
        key = RSA.importKey(public_key)
        cur = self.saved_keys.get(key.n)

        if cur is not None:
            self.export_key(cur, root.Msg.ClientId)

    def find_widevine_process(self, process_name):
        process = self.usb_device.attach(process_name)
        script = process.create_script(self.frida_script)
        script.load()
        loaded_modules = []
        try:
            for lib in self.widevine_libraries:
                try:
                    loaded_modules.append(script.exports.getmodulebyname(lib))
                except frida.core.RPCException as e:
                    # Hide the cases where the module cannot be found
                    continue
                except Exception as e:
                    raise(e)
        finally:
            process.detach()
            return loaded_modules

    def hook_to_process(self, process, library):
        session = self.usb_device.attach(process)
        script = session.create_script(self.frida_script)
        script.on('message', self.on_message)
        script.load()
        script.exports.hooklibfunctions(library)
        return session

    def save_key_box(self):
        try:
            if self.device['device_id'] is not None and self.device['device_token'] is not None:
                self.logger.info('saving key box')
                keybox = Keybox(self.device)
                box = os.path.join('key_dumps', f'{self.name}/key_boxes/{keybox.system_id}')
                self.logger.debug(f'saving to {box}')
                if not os.path.exists(box):
                    os.makedirs(box)
                with open(os.path.join(box, f'{keybox.system_id}.bin'), 'wb') as writer:
                    writer.write(keybox.get_keybox())
                with open(os.path.join(box, f'{keybox.system_id}.json'), 'w') as writer:
                    writer.write(keybox.__repr__())
                self.logger.info(f'saved keybox to {box}')
        except Exception as error:
            self.logger.error('unable to save keybox')
            self.logger.error(error)
