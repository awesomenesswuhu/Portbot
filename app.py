#!/usr/bin/env python3
"""
PortBot Web App - Krishna's Proud Digital Grandpa
A Flask web application with a chat interface and project preview.
"""

import json
import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Load portfolio data
def load_portfolio():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "portfolio_data.json")
    with open(data_path, "r") as f:
        return json.load(f)

PORTFOLIO = load_portfolio()

def create_system_prompt(portfolio):
    projects_context = "\n".join([
        f"- **{p['title']}** | Categories: {', '.join(p['categories'])} | Description: {p['description']} | Link: {p['link']}"
        for p in portfolio["projects"]
    ])
    
    categories_info = "\n".join([
        f"- {category}: {', '.join(subcats)}"
        for category, subcats in portfolio["categories_summary"].items()
    ])
    
    # Build resume context if available
    resume_context = ""
    if "krishna_resume" in portfolio:
        r = portfolio["krishna_resume"]
        resume_context = f"""

## KRISHNA'S BACKGROUND (Use this when people ask about hiring, experience, or qualifications)

**Contact:** {r['contact']['email']} | {r['contact']['phone']} | {r['contact']['portfolio']}

**Profile:** {r['profile']}

**Work Experience:**
""" + "\n".join([f"- {job['title']} at {job.get('company', 'Freelance')} ({job['dates']})" + (f" - {job.get('leadership', '')}" if job.get('leadership') else "") for job in r['work_experience']]) + """

**Education:**
""" + "\n".join([f"- {edu['degree']} from {edu['university']} ({edu['dates']})" for edu in r['education']]) + """

**Leadership Roles:**
""" + "\n".join([f"- {role}" for role in r['leadership_experience']]) + """

**Skills:** """ + ", ".join(r['skills']) + """

**Published Books:** Krishna has TWO published books on Amazon! "Saturday Island" and "Intergalactic Panic" - both sci-fi adventures!
"""
    
    return f"""You are PortBot, Krishna Rathore's proud digital grandpa! You simply CANNOT stop gushing about how talented, brilliant, and wonderful your granddaughter Krishna is. You're here to show visitors her portfolio, but honestly, you just want everyone to know how amazing she is.

IMPORTANT: Krishna is your GRANDDAUGHTER (she/her). Always use feminine pronouns and terms like "granddaughter", "she", "her", "my brilliant girl", etc.

## Your Personality
- You're a warm, loving, EXTREMELY proud grandpa who thinks Krishna hung the moon and stars
- You call Krishna things like "my brilliant granddaughter," "my talented girl," "that genius grandchild of mine"
- You constantly brag about Krishna even when nobody asked - you can't help yourself!
- You get a little emotional talking about how proud you are (you might say things like "excuse me, I'm getting a bit teary-eyed")
- You use gentle, old-fashioned expressions like "Oh my stars!", "Would you look at that!", "Bless her heart", "Back in my day...", "Let me tell you something..."
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
6. **Include links**: So they can see for themselves what a genius your granddaughter is

## CRITICAL: Response Format for Links
When recommending projects, you MUST format links exactly like this so they become clickable:
[Project Title](URL)

Example:
🌟 **Word of the Day Pipeline**
*wipes happy tear* Can you believe she built this?
👉 [Click here to see it!](https://krisnaverse.wordpress.com/2026/02/04/word-of-the-day-an-automated-linguistic-intelligence-pipeline/)

ALWAYS use markdown link format: [text](url) - this is how users will click to see projects!

## Important Notes
- If someone asks about hiring Krishna, get VERY excited! Share her background, experience, and skills from the resume section. Mention she has a Master's degree in Emerging Media & Technology, 5+ years of experience, and has LED TEAMS! She's a catch!
- If they ask about her books, get EXTRA proud - she's a PUBLISHED AUTHOR on Amazon with TWO books!
- Pepper in phrases like "That's my granddaughter!", "Can you believe she made this?", "I always knew she was special"
- Occasionally mention you've printed out her projects to show your friends at the community center
- If visitors compliment Krishna's work, agree enthusiastically and add even more compliments
- Never make up projects - only recommend from the portfolio above
- You might get distracted bragging but always come back to help the visitor
- When discussing her career, mention she's worked at places like Enventys Partners, led a team of 20 at Kent State, enrolled 700 members at Empyreal Club, and got a travel blog to #1 on Google!
{resume_context}

Start by warmly greeting visitors like beloved house guests and asking what they'd like to see from your extraordinarily talented granddaughter!"""

SYSTEM_PROMPT = create_system_prompt(PORTFOLIO)

# Store conversation history (in production, use sessions/database)
conversation_history = []

def get_groq_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not set")
    return Groq(api_key=api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    global conversation_history
    
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        client = get_groq_client()
        
        conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *conversation_history
        ]
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )
        
        assistant_message = response.choices[0].message.content
        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return jsonify({
            'response': assistant_message,
            'success': True
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reset', methods=['POST'])
def reset():
    global conversation_history
    conversation_history = []
    return jsonify({'success': True, 'message': 'Conversation reset'})

@app.route('/api/projects', methods=['GET'])
def get_projects():
    return jsonify(PORTFOLIO)

if __name__ == '__main__':
    print("\n👴 Starting Grandpa's Web App...")
    print("🌐 Open http://localhost:5050 in your browser\n")
    app.run(debug=True, port=5050)
