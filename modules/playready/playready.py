from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64

key = RSA.generate(2048)

public_key_xml = key.exportKey('PEM').decode('utf-8')

license_template = """<?xml version="1.0" encoding="UTF-8"?>
<PlayReadyLicenseResponse xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <License>
    <ContentHeader>
      <DataDescription xmlns="">
        <PlayRight>
          <Agenda>
            <AgendaItem>
              <ContentType>
                <ProtectionSystemID>urn:mpeg:dash:23003:3:video:2012</ProtectionSystemID>
              </ContentType>
              <PlaybackSystemIDs>
                <PlaybackSystemID>urn:mpeg:dash:23003:4:android:2012</PlaybackSystemID>
              </PlaybackSystemIDs>
            </AgendaItem>
          </Agenda>
        </PlayRight>
      </DataDescription>
    </ContentHeader>
    <Content KeyId="{key_id}">
      < RightsManagement>
        <LicenseTemplate ID="{template_id}" xmlns="">
          <Agenda>
            <AgendaItem>
              <ContentType>
                <ProtectionSystemID>urn:mpeg:dash:23003:3:video:2012</ProtectionSystemID>
              </ContentType>
              <PlaybackSystemIDs>
                <PlaybackSystemID>urn:mpeg:dash:23003:4:android:2012</PlaybackSystemID>
              </PlaybackSystemIDs>
            </AgendaItem>
          </Agenda>
          <Signature xmlns="">
            <SignedInfo>
              <CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#" />
              <SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256" />
              <Reference URI="">
                <Transforms>
                  <Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature" />
                </Transforms>
                <DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256" />
                <DigestValue>{digest}</DigestValue>
              </Reference>
            </SignedInfo>
            <SignatureValue>{signature}</SignatureValue>
          </Signature>
        </LicenseTemplate>
      </RightsManagement>
    </Content>
  </License>
</PlayReadyLicenseResponse>
"""

digest = SHA256.new(license_template.format(key_id='key-id', template_id='template-id').encode('utf-8')).digest()
signature = pkcs1_15.new(key).sign(SHA256.new(digest))
base64_signature = base64.b64encode(signature).decode('utf-8')

license = license_template.format(key_id='key-id', template_id='template-
id', digest=base64.b64encode(digest).decode('utf-8'), signature=base64_signature)

# Print the PlayReady license
print(license)
