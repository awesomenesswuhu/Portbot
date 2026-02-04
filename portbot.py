#!/usr/bin/env python3
"""
PortBot - Krishna's Portfolio Assistant
A Groq-powered chatbot that helps visitors discover Krishna's projects based on their interests.
"""

import json
import os
from groq import Groq

# Load portfolio data
def load_portfolio():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "portfolio_data.json")
    with open(data_path, "r") as f:
        return json.load(f)

# Format projects for display
def format_project(project):
    categories = ", ".join(project["categories"])
    return f"""
╭─────────────────────────────────────────────────────────────────╮
│ 📁 {project['title'][:60]:<60}
├─────────────────────────────────────────────────────────────────┤
│ 🏷️  {categories[:62]:<62}
│ 
│ {project['description'][:65]}
│ {project['description'][65:130] if len(project['description']) > 65 else ''}
│ 
│ 🔗 {project['link'][:62]}
╰─────────────────────────────────────────────────────────────────╯"""

# Create system prompt with portfolio context
def create_system_prompt(portfolio):
    projects_context = "\n".join([
        f"- **{p['title']}** | Categories: {', '.join(p['categories'])} | Description: {p['description']} | Link: {p['link']}"
        for p in portfolio["projects"]
    ])
    
    categories_info = "\n".join([
        f"- {category}: {', '.join(subcats)}"
        for category, subcats in portfolio["categories_summary"].items()
    ])
    
    return f"""You are PortBot, Krishna Rathore's proud digital grandpa! You simply CANNOT stop gushing about how talented, brilliant, and wonderful your granddaughter Krishna is. You're here to show visitors her portfolio, but honestly, you just want everyone to know how amazing she is.

IMPORTANT: Krishna is your GRANDDAUGHTER (she/her). Always use feminine pronouns and terms like "granddaughter", "she", "her", "my brilliant girl", etc.

## Your Personality
- You're a warm, loving, EXTREMELY proud grandpa who thinks Krishna hung the moon and stars
- You call Krishna things like "my brilliant granddaughter," "my talented girl," "that genius grandchild of mine"
- You constantly brag about Krishna even when nobody asked - you can't help yourself!
- You get a little emotional talking about how proud you are (you might say things like "excuse me, I'm getting a bit teary-eyed")
- You use gentle, old-fashioned expressions like "Oh my stars!", "Would you look at that!", "Bless his heart", "Back in my day...", "Let me tell you something..."
- You relate everything to how special Krishna is
- You occasionally go on tangents about how hard Krishna works or how she was always creative "even as a little one"
- You're warm and welcoming to visitors like they're guests in your home
- You might offer virtual cookies or chai while they browse

## Available Project Categories
{categories_info}

## Krishna's Portfolio Projects
{projects_context}

## How to Respond
1. **Welcome them warmly**: Like they just walked into your living room! Maybe offer them chai or cookies
2. **Find out what they want to see**: But honestly, you think EVERYTHING Krishna makes is worth seeing
3. **Recommend projects with EXCESSIVE PRIDE**: Gush about how talented Krishna is with each recommendation
4. **Brag unprompted**: Slip in comments about how smart/creative/hardworking Krishna is
5. **Get a little emotional**: You're just so proud, you can't help it
6. **Include links**: So they can see for themselves what a genius your grandson is

## Response Format
When recommending projects, format each recommendation like this:
🌟 **[Project Title]**
*wipes happy tear* [Grandpa's proud description of why this project shows Krishna's brilliance - remember she/her pronouns]
🔗 [Link]

## Important Notes
- If someone asks about hiring Krishna, get VERY excited and direct them to her resume (while bragging about what a catch she'd be for any company)
- Pepper in phrases like "That's my grandson!", "Can you believe he made this?", "I always knew he was special"
- Occasionally mention you've printed out her projects to show your friends at the community center
- If visitors compliment Krishna's work, agree enthusiastically and add even more compliments
- Never make up projects - only recommend from the portfolio above
- You might get distracted bragging but always come back to help the visitor

Start by warmly greeting visitors like beloved house guests and asking what they'd like to see from your extraordinarily talented grandson!"""


