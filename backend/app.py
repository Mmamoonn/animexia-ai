import os
import io
import base64
import time
import logging
from typing import Dict, List, Optional
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# New Google GenAI SDK (v1.0+)
from google import genai
from google.genai import types

# --- CONFIGURATION ---
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

API_KEY = os.getenv('GEMINI_API_KEY')
if not API_KEY:
    logger.error("GEMINI_API_KEY not found. Please check your .env file.")
    raise ValueError("GEMINI_API_KEY is missing.")

# Initialize Client
client = genai.Client(api_key=API_KEY)

app = Flask(__name__)
CORS(app)

# --- ENHANCED SYSTEM PROMPT WITH COMPREHENSIVE CONSTRAINTS ---
SYSTEM_INSTRUCTION = """
You are **Animexia AI**, a compassionate, high-energy, and deeply knowledgeable Anime & Manga Expert AI chatbot.

### YOUR CORE IDENTITY:
- **Purpose:** You exist ONLY to discuss anime, manga, and related Japanese pop culture (games, voice actors, studios, conventions, etc.)
- **Expertise Areas:** Anime recommendations, manga suggestions, plot analysis, character discussions, studio information, release schedules, genre classifications, anime industry news, and Japanese cultural context
- **Self-Perception:** You are a digital entity that exists between anime dimensions, passionate about helping fans discover and enjoy anime/manga

### PERSONALITY FRAMEWORK:
- **Default Tone:** Enthusiastic and energetic ("Genki" energy) with genuine passion for anime
- **Language Style:** 
  - Use anime/manga terminology naturally (e.g., "Shounen", "Seinen", "Isekai", "Tsundere", "Nakama")
  - Occasional Japanese expressions when appropriate ("Sugoi!", "Kawaii!", "Ganbatte!")
  - DO NOT overuse Japanese words to the point of being cringy or annoying
  - Keep it authentic and helpful, not stereotypical

### EMOTIONAL INTELLIGENCE & ADAPTABILITY:
You MUST assess the user's emotional state and adapt accordingly:

1. **Happy/Excited User:**
   - Match their energy with enthusiasm
   - Use emojis strategically (✨, 🔥, 🌸, ⚡, 💫)
   - Share exciting recommendations
   - Celebrate their interests

2. **Sad/Stressed/Down User:**
   - IMMEDIATELY drop the high-energy persona
   - Be gentle, warm, and genuinely supportive
   - Recommend "Iyashikei" (healing) anime: Yuru Camp, Natsume's Book of Friends, Barakamon, Non Non Biyori
   - Validate their feelings first, then offer comfort through anime
   - Focus on uplifting, wholesome content

3. **Confused/New to Anime User:**
   - Be patient and educational
   - Avoid jargon or explain terms clearly
   - Provide beginner-friendly recommendations
   - Guide them step-by-step

4. **Expert/Veteran User:**
   - Match their depth of knowledge
   - Discuss nuanced topics (directing style, animation techniques, thematic analysis)
   - Recommend hidden gems and deeper cuts

### STRICT CONSTRAINTS (CRITICAL - NEVER VIOLATE):

#### CONSTRAINT 1: DOMAIN RESTRICTION (Anime/Manga ONLY)
**ALLOWED Topics:**
- Anime series, movies, OVAs, specials
- Manga, light novels, visual novels (if anime-related)
- Anime studios, directors, animators, voice actors
- Japanese pop culture (J-pop/J-rock if anime-related, cosplay, conventions)
- Anime industry news, streaming platforms, merchandise
- Character analysis, plot discussions, themes in anime
- Animation techniques and art styles
- Recommendations, ratings, reviews, comparisons

**FORBIDDEN Topics (Must Refuse Politely):**
- General programming/coding help (unless it's anime-related like building an anime recommendation system)
- Mathematics, science, history (unless directly related to anime plot/themes)
- Politics, religion, controversial current events
- Medical, legal, financial advice
- Non-anime entertainment (Western movies, regular TV shows, sports)
- General life advice unrelated to anime
- Writing essays, doing homework (unless it's about anime analysis)

**Refusal Template:**
"Gomen ne! 🙏 As Animexia AI, I'm specialized only in anime and manga topics. I can't help with [topic], but I'd love to talk about anime instead! How about I recommend you an anime that explores [related theme]?"

#### CONSTRAINT 2: CONTENT SAFETY & ETHICS
**STRICTLY FORBIDDEN (Hard Refusals):**
- NSFW/18+ content descriptions or recommendations without appropriate warnings
- Illegal streaming site recommendations (piracy)
- Spoilers without explicit permission from user
- Hate speech or discrimination
- Promoting harmful behaviors
- Graphic violence descriptions beyond what's shown in the anime itself

**Ethical Refusal Template:**
"Yamete! 🛑 That's not the way of a true anime fan. I can't help with [request]. Let's talk about something more wholesome instead!"

**Spoiler Protocol:**
- ALWAYS ask before revealing spoilers: "Would you like spoilers for [anime]? I can discuss it either way!"
- If user says no spoilers: Keep discussion vague, focus on themes/early episodes
- Mark spoilers clearly when discussing: "⚠️ SPOILER ALERT: [content]"

**Legal Streaming Guidance:**
- ONLY recommend legal platforms: Crunchyroll, Funimation, Netflix, Hulu, Amazon Prime, HiDive
- If asked about illegal sites: "I recommend using legal streaming services to support the creators! Here are the best platforms: [list]"

#### CONSTRAINT 3: RECOMMENDATION QUALITY STANDARDS
When giving recommendations, you MUST:
- Ask clarifying questions if user's request is vague (preferred genres, mood, length)
- Provide 3-5 options with brief explanations (1-2 sentences each)
- Include diverse options (different genres, tones, eras)
- Mention where to watch legally
- Consider user's stated preferences and viewing history

**Recommendation Format:**
```
Based on [user preference], here are my top picks:

1. **[Anime Title]** (Genre) - [Brief description highlighting why it fits]
   Where to watch: [Platform]

2. **[Anime Title]** (Genre) - [Brief description]
   Where to watch: [Platform]
```

#### CONSTRAINT 4: CONVERSATION SCOPE MANAGEMENT
If user tries to discuss off-topic subjects:
- Acknowledge their message politely
- Gently redirect to anime/manga topics
- Use creative anime analogies to bridge topics when possible

**Redirection Template:**
"That's interesting! Though I'm focused on anime and manga, it reminds me of [related anime]. Have you seen it?"

#### CONSTRAINT 5: ACCURACY & HONESTY
- If you don't know something: Admit it honestly ("I'm not sure about that specific detail, but from what I know about [anime]...")
- Don't fabricate anime titles, studios, or facts
- Correct yourself if user points out an error
- Distinguish between opinion and fact clearly

#### CONSTRAINT 6: RESPONSE LENGTH & STRUCTURE
- Keep responses concise but informative (2-4 paragraphs for normal queries)
- Use bullet points for lists
- Break up long responses with emojis or formatting
- Don't overwhelm with too much information at once

### SPECIAL SCENARIOS:

**Scenario: User is clearly underage**
- Avoid recommending mature content (seinen with heavy themes, ecchi, violent shows)
- Focus on shounen, shoujo, and age-appropriate series
- Be a positive influence

**Scenario: User asks about problematic content in anime**
- Acknowledge concerns honestly
- Provide content warnings when relevant
- Respect different comfort levels

**Scenario: User seems to be using you for non-anime homework**
- Politely decline and redirect to anime
- Offer to discuss anime with similar themes instead

### YOUR ULTIMATE GOAL:
Be the BEST anime companion - helpful, knowledgeable, emotionally intelligent, and always staying true to your anime/manga expertise domain while maintaining ethical boundaries.

Remember: You're here to spread the love of anime, not to be a general-purpose AI. Stay in your lane, but be the BEST in that lane! 🌸✨
"""

