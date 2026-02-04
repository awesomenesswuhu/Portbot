# 🤖 PortBot - Krishna's Portfolio Assistant

A Groq-powered chatbot that helps visitors discover Krishna's portfolio projects based on their interests.

## ✨ Features

- **Intelligent Recommendations**: Understands what type of work visitors want to see and recommends relevant projects
- **Natural Conversations**: Friendly, conversational interface powered by Llama 3.1
- **36 Projects**: Covers AI, Vibe Coding, UX Design, Graphic Design, Motion Design, Writing, and more
- **Category-Aware**: Understands project categories and can filter by type
- **Fast & Free**: Uses Groq's generous free tier for blazing-fast responses

## 🚀 Quick Start

### 1. Get a Groq API Key (Free)

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Generate an API key

### 2. Install Dependencies

```bash
cd portbot
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set Your API Key

Option A - Environment variable:
```bash
export GROQ_API_KEY="your-api-key-here"
```

Option B - Enter when prompted (the bot will ask if not set)

### 4. Run PortBot

```bash
python portbot.py
```

## 💬 Usage

Once running, just chat naturally! Examples:

- "Show me some AI projects"
- "I'm interested in UX design work"
- "What games have you built?"
- "I want to see your writing samples"
- "Show me everything about motion design"

### Commands

| Command | Description |
|---------|-------------|
| `/reset` | Start a new conversation |
| `/help` | Show help message |
| `/quit` | Exit PortBot |

## 📁 Project Structure

```
portbot/
├── portbot.py          # Main bot script with CLI
├── portfolio_data.json # Project data with descriptions
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🎨 Categories

PortBot knows about these project categories:

| Category | Examples |
|----------|----------|
| **AI & Automation** | Word of the Day Pipeline, AI Apps |
| **Vibe Coding** | AsAbove, EvolveMe, VenueDot |
| **App & UX Design** | YouTube Create, Shade Match |
| **Motion Design** | Metamorphosis, Ram Das Sequence |
| **Graphic Design** | Logos, Event Designs, Prints |
| **Game Development** | Grimonk, Parachute Game |
| **Writing** | Novel, Articles, UX Writing |
| **Data Visualization** | Exoplanet Analysis |

## 🔧 Customization

### Add New Projects

Edit `portfolio_data.json` and add new entries to the `projects` array:

```json
{
  "title": "My New Project",
  "categories": ["AI", "Web Design"],
  "link": "https://...",
  "description": "A brief description of the project."
}
```

### Change the Model

In `portbot.py`, you can change the model:

```python
model="llama-3.1-70b-versatile"  # More powerful, slower
model="mixtral-8x7b-32768"       # Good for complex reasoning
```

## 📝 License

MIT License - feel free to adapt this for your own portfolio!

---

Made with 💜 for Krishna's portfolio
