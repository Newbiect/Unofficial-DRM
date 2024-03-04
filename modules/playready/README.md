# PlayReady License Generator

## Introduction

This Python script automates the generation of a PlayReady license response. It includes creating a RSA key pair, signing the license template, and embedding the signature within the XML response. This tool is useful for testing and development purposes in scenarios where PlayReady DRM is used for content protection.

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

This script requires Python 3.6 or later with the `pycryptodome` package. To install the necessary dependency, run:

```bash
pip install pycryptodome
```

## Usage

To generate a PlayReady license, simply run the script. Make sure to replace placeholder values such as `{key_id}` and `{template_id}` with actual values relevant to your implementation.

## Features

- RSA key pair generation for digital signatures.
- Generation of a signed PlayReady license response in XML format.
- SHA256 hashing for digital signature generation.

## Dependencies

- Python 3.6+
- Pycryptodome

## Configuration

The script includes placeholder values that need to be replaced with actual data specific to your DRM setup, such as `key-id` and `template-id`. Additionally, you may need to adjust the XML structure based on your specific PlayReady license response requirements.

## Examples

The provided script is a complete example of how to generate a signed PlayReady license. You can modify the `license_template` string to fit the structure required by your application or DRM system.

## Troubleshooting

Ensure that Python and Pycryptodome are correctly installed and up to date. If you encounter issues with the RSA signing process, verify that your Python environment is correctly set up and that you are using compatible versions of the libraries.

## Contributors

- [Pari Malam] - Initial work

Feel free to contribute to the development of this tool by submitting pull requests or reporting bugs and issues.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
