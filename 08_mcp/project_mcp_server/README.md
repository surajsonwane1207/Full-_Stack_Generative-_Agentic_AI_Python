# Project: Model Context Protocol (MCP) Server

This project demonstrates how to build a simple Model Context Protocol (MCP) Server in Python using `fastmcp`.

## What is MCP?
The Model Context Protocol is an open standard introduced by Anthropic that allows AI models (like Claude) to securely connect to local or remote tools and data sources. 

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

This server is designed to run over `stdio` (Standard Input/Output), which is how desktop clients like Claude Desktop or the Cursor IDE communicate with it.

To run it standalone in the terminal:
```bash
python mcp_server.py
```
*(Note: It will wait for JSON-RPC messages on stdin, so it will appear to just hang).*

### Connecting to Claude Desktop
To add this to Claude Desktop, edit your `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "system_stats": {
      "command": "python",
      "args": [
        "/absolute/path/to/08_mcp/project_mcp_server/mcp_server.py"
      ]
    }
  }
}
```

Once configured, you can open Claude Desktop and ask: 
*"What is the current system time from the MCP server?"* or *"How many CPU cores do I have?"*
