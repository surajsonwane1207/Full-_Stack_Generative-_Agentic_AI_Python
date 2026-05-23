# Project: CLI Coding Assistant

A beautiful, terminal-based AI coding assistant powered by Anthropic's Claude 3. It features rich Markdown rendering, syntax highlighting, and conversation history.

## Prerequisites
- An API key from Anthropic.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file in this directory and add your API key:
   ```env
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

## Usage

Run the assistant from the terminal:
```bash
python assistant.py
```

- Type your coding questions or paste code for review.
- The assistant maintains context of the conversation.
- Type `exit` or `quit` to end the session.

## Architecture
- **Anthropic Python SDK**: Handles API communication with Claude.
- **Rich**: Provides beautiful terminal output, loading spinners, and markdown/syntax highlighting.
- **Conversation State**: The `CodingAssistant` class maintains a `messages` list to keep track of the chat history, enabling multi-turn conversations.
