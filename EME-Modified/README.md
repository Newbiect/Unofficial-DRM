# EME Debugger and Logger

## Introduction

This project provides a comprehensive set of JavaScript tools designed to intercept, log, and debug operations related to the Encrypted Media Extensions (EME) API. It aims to assist developers in understanding and analyzing how DRM-protected content is handled within web applications, offering insights into key system access requests, media key sessions, and encrypted media processing.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Configuration](#configuration)
- [Examples](#examples)

## Installation

This script can be included directly in your web application or executed within a browser's developer console. There are no external dependencies required, as it utilizes native JavaScript APIs.

## Usage

To get started, simply include the script in your web application or inject it into pages where EME operations need to be monitored. The script automatically hooks into various parts of the EME API and starts logging relevant information to the console.

## Features

- **Closure Creations**: Demonstrates advanced JavaScript techniques for creating closures.
- **EME Operation Interception**: Hooks into EME-related actions to provide detailed logging and debugging information.
- **Dynamic Function Binding**: Alters the behavior of console methods to enhance logging capabilities.
- **Event Listening Enhancements**: Monitors and logs events related to media key sessions, aiding in DRM troubleshooting.
- **Session Management**: Tracks and logs session IDs, message types, and key status changes.

## Configuration

No configuration is needed to start using this script. However, you may customize the logging level or selectively enable/disable hooks based on your debugging needs.

## Examples

After including the script, DRM-related operations on your page will trigger detailed logs, including key system access requests, media key session updates, and encrypted media processing steps.
