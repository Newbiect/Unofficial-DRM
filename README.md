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
