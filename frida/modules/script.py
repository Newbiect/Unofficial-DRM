import os
import base64
import json
from Crypto.PublicKey import RSA
from google.protobuf import message
import frida
from modules.wv_proto2_pb2 import SignedLicenseRequest
from modules.logging import setup_logging

logging = setup_logging()

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

class Scan:
    def __init__(self, device_name):
        self.logger = logging.getLogger(__name__)
        self.KEY_DUMP_LOC = 'keydump/'
        self.device_name = device_name
        self.saved_keys = {}
        self.frida_script = open('modules/script.js', 'r').read()
        self.device = {
            'device_id': None,
            'device_token': None,
            'device_key': os.urandom(16).hex(),
            'security_level': ''
        }
        self.widevine_libraries = [
            'libwvhidl.so',
            'libwvdrmengine.so',
            'liboemcrypto.so',
            'libmediadrm.so',
            'libwvdrm_L1.so',
            'libWVStreamControlAPI_L1.so',
            'libdrmwvmplugin.so',
            'libwvm.so'
        ]

    def export_key(self, k):
        root = SignedLicenseRequest()
        root.ParseFromString(k['id'])
        cid = root.Msg.ClientId
        system_id = cid.Token._DeviceCertificate.SystemId
        save_dir = os.path.join('key_dumps', f'{self.device_name}/private_keys/{system_id}/{str(k["key"].n)[:10]}')

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        with open(os.path.join(save_dir, 'client_id.bin'), 'wb+') as writer:
            writer.write(cid.SerializeToString())

        with open(os.path.join(save_dir, 'private_key.pem'), 'wb+') as writer:
            writer.write(k['key'].exportKey('PEM'))
        self.logger.info('Key pairs saved at ' + save_dir)

    def on_message(self, msg, data):
        try:
            if msg['payload'] == 'priv':
                self.logger.debug('processing private key')
                self.private_key_message(msg, data)
            elif msg['payload'] == 'id':
                self.logger.debug('processing id')
                self.license_request_message(data)
            elif msg['payload'] == 'device_id':
                self.logger.debug('processing device id')
                self.device_id_message(data)
            elif msg['payload'] == 'device_token':
                self.logger.debug('processing device token')
                self.device_token_message(data)
            elif msg['payload'] == 'security_level':
                tag = data.decode()
                if tag == 'L1':
                    self.device['security_level'] = 'LVL1'
                else:
                    self.device['security_level'] = 'LVL3'
            elif msg['payload'] == 'aes_key':
                self.aes_key_message(data)
            elif msg['payload'] == 'message':
                payload = json.loads(data.decode())
                self.logger.debug(
                    json.dumps(
                        payload,
                        indent=4
                    )
                )
            elif msg['payload'] == 'message_info':
                self.logger.info(data.decode())

        except:
            self.logger.error('unable to process the message')
            self.logger.error(msg)
            self.logger.error(data)

    def private_key_message(self, private_key_message, data):
        try:
            try:
                key = RSA.importKey(data)
                cur = self.saved_keys.get(key.n, {})
                if 'id' in cur:
                    if 'key' not in cur:
                        cur['key'] = key
                        self.saved_keys[key.n] = cur
                        self.export_key(cur)
                else:
                    self.saved_keys[key.n] = {'key': key}
            except:
                self.logger.error('unable to load private key')
                self.logger.error(data)
                pass
        except:
            self.logger.error('payload of type priv failed')
            self.logger.error(private_key_message)

    def license_request_message(self, data):
        with open('license_request.bin', 'wb+') as f:
            f.write(data)
        root = SignedLicenseRequest()
        try:
            root.ParseFromString(data)
        except message.DecodeError:
            return
        try:
            key = RSA.importKey(root.Msg.ClientId.Token._DeviceCertificate.PublicKey)
            cur = self.saved_keys.get(key.n, {})
            if 'key' in cur:
                if 'id' not in cur:
                    cur['id'] = data
                    self.saved_keys[key.n] = cur
                    self.export_key(cur)
            else:
                self.saved_keys[key.n] = {'id': data}
        except Exception as error:
            self.logger.error(error)

    def device_id_message(self, data_buffer):
        if not self.device['device_id']:
            self.device['device_id'] = data_buffer.hex()
        if self.device['device_id'] and self.device['device_token'] and self.device['device_key']:
            self.save_key_box()

    def device_token_message(self, data_buffer):
        if not self.device['device_token']:
            self.device['device_token'] = data_buffer.hex()
        if self.device['device_id'] and self.device['device_token']:
            self.save_key_box()

    def aes_key_message(self, data_buffer):
        if not self.device['device_key']:
            self.device['device_key'] = data_buffer.hex()
        if self.device['device_id'] and self.device['device_token']:
            self.save_key_box()

    def find_widevine_process(self, dev, process_name):
        process = dev.attach(process_name)
        script = process.create_script(self.frida_script)
        script.load()
        loaded = []
        try:
            for lib in self.widevine_libraries:
                try:
                    loaded.append(script.exports.widevinelibrary(lib))
                except:
                    pass
        finally:
            process.detach()
            return loaded

    def hook_to_process(self, device, process, library):
        session = device.attach(process)
        script = session.create_script(self.frida_script)
        script.on('message', self.on_message)
        script.load()
        script.exports.inject(library, process)
        return session

    def save_key_box(self):
        try:
            if self.device['device_id'] is not None and self.device['device_token'] is not None:
                self.logger.info('saving key box')
                keybox = Keybox(self.device)
                box = os.path.join('key_dumps', f'{self.device_name}/key_boxes/{keybox.system_id}')
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

