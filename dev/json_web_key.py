import base64
import json

class JsonWebKey:
    def __init__(self):
        self.kBase64Padding = "="
        self.kKeysTag = "keys"
        self.kKeyTypeTag = "kty"
        self.kKeyTag = "k"
        self.kKeyIdTag = "kid"
        self.kMediaSessionType = "type"
        self.kPersistentLicenseSession = "persistent-license"
        self.kSymmetricKeyValue = "oct"
        self.kTemporaryLicenseSession = "temporary"
        self.mJsonObjects = []
        self.mTokens = []
        self.mJsmnTokens = []

    def extractKeysFromJsonWebKeySet(self, jsonWebKeySet):
        keys = {}
        self.mJsonObjects.clear()
        self.mTokens.clear()
        self.mJsmnTokens.clear()

        if not self.parseJsonWebKeySet(jsonWebKeySet, self.mJsonObjects):
            return False

        if len(self.mJsonObjects) == 0 or not self.isJsonWebKeySet(self.mJsonObjects[0]):
            return False

        for i in range(1, len(self.mJsonObjects)):
            encodedKeyId = ""
            encodedKey = ""
            self.mTokens.clear()

            if not self.parseJsonObject(self.mJsonObjects[i], self.mTokens):
                return False

            if self.findKey(self.mJsonObjects[i], encodedKeyId, encodedKey):
                if encodedKeyId == "" or encodedKey == "":
                    print("Must have both key id and key in the JsonWebKey set.")
                    continue

                decodedKeyId = self.decodeBase64String(encodedKeyId)
                decodedKey = self.decodeBase64String(encodedKey)

                if decodedKeyId is None or decodedKey is None:
                    print("Failed to decode key id or key.")
                    continue

                keys[decodedKeyId] = decodedKey

        return keys

    def decodeBase64String(self, encodedText):
        if self.kBase64Padding in encodedText:
            return None

        remainder = len(encodedText) % 4
        paddedText = encodedText

        if remainder > 0:
            paddedText += self.kBase64Padding * (4 - remainder)

        try:
            decodedText = base64.urlsafe_b64decode(paddedText)
            return decodedText
        except:
            print("Malformed base64 encoded content found.")
            return None

    def findKey(self, jsonObject, keyId, encodedKey):
        if self.kKeyTypeTag in jsonObject:
            if jsonObject[self.kKeyTypeTag] != self.kSymmetricKeyValue:
                return False

        if self.kKeyIdTag in jsonObject:
            keyId.append(jsonObject[self.kKeyIdTag])

        if self.kKeyTag in jsonObject:
            encodedKey.append(jsonObject[self.kKeyTag])

        return True

    def parseJsonObject(self, jsonObject, tokens):
        try:
            parsedJson = json.loads(jsonObject)
            for key, value in parsedJson.items():
                tokens.append(key)
                tokens.append(value)
            return True
        except:
            print("Failed to parse JSON object.")
            return False

    def isJsonWebKeySet(self, jsonObject):
        if self.kKeysTag not in jsonObject:
            print("JSON Web Key does not contain keys.")
            return False
        return True

    def parseJsonWebKeySet(self, jsonWebKeySet, jsonObjects):
        if jsonWebKeySet == "":
            print("Empty JSON Web Key")
            return False

        try:
            parsedJson = json.loads(jsonWebKeySet)
            for key, value in parsedJson.items():
                if key == self.kKeysTag:
                    jsonObjects.append(json.dumps(value))
            return True
        except:
            print("Failed to parse JSON Web Key Set.")
            return False

# jsonWebKeySet = '''
# {
#     "keys": [
#         {
#             "kty": "oct",
#             "kid": "key1",
#             "k": "a2V5MQ=="
#         },
#         {
#             "kty": "oct",
#             "kid": "key2",
#             "k": "a2V5Mg=="
#         }
#     ]
# }
# '''

# jsonWebKey = JsonWebKey()
# keys = jsonWebKey.extractKeysFromJsonWebKeySet(jsonWebKeySet)
# print(keys)