import os
import sys
from anthropic import Anthropic
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

console = Console()

class CodingAssistant:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            console.print("[red]Error: ANTHROPIC_API_KEY environment variable not found.[/red]")
            console.print("Please create a .env file with your API key or export it.")
            sys.exit(1)
            
        self.client = Anthropic(api_key=api_key)
        self.system_prompt = (
            "You are an expert software engineer and coding assistant. "
            "Provide concise, accurate, and idiomatic code solutions. "
            "Always explain the 'why' behind your technical choices briefly. "
            "Format all code blocks clearly."
        )
        self.messages = []

    def chat_loop(self):
        console.print("[bold green]Welcome to the AI Coding Assistant (powered by Claude)[/bold green]")
        console.print("Type 'exit' or 'quit' to end the session.\n")
        
        while True:
            try:
                user_input = Prompt.ask("[bold blue]You[/bold blue]")
                if user_input.lower() in ['exit', 'quit']:
                    console.print("[yellow]Goodbye![/yellow]")
                    break
                    
                if not user_input.strip():
                    continue

                self.messages.append({"role": "user", "content": user_input})
                
                with console.status("[bold cyan]Claude is thinking...[/bold cyan]", spinner="dots"):
                    response = self.client.messages.create(
                        model="claude-3-haiku-20240307", # Fast and efficient model
                        max_tokens=2048,
                        system=self.system_prompt,
                        messages=self.messages
                    )
                
                assistant_reply = response.content[0].text
                self.messages.append({"role": "assistant", "content": assistant_reply})
                
                console.print("\n[bold purple]Assistant:[/bold purple]")
                console.print(Markdown(assistant_reply))
                console.print("\n" + "-"*50 + "\n")
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Session interrupted. Goodbye![/yellow]")
                break
            except Exception as e:
                console.print(f"[red]An error occurred: {str(e)}[/red]")

if __name__ == "__main__":
    assistant = CodingAssistant()
    assistant.chat_loop()
