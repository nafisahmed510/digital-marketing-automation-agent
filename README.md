# Instagram Automation for Kortix

A Python implementation of Instagram automation tools migrated from Riona's TypeScript/Puppeteer codebase for integration with the Kortix AI agent platform.

## Overview

This project extracts the core Instagram automation functionality from the Riona AI Agent and rebuilds it as a native Python tool using Playwright for browser automation. The tool is designed to run within Kortix's Docker-based Agent Runtime.

## Features

- **Instagram Login**: Credential-based login with cookie persistence
- **Direct Messaging**: Send messages with optional media attachments
- **Post Interaction**: Like posts and generate AI-powered comments
- **Follower Scraping**: Extract follower information from target accounts
- **Session Management**: Cookie-based session persistence

## Technology Stack

- **Python 3.11**: Core programming language
- **Playwright**: Modern browser automation library
- **Docker**: Containerization for Kortix integration
- **Async/Await**: Asynchronous programming patterns

## Project Structure

```
instagram-automation-python/
├── instagram_tool.py          # Main Instagram automation class
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Containerization setup
└── kortix_integration_template.py  # Kortix tool integration template
```

## Getting Started

### Prerequisites

- Python 3.11+
- Docker
- Playwright browsers

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
playwright install chromium
```

2. Set environment variables:
```bash
export IG_USERNAME=your_instagram_username
export IG_PASSWORD=your_instagram_password
```

### Usage

```python
from instagram_tool import InstagramAutomationTool
import asyncio

async def main():
    tool = InstagramAutomationTool()
    await tool.init()
    
    # Send a direct message
    await tool.send_direct_message("username", "Hello from Kortix!")
    
    await tool.close()

asyncio.run(main())
```

## Kortix Integration

The tool includes a Kortix integration template (`kortix_integration_template.py`) that demonstrates how to wrap the Instagram automation functionality as a Kortix custom tool with proper OpenAPI schemas and error handling.

## License

This project is part of the migration from Riona AI Agent to Kortix platform.