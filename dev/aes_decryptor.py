import logging
from Crypto import AES
from Crypto.Util import Counter

def decrypt(key, iv, source, destination, clearDataLengths, encryptedDataLengths):
    if len(key) != 16 or len(clearDataLengths) != len(encryptedDataLengths):
        logging.error("Invalid key or data lengths")
        return None
    
    blockOffset = 0
    previousEncryptedCounter = b'\x00' * 16
    offset = 0
    cipher = AES.new(key, AES.MODE_CTR, counter=Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big')))
    
    for i in range(len(clearDataLengths)):
        numBytesOfClearData = clearDataLengths[i]
        if numBytesOfClearData > 0:
            destination[offset:offset+numBytesOfClearData] = source[offset:offset+numBytesOfClearData]
            offset += numBytesOfClearData
        
        numBytesOfEncryptedData = encryptedDataLengths[i]
        if numBytesOfEncryptedData > 0:
            encryptedData = source[offset:offset+numBytesOfEncryptedData]
            decryptedData = cipher.encrypt(encryptedData)
            destination[offset:offset+numBytesOfEncryptedData] = decryptedData
            offset += numBytesOfEncryptedData
    
    return offset