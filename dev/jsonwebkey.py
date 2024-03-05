import json
import base64

class JSONWEBKEY:
    def __init__(self):
        pass
    
    def extractKeysFromJsonWebKeySet(self, jsonWebKeySet):
        keys = {}
        jsonObjects = self.parseJsonWebKeySet(jsonWebKeySet)
        
        if len(jsonObjects) == 0 or not self.isJsonWebKeySet(jsonObjects[0]):
            return False
        
        for i in range(1, len(jsonObjects)):
            encodedKeyId = ""
            encodedKey = ""
            
            if not self.parseJsonObject(jsonObjects[i]):
                return False
            
            if self.findKey(jsonObjects[i], encodedKeyId, encodedKey):
                if encodedKeyId == "" or encodedKey == "":
                    print("Must have both key id and key in the JsonWebKey set.")
                    continue
                
                decodedKeyId = self.decodeBase64String(encodedKeyId)
                decodedKey = self.decodeBase64String(encodedKey)
                
                keys[decodedKeyId] = decodedKey
        
        return keys
    
    def decodeBase64String(self, encodedText):
        # encodedText should not contain padding characters as per EME spec.
        if "=" in encodedText:
            return False
        
        # Since base64.b64decode() requires padding characters,
        # add them so length of encodedText is exactly a multiple of 4.
        remainder = len(encodedText) % 4
        paddedText = encodedText
        if remainder > 0:
            for i in range(4 - remainder):
                paddedText += "="
        
        decodedText = base64.b64decode(paddedText)
        return decodedText
    
    def findKey(self, jsonObject, keyId, encodedKey):
        # Only allow symmetric key, i.e. "kty":"oct" pair.
        if "kty" in jsonObject:
            if jsonObject["kty"] != "oct":
                return False
        
        if "kid" in jsonObject:
            keyId = jsonObject["kid"]
        
        if "k" in jsonObject:
            encodedKey = jsonObject["k"]
        
        return True
    
    def parseJsonObject(self, jsonObject):
        try:
            json.loads(jsonObject)
            return True
        except ValueError:
            return False
    
    def isJsonWebKeySet(self, jsonObject):
        if "keys" not in jsonObject:
            print("JSON Web Key does not contain keys.")
            return False
        
        return True
    
    def parseJsonWebKeySet(self, jsonWebKeySet):
        try:
            jsonObject = json.loads(jsonWebKeySet)
            if isinstance(jsonObject, list):
                return jsonObject
            else:
                return [jsonObject]
        except ValueError:
            return []