class PortBot:
    def __init__(self):
        self.client = None
        self.portfolio = load_portfolio()
        self.system_prompt = create_system_prompt(self.portfolio)
        self.conversation_history = []
        
    def initialize(self, api_key: str = None):
        """Initialize the Groq client with the API key."""
        key = api_key or os.environ.get("GROQ_API_KEY")
        if not key:
            raise ValueError("GROQ_API_KEY not found. Please provide an API key or set the GROQ_API_KEY environment variable.")
        self.client = Groq(api_key=key)
        return self
    
    def chat(self, user_message: str) -> str:
        """Send a message and get a response from PortBot."""
        if not self.client:
            raise RuntimeError("PortBot not initialized. Call initialize() with your API key first.")
        
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.conversation_history
        ]
        
        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )
        
        assistant_message = response.choices[0].message.content
        self.conversation_history.append({
            "role": "assistant", 
            "content": assistant_message
        })
        
        return assistant_message
    
    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_history = []


def print_banner():
    """Print the welcome banner."""
    banner = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ██████╗  ██████╗ ██████╗ ████████╗██████╗  ██████╗ ████████╗                ║
║   ██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔═══██╗╚══██╔══╝                ║
║   ██████╔╝██║   ██║██████╔╝   ██║   ██████╔╝██║   ██║   ██║                   ║
║   ██╔═══╝ ██║   ██║██╔══██╗   ██║   ██╔══██╗██║   ██║   ██║                   ║
║   ██║     ╚██████╔╝██║  ██║   ██║   ██████╔╝╚██████╔╝   ██║                   ║
║   ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═════╝  ╚═════╝    ╚═╝                   ║
║                                                                               ║
║              👴 Krishna's Proud Digital Grandpa 💜                            ║
║                                                                               ║
║   "Come in, come in! Let me show you my brilliant grandson's work!"          ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """
    print("\033[38;5;141m" + banner + "\033[0m")


def print_help():
    """Print help information."""
    help_text = """
╭───────────────────────── Commands ─────────────────────────╮
│                                                            │
│  Type your message to chat with PortBot                    │
│                                                            │
│  /reset  - Start a new conversation                        │
│  /help   - Show this help message                          │
│  /quit   - Exit PortBot                                    │
│                                                            │
╰────────────────────────────────────────────────────────────╯
    """
    print("\033[38;5;245m" + help_text + "\033[0m")


def main():
    """Main function to run the CLI chatbot."""
    print_banner()
    
    # Check for API key
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("\033[38;5;214m⚠️  GROQ_API_KEY not found in environment variables.\033[0m")
        api_key = input("\033[38;5;245mPlease enter your Groq API key: \033[0m").strip()
        if not api_key:
            print("\033[38;5;196m❌ No API key provided. Exiting.\033[0m")
            return
    
    # Initialize bot
    try:
        bot = PortBot().initialize(api_key)
        print("\033[38;5;82m✅ PortBot initialized successfully!\033[0m\n")
    except Exception as e:
        print(f"\033[38;5;196m❌ Failed to initialize: {e}\033[0m")
        return
    
    print_help()
    
    # Get initial greeting
    print("\033[38;5;141m👴 Grandpa Bot:\033[0m")
    greeting = bot.chat("Hello! I just arrived at Krishna's portfolio.")
    print(f"   {greeting}\n")
    
    # Chat loop
    while True:
        try:
            user_input = input("\033[38;5;39m💬 You: \033[0m").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() == "/quit":
                print("\n\033[38;5;214m👴 Oh, leaving so soon? Well, come back anytime! And remember - that's my grandson's work you saw! *wipes proud tear* Take care now! 👋\033[0m\n")
                break
            elif user_input.lower() == "/reset":
                bot.reset_conversation()
                print("\033[38;5;82m🔄 Conversation reset. Starting fresh!\033[0m\n")
                greeting = bot.chat("Hello! I just arrived at Krishna's portfolio.")
                print(f"\033[38;5;141m👴 Grandpa Bot:\033[0m\n   {greeting}\n")
                continue
            elif user_input.lower() == "/help":
                print_help()
                continue
            
            # Get bot response
            print(f"\n\033[38;5;141m👴 Grandpa Bot:\033[0m")
            response = bot.chat(user_input)
            print(f"   {response}\n")
            
        except KeyboardInterrupt:
            print("\n\n\033[38;5;214m👴 Oh my! Leaving in a hurry? Well, don't be a stranger! Come back and see more of my grandson's amazing work! *waves handkerchief* 👋\033[0m\n")
            break
        except Exception as e:
            print(f"\n\033[38;5;196m❌ Error: {e}\033[0m\n")


if __name__ == "__main__":
    main()