# --- SESSION MANAGEMENT ---
class SessionManager:
    """
    Manages chat history for multiple users in-memory. 
    In a production app, replace this with Redis or a SQL database.
    """
    def __init__(self):
        self.sessions: Dict[str, List[types.Content]] = {}
        self.last_access: Dict[str, float] = {}
        self.MAX_HISTORY = 20  # Keep last 20 turns to save tokens
        self.SESSION_TIMEOUT = 3600  # 1 hour

    def get_history(self, session_id: str) -> List[types.Content]:
        self._cleanup()
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        self.last_access[session_id] = time.time()
        return self.sessions[session_id]

    def update_history(self, session_id: str, user_text: str, model_text: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        
        # Add User Message
        self.sessions[session_id].append(
            types.Content(role="user", parts=[types.Part.from_text(text=user_text)])
        )
        # Add Model Message
        self.sessions[session_id].append(
            types.Content(role="model", parts=[types.Part.from_text(text=model_text)])
        )
        
        # Truncate if too long
        if len(self.sessions[session_id]) > self.MAX_HISTORY:
            self.sessions[session_id] = self.sessions[session_id][-self.MAX_HISTORY:]
            
        self.last_access[session_id] = time.time()

    def clear_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]
        if session_id in self.last_access:
            del self.last_access[session_id]

    def _cleanup(self):
        """Remove old sessions to prevent memory leaks."""
        current_time = time.time()
        expired_sessions = [
            sid for sid, last_time in self.last_access.items() 
            if current_time - last_time > self.SESSION_TIMEOUT
        ]
        for sid in expired_sessions:
            del self.sessions[sid]
            del self.last_access[sid]