def create_table():
    a = []
    for i in range(256):
        k = i << 24
        for _ in range(8):
            k = (k << 1) ^ 0x4c11db7 if k & 0x80000000 else k << 1
        a.append(k & 0xffffffff)
    return a

def crc32_mpeg(data, length):
    crc_val = 0xFFFFFFFF
    crctab = create_table()
    for i in range(length):
        crc_val = (crctab[(data[i] & 0xFF) ^ (crc_val >> 24)] ^ (crc_val << 8)) & 0xFFFFFFFF
    return crc_val

class Keybox:
    def __init__(self, keybox_data: any):
        if isinstance(keybox_data, str):
            self.__keybox = b64decode(keybox_data)
        elif isinstance(keybox_data, io.BufferedReader):
            self.__keybox = keybox_data.read()
        elif isinstance(keybox_data, dict):
            self.__keybox = self.__generate_crc(keybox_data)
        else:
            print(type(keybox_data))
            raise ValueError('unable to read the file/string, etc')

        self.__parse()

    @staticmethod
    def __generate_crc(keybox) -> bytes:
        device_id = keybox['device_id']
        device_token = keybox['device_token']
        device_key = keybox['device_key']
        key_box = bytes.fromhex(device_id) + bytes.fromhex(device_key) + bytes.fromhex(device_token) + b'kbox'
        crc = crc32_mpeg(key_box, len(key_box))
        key_box += struct.pack('>I', crc)
        key_box += keybox['security_level'].encode()
        return key_box

    def __parse(self):
        self.device_id = self.__keybox[0:32]
        # this is the aes key
        self.device_key = self.__keybox[32:48]
        self.device_token = self.__keybox[48:120]
        self.keybox_tag = self.__keybox[120:124]
        self.crc32 = struct.unpack('>I', self.__keybox[124:128])[0]
        self.crc32_raw = hexlify(self.__keybox[124:128])
        # this is optional, most likely not required
        self.level_tag = self.__keybox[128:132]
        self.flags = struct.unpack(">L", self.__keybox[48:120][0:4])[0]
        self.version = struct.unpack(">I", self.__keybox[48:52])[0]
        self.system_id = struct.unpack(">I", self.__keybox[52:56])[0]
        # or unique_id as in wv pdf, encrypted by pre-provisioning key
        self.provisioning_id = self.__keybox[56:72]
        # encrypted with unique id, contains device key, device key hash, and flags
        self.encrypted_bits = self.__keybox[72:120]

    def __repr__(self):
        return json.dumps({
            'device_id': b64encode(self.device_id).decode(),
            'device_id_size': len(self.device_id),
            'device_key': b64encode(self.device_key).decode(),
            'device_token': b64encode(self.device_token).decode(),
            'device_token_size': len(self.device_token),
            'kbox_tag': self.keybox_tag.decode(),
            'crc32': self.crc32,
            'crc32_raw': self.crc32_raw.decode(),
            'lvl1_tag': self.level_tag.decode(),
            'flags': self.flags,
            'released': True if self.flags & 2 == 2 else False,
            'version': self.version,
            'system_id': self.system_id,
            'provisioning_id': b64encode(self.provisioning_id).decode(),
            'encrypted_bits': b64encode(self.encrypted_bits).decode(),
            'keybox': b64encode(self.__keybox).decode()
        }, indent=4)

    def get_keybox(self):
        return self.__keybox
