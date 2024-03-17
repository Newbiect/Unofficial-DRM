# Widevine License Server Simulator

## Introduction

This project provides a Python-based simulator for generating Widevine license requests and responses. It demonstrates the process of encrypting a license payload, generating a license challenge, and creating a signed license response using RSA digital signatures. This tool can be useful for testing DRM implementations in media applications that rely on Widevine for content protection.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)
- [License](#license)

## Installation

To use this simulator, you need Python 3.6 or later and the `pycryptodome` package. Install the dependencies with:

```bash
pip install pycryptodome
```

## Usage

Run the script directly in your Python environment. Ensure all required parameters (`provider`, `content_id`, `policy_id`, etc.) are correctly set in the script before execution.

## Features

- Generation of encrypted license payloads using AES in CTR mode.
- RSA key pair generation for digital signatures.
- Creation of Widevine license challenges and responses.
- Support for custom Widevine license server URL and device properties configuration.

## Dependencies

- Python 3.6+
- Pycryptodome

## Configuration

Before running the script, you should configure the license payload and key system parameters according to your specific requirements. These include setting the appropriate content ID, policy ID, device brand, model, OS version, and manufacturer details.

## Examples

The script provided demonstrates a complete workflow for creating a Widevine license challenge and response. You can customize the `license_payload` and `key_system` dictionaries with your specific values to simulate different scenarios.

## Troubleshooting

Ensure that all dependencies are installed and that Python 3.6 or newer is being used. If you encounter any issues with encryption or RSA signing, verify that the `pycryptodome` library is correctly installed and up to date.

## Contributors

- [Pari Malam] - Initial work
Feel free to contribute to this project by submitting pull requests or reporting issues.
Join our Telegram channel to stay updated with the latest news, discussions, and announcements related to W1Devine. Click [here](https://t.me/w1devine) to join.

## Community Guidelines

1. Be respectful and considerate towards others.
2. Keep discussions relevant to W1Devine and Widevine DRM.
3. Avoid spamming or posting irrelevant content.
4. Respect the privacy of others and avoid sharing personal information.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## A typical WidevineCdm setup for Windows x64 will contain the following files:

- manifest.json
- widevinecdm.dll
- widevinecdmadapter.dll

## Common System ID

```
UUID                                    DRM System                          Additional Information
--------------------------------------------------------------------------------------------------------------
6dd8b3c3-45f4-4a68-bf3a-64168d01a4a6   ABV DRM (MoDRM)                    For further information please contact ABV International Pte Ltd. Documentation is available under NDA. ABV Content Protection for MPEG DASH (MoDRM v4.7 and above).
f239e769-efa3-4850-9c16-a903c6932efb   Adobe Primetime DRM version 4      For further information please contact Adobe.
616c7469-6361-7374-2d50-726f74656374   Alticast                            For further information please contact Alticast. galtiprotect_drm@alticast.com.
94ce86fb-07ff-4f43-adb8-93d2fa968ca2   Apple FairPlay                      Content Protection System Identifier for Apple FairPlay Streaming.
279fe473-512c-48fe-ade8-d176fee6b40f   Arris Titanium                      For further information please contact multitrust.info@arris.com. Documentation is available under NDA. @value is specified in documentation related to a specific version of the product.
3d5e6d35-9b9a-41e8-b843-dd3c6e72c42c   ChinaDRM                            ChinaDRM is defined by China Radio and Television Film Industry Standard GY/T 277-2014. @value indicates ChinaDRM specific solution provided by various vendors.
3ea8778f-7742-4bf9-b18b-e834b2acbd47   Clear Key AES-128                   Identifier for HLS Clear Key encryption using CBC mode. This is to be used as an identifier when requesting key system information when using CPIX.
be58615b-19c4-4684-88b3-c8c57e99e957   Clear Key SAMPLE-AES                Identifier for HLS Clear Key encryption using CBCS mode. This is to be used as an identifier when requesting key system information when using CPIX.
e2719d58-a985-b3c9-781a-b030af78d30e   Clear Key DASH-IF                   This identifier is meant to be used to signal the availability of W3C Clear Key in the context of a DASH presentation.
644fe7b5-260f-4fad-949a-0762ffb054B4   CMLA (OMA DRM)                      A draft version of the CMLA Technical Specification which is in process with involved adopters is not published. It is planned to be chapter 18 of our CMLA Technical Specification upon completion and approval. Revisions of the CMLA Technical Specification become public upon CMLA approval. UUID will correlate to various related XML schema and PSSH components as well as elements of the content protection element relating to CMLA DASH mapping.
37c33258-7b99-4c7e-b15d-19af74482154   Commscope Titanium V3               Documentation available under NDA. @value is specified in documentation related to a specific version of the product. Contact multitrust.info@arris.com for further information.
45d481cb-8fe0-49c0-ada9-ab2d2455b2f2   CoreCrypt                           CoreTrust Content Protection for MPEG-DASH. For further information and specification please contact CoreTurst at mktall@coretrust.com.
dcf4e3e3-62f1-5818-7ba6-0a6fe33ff3dd   DigiCAP SmartXess                  For further information please contact DigiCAP. Documentation is available under NDA. DigiCAP SmartXess for DASH @value CA/DRM_NAME VERSION (CA 1.0, DRM+ 2.0)
35bf197b-530e-42d7-8b65-1b4bf415070f   DivX DRM Series 5                   Please contact DivX for specifications.
80a6be7e-1448-4c37-9e70-d5aebe04c8d2   Irdeto Content Protection          For further information please contact Irdeto. Documentation is available under NDA.
5e629af5-38da-4063-8977-97ffbd9902d4   Marlin Adaptive Streaming Simple Profile V1.0     Details of what can be further specified within the ContentProtection element is in the specifications.
9a04f079-9840-4286-ab92-e65be0885f95   Microsoft PlayReady                 For further information please contact Microsoft.
6a99532d-869f-5922-9a91-113ab7b1e2f3   MobiTV DRM                          Identifier for any version of MobiDRM (MobiTV DRM). The version is signaled in the pssh box.
adb41c24-2dbf-4a6d-958b-4457c0d27b95   Nagra MediaAccess PRM 3.0           It identifies Nagra MediaAccess PRM 3.0 and above. Documentation is available under NDA.
1f83e1e8-6ee9-4f0d-ba2f-5ec4e3ed1a66   SecureMedia                         Documentation is available under NDA. @value shall be Arris SecureMedia version XXXXXXX. XXXXXX is specified in documentation associated with a particular version of the product. The UUID will be made available in SecureMedia documentation shared with a partner or customer of SecureMedia Arris.
992c46e6-c437-4899-b6a0-50fa91ad0e39   SecureMedia SteelKnot               Documentation is available under NDA. @value shall be Arris SecureMedia SteelKnot version XXXXXXX. The exact length and syntax of XXXXXXX is specified in documentation associated with a particular version of the product. The UUID will be made available in SecureMedia SteelKnot documentation shared with a partner or customer of SecureMedia SteelKnot.
a68129d3-575b-4f1a-9cba-3223846cf7c3   Synamedia/Cisco/NDS VideoGuard DRM  Documentation is available under NDA.
aa11967f-cc01-4a4a-8e99-c5d3dddfea2d   Unitend DRM (UDRM)                  For further information please contact y.ren@unitend.com.
9a27dd82-fde2-4725-8cbc-4234aa06ec09   Verimatrix VCAS                     @value is Verimatrix VCAS for DASH ViewRightWeb VV.vv (VV.vv is the version number). If used this can help the client to determine if the current DRM client can play the content.
b4413586-c58c-ffb0-94a5-d4896c1af6c3   Viaccess-Orca DRM (VODRM)           For further information please contact Viaccess-Orca. VODRM documentation is available under NDA.
793b7956-9f94-4946-a942-23e7ef7e44b4   VisionCrypt                         For further information please contact gosdrm@gospell.com.
1077efec-c0b2-4d02-ace3-3c1e52e2fb4b   W3C Common PSSH box                 This identifier is to be used as the SystemID for the Common PSSH box format defined by W3C as a preferred alternative to DRM system specific PSSH box formats. This identifier may be used in PSSH boxes and MPEG-DASH ContentProtection elements.
edef8ba9-79d6-4ace-a3c8-27dcd51d21ed   Widevine Content Protection         For further information please contact Widevine.
```
## Requests Structure Payload (Example)

```
{
  "original_headers": {
    "host": "127.0.0.1:8000",
    "user-agent": "curl/7.68.0",
    "accept": "*/*",
    "x-project": "[project]",
    "content-length": "8346",
    "content-type": "application/x-www-form-urlencoded",
    "expect": "100-continue",
    "X-Project": "[project]",
    "QUERY_ARGS": "arg1=val1&arg2=val2"
  },
  "key_data": [
    {
      "track_type": "UHD",
      "content_id": "ZXhwNTY=",
      "key_id": "SBBgssxKQlisxKCRJtBGfw=="
    }
  ],
  "parse_only_data": {
    "status": "OK",
    "status_message": "",
    "license_metadata": {
      "content_id": "ZXhwNTY=",
      "license_type": "STREAMING",
      "request_type": "NEW"
    },
    "supported_tracks": [
      {
        "type": "UHD1",
        "key_id": "qUSciifJUaCcliHbl3zY5w=="
      },
      {
        "type": "HD",
        "key_id": "Ex6k7P0WUACFcnLoPcZRAg=="
      },
      {
        "type": "SD",
        "key_id": "5o+8VuETV8SEbxEAUtiImA=="
      },
      {
        "type": "AUDIO",
        "key_id": "YzEzHAB4WL+bxXpSRzLKKA=="
      }
    ],
    "make": "Google",
    "model": "ChromeCDM-Linux-x64-4",
    "security_level": 3,
    "internal_status": 0,
    "session_state": {
      "license_id": {
        "request_id": "YAbdFo8FyLr2PYTSdv5/0Q==",
        "session_id": "YAbdFo8FyLr2PYTSdv5/0Q==",
        "purchase_id": "",
        "type": "STREAMING",
        "version": 0,
        "original_rental_duration_seconds": 0,
        "original_playback_duration_seconds": 0,
        "original_start_time_seconds": 1623862478
      },
      "signing_key": "Pjod4jIVOdkTiu5SP2fRSyHiSDHk2JzmjneksAhR9mJo/QZ7KE5uqqg6mI6L/5kEc6q/U/99HMfeEvXb84Wesw==",
      "keybox_system_id": 20121,
      "license_counter": 0
    },
    "drm_cert_serial_number": "NjFhNTZjOTJjNzc0ZDBjMGRmNDViODMzZTQzOTFiYmEwYQ==",
    "device_whitelist_state": "DEVICE_NOT_WHITELISTED",
    "platform": "linux",
    "device_state": "RELEASED",
    "pssh_data": {
      "key_id": [
        "YjAyMjg3NTIwODdjMjM2YzU1YTQ0NTM0YWU3ZGE0MTQ="
      ],
      "content_id": "YmJi"
    },
    "client_max_hdcp_version": "HDCP_NONE",
    "client_info": [
      {
        "name": "architecture_name",
        "value": "x86-64"
      },
      {
        "name": "company_name",
        "value": "Google"
      },
      {
        "name": "model_name",
        "value": "ChromeCDM"
      },
      {
        "name": "platform_name",
        "value": "Linux"
      },
      {
        "name": "widevine_cdm_version",
        "value": "4.10.2209.0"
      }
    ],
    "signature_expiration_secs": 188559989,
    "platform_verification_status": "PLATFORM_UNVERIFIED",
    "content_owner": "***",
    "content_provider": "***",
    "system_id": 20121,
    "oem_crypto_api_version": 16,
    "resource_rating_tier": 0,
    "default_device_security_profiles": {
      "profile_name": [
        "minimum"
      ]
    },
    "service_version_info": {
      "license_sdk_version": "16.4.2 Built on Mar 29 2021 23:40:46 (1617086373)",
      "license_service_version": "widevine_license_wls_20210302_202486-RC04"
    }
  },
  "response_prototype": {
    "content_key_specs": [
      {
        "key_id": "SBBgssxKQlisxKCRJtBGfw==",
        "security_level": 1,
        "required_output_protection": {
          "hdcp": "HDCP_NONE",
          "disable_analog_output": false,
          "hdcp_srm_rule": "HDCP_SRM_RULE_NONE"
        }
      }
    ],
    "session_init": {
      "override_device_revocation": true
    },
    "use_policy_overrides_exclusively": true,
    "policy_overrides": {
      "license_duration_seconds": 0,
      "playback_duration_seconds": 0,
      "can_play": true,
      "can_persist": false,
      "can_renew": false
    },
    "allow_unverified_platform": true
  }
}
```

## Response (Example)
```
{
  "content_key_specs": [
    {
      "key_id": "SBBgssxKQlisxKCRJtBGfw==",
      "security_level": 3,
      "required_output_protection": {
        "hdcp": "HDCP_NONE",
        "disable_analog_output": false,
        "hdcp_srm_rule": "HDCP_SRM_RULE_NONE"
      }
    }
  ],
  "session_init": {
    "override_device_revocation": true
  },
  "use_policy_overrides_exclusively": true,
  "policy_overrides": {
    "license_duration_seconds": 3600,
    "playback_duration_seconds": 3600,
    "can_play": true,
    "can_persist": true,
    "can_renew": false
  },
  "allow_unverified_platform": true
}
```