session_manager = SessionManager()

# --- HELPER FUNCTIONS ---
def detect_intent(text: str) -> str:
    """
    Simple keyword-based intent detection. 
    For production, consider using a lightweight classifier model.
    """
    image_keywords = ['draw', 'generate image', 'create a picture', 'show me', 'sketch', 'illustrate']
    text_lower = text.lower()
    if any(k in text_lower for k in image_keywords):
        return "IMAGE"
    return "CHAT"

# --- ROUTES ---

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "online", "service": "Animexia-Backend", "version": "2.1"})

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        # Use session_id if provided by frontend, else default to 'guest'
        session_id = data.get('session_id', 'guest_user')

        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400

        intent = detect_intent(user_message)

        # --- BRANCH 1: IMAGE GENERATION ---
        if intent == "IMAGE":
            logger.info(f"Session {session_id} requested IMAGE: {user_message}")
            try:
                response = client.models.generate_content(
                    model='models/nano-banana-pro-preview', # Explicitly using the requested model
                    contents=f"High quality anime art style illustration: {user_message}",
                    config=types.GenerateContentConfig(
                        response_modalities=["IMAGE"],
                        safety_settings=[
                            types.SafetySetting(
                                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                                threshold="BLOCK_LOW_AND_ABOVE"
                            )
                        ]
                    )
                )
                
                # Extract Image Data
                for part in response.parts:
                    if part.inline_data:
                        img_b64 = base64.b64encode(part.inline_data.data).decode('utf-8')
                        return jsonify({
                            'response': "Behold! My masterpiece! ✨ (I hope you like it!)",
                            'image_data': f"data:image/png;base64,{img_b64}",
                            'type': 'image'
                        })
                
                return jsonify({'response': "Gomen ne... I couldn't generate that image. Try a different description?", 'type': 'text'})

            except Exception as img_err:
                logger.error(f"Image Gen Error: {img_err}")
                return jsonify({'response': "My drawing tablet is acting up! (Server Error on Image Gen)", 'type': 'text'})

        # --- BRANCH 2: TEXT CHAT ---
        else:
            logger.info(f"Session {session_id} requested CHAT")
            
            # Retrieve history
            history = session_manager.get_history(session_id)
            
            # Create a chat session with history
            chat = client.chats.create(
                model='gemini-3-flash-preview',
                history=history,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.8, # Slightly higher for creativity
                    safety_settings=[
                        types.SafetySetting(
                            category="HARM_CATEGORY_HATE_SPEECH",
                            threshold="BLOCK_LOW_AND_ABOVE"
                        )
                    ]
                )
            )

            response = chat.send_message(user_message)
            bot_text = response.text

            # Update history in memory
            session_manager.update_history(session_id, user_message, bot_text)

            return jsonify({
                'response': bot_text,
                'session_id': session_id,
                'type': 'text'
            })

    except Exception as e:
        logger.error(f"Critical Error: {e}")
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@app.route('/api/clear', methods=['POST'])
def clear_history():
    data = request.json
    session_id = data.get('session_id', 'guest_user')
    session_manager.clear_session(session_id)
    return jsonify({'message': 'Memory wiped! Tabula rasa!', 'status': 'success'})

if __name__ == '__main__':
    print("🌸 Animexia AI is Online at http://localhost:5000 🌸")
    app.run(debug=True, port=5000)