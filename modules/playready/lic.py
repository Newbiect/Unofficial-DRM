import requests
import xml.etree.ElementTree as ET
import base64

widevine2_challenge = "0123456789abcdef0123456789abcdef"
license_server_url = "https://playready.directtaps.net/svc/rightsmanager.asmx/GetPlayReadyLicense"
headers = {
    "Content-Type": "application/soap+xml; charset=utf-8",
    "SOAPAction": "http://schemas.microsoft.com/DRM/PlayReady/soap/acquireLicense",
}

soap_envelope = f"""<?xml version="1.0" encoding="utf-8"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Header>
    <t:RequestSecurityToken xmlns:t="http://schemas.xmlsoap.org/ws/2005/02/trust">
      <wsp:AppliesTo xmlns:wsp="http://schemas.xmlsoap.org/ws/2004/09/policy">
        <EndpointReference xmlns="http://www.w3.org/2005/08/addressing">
          <Address>{license_server_url}</Address>
        </EndpointReference>
      </wsp:AppliesTo>
      <t:KeyType>http://schemas.xmlsoap.org/ws/2005/05/identity/NoProofKey</t:KeyType>
      <t:RequestType>http://schemas.xmlsoap.org/ws/2005/02/trust/Issue</t:RequestType>
      <t:TokenType>http://schemas.xmlsoap.org/ws/2005/02/sc/sct</t:TokenType>
    </t:RequestSecurityToken>
  </s:Header>
  <s:Body>
    <acquireLicenseRequest xmlns="http://schemas.microsoft.com/DRM/PlayReady/2007/03">
      <input>
        <KeyId>urn:microsoft:playready:kid:01234567-0123-0123-0123-0123456789ab</KeyId>
        <LicenseType>NonPersistent</LicenseType>
        <PlayRight>
          <AllowTestDevices>true</AllowTestDevices>
          <ContentKeySystems>
            <ContentKeySystem>urn:mpeg:dash:mp4protection:2011</ContentKeySystem>
          </ContentKeySystems>
          <PlaybackRestrictions>
            <MaxPlaybackDuration>0</MaxPlaybackDuration>
            <MaxTransferSize>0</MaxTransferSize>
            <PlaybackServerUrl>https://playback.example.com</PlaybackServerUrl>
          </PlaybackRestrictions>
          <PlaybackDeviceIds>
            <PlaybackDeviceId>0123456789abcdef0123456789abcdef</PlaybackDeviceId>
          </PlaybackDeviceIds>
        </PlayRight>
        <Widevine2Challenge>{widevine2_challenge}</Widevine2Challenge>
      </input>
    </acquireLicenseRequest>
  </s:Body>
</s:Envelope>
"""

response = requests.post(license_server_url, headers=headers, data=soap_envelope)
response_xml = response.content.decode("utf-8")
root = ET.fromstring(response_xml)
license_data = base64.b64decode(root.find(".//{http://schemas.microsoft.com/DRM/2007/03/protocols}response").text)
print(license_data)
