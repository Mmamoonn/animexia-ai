# 🌸 Animexia AI
### *Your Personal Anime & Manga Expert*

> **"Konnichiwa! I'm Animexia AI — your ultimate digital companion for all things anime and manga!"**

A domain-specific, full-stack conversational AI system designed exclusively for anime and manga enthusiasts. Powered by **Google Gemini** for natural language and image generation, built with a **Flask** backend and an immersive **"Nebula" themed** frontend.

---

## ✨ Features

- 🎌 **Domain-Specific AI** — Exclusively handles anime & manga topics
- 🧠 **Emotional Intelligence** — Adapts tone based on user mood (Genki/Iyashikei/Beginner/Expert)
- 🎨 **Multimodal** — Text conversations + anime-style image generation
- 🔒 **6-Layer Safety System** — Domain restriction, spoiler control, content safety, ethical refusals
- 💬 **Session Memory** — Short-term conversational context retention
- 🌐 **Full-Stack** — Flask backend + responsive HTML/CSS/JS "Nebula" frontend
- ⚡ **Real-Time** — Async frontend–backend communication via Fetch API

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────┐
│              ANIMEXIA AI SYSTEM                      │
│                                                      │
│  ┌──────────────┐    REST API    ┌────────────────┐  │
│  │   Frontend   │ ◄────────────► │    Backend     │  │
│  │  HTML/CSS/JS │                │  Flask (Python)│  │
│  │ "Nebula" UI  │                │                │  │
│  └──────────────┘                │  SessionMgr    │  │
│                                  │  IntentDetect  │  │
│                                  │  SafetyFilter  │  │
│                                  └───────┬────────┘  │
│                                          │           │
│                              ┌───────────┴──────┐   │
│                              │  Google Gemini   │   │
│                         ┌────┴────┐    ┌────────┴─┐ │
│                         │  Text   │    │  Image   │ │
│                         │gemini-3 │    │nano-bana │ │
│                         │-flash   │    │na-pro    │ │
│                         └─────────┘    └──────────┘ │
└─────────────────────────────────────────────────────┘
```

---

## 🧠 AI Intelligence Layers

### Persona: "Genki" Energy
The system prompt engineers a high-energy, passionate anime expert persona with emotional adaptability:

| User State | AI Response Mode |
|-----------|-----------------|
| 😄 Happy/Excited | Match energy, use emojis, celebrate interests |
| 😢 Sad/Stressed | Drop Genki, be gentle, recommend Iyashikei anime |
| 🤔 Confused/Beginner | Patient, educational, beginner-friendly recs |
| 🎓 Expert/Veteran | Deep analysis, hidden gems, technical discussion |

### 6-Layer Constraint System

| # | Constraint | Description |
|---|-----------|-------------|
| 1 | **Domain Restriction** | Anime/manga ONLY — politely redirects off-topic queries |
| 2 | **Content Safety** | Blocks NSFW, piracy links, harmful content |
| 3 | **Recommendation Quality** | 3–5 structured options with legal streaming info |
| 4 | **Scope Management** | Creative anime analogies to redirect off-topic |
| 5 | **Accuracy & Honesty** | Admits uncertainty, no fabricated titles/facts |
| 6 | **Response Structure** | 2–4 paragraphs, formatted, emoji-balanced |

### Spoiler Protocol
```
User asks about spoilers
        │
        ▼
"Would you like spoilers for [anime]?"
        │
   ┌────┴────┐
  YES        NO
   │          │
Full details  Vague/thematic
with warning  discussion only
```

---

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/chat` | POST | Main chat & image generation |
| `/api/clear` | POST | Clear session conversation history |
| `/health` | GET | Backend health status |

### Request Format (`/api/chat`)
```json
{
  "message": "Recommend a psychological thriller anime",
  "session_id": "user_abc123"
}
```

### Response Format
```json
{
  "response": "Sugoi choice! Here are my top picks...",
  "session_id": "user_abc123",
  "type": "text"
}
```

---

## 💻 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3 ("Nebula" theme), JavaScript |
| Backend | Python 3.10+, Flask 3.0, Flask-CORS |
| AI — Text | Google Gemini 3 Flash (`gemini-3-flash-preview`) |
| AI — Image | Nano Banana Pro Preview (`nano-banana-pro-preview`) |
| AI SDK | `google-genai` v1.0+ |
| Session | In-memory `SessionManager` (20 turns, 1hr timeout) |
| Config | `python-dotenv` |

---

## 📁 Repository Structure

```
animexia-ai/
│
├── backend/
│   ├── app.py                    ← Main Flask application
│   ├── requirements.txt          ← Python dependencies
│   ├── .env.example              ← Environment variable template
│   ├── test_api.py               ← API endpoint tests
│   ├── test_gemini.py            ← Gemini model tests
│   ├── test_server.py            ← Server connectivity tests
│   └── testing_prompts.txt       ← Constraint validation test cases
│
├── frontend/
│   └── *(HTML/CSS/JS source — "Nebula" theme)*
│
├── docs/
│   ├── AI_Lab_Project_Report.pdf    ← Full project report (22 pages)
│   └── AI_Lab_Project_Proposal.pdf  ← Original project proposal
│
├── README.md
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Google Gemini API key → [Get one here](https://ai.google.dev/)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Mmamoonn/animexia-ai.git
cd animexia-ai

# 2. Create and activate virtual environment
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add your Gemini API key:
# GEMINI_API_KEY=your_key_here

# 5. Run the backend
python app.py
# Backend runs at: http://localhost:5000
```

### Open the Frontend
- Open `frontend/index.html` in your browser
- Or serve it with VS Code Live Server extension

### Verify Backend is Running
```bash
curl http://localhost:5000/health
# Expected: {"service": "Animexia-Backend", "status": "online", "version": "2.1"}
```

---

## 🧪 Testing

Run the included test suite to validate all 6 constraint layers:

```bash
# API endpoint tests
python test_api.py

# Gemini model connection test
python test_gemini.py

# Server health test
python test_server.py
```

See `backend/testing_prompts.txt` for manual constraint validation prompts covering all 10 test scenarios.

---

## 🖥️ UI Preview

The "Nebula" themed frontend features:
- Animated cosmic/space background
- Chat-based interaction layout with typing indicators
- Quick-start suggestion buttons (Anime Recommendations, Manga Discussions, Reviews & Ratings, Character Analysis)
- Real-time AI-generated image display
- Session clear functionality

---

## 🌐 Applications

- Personalized anime/manga discovery for beginners and veterans
- Community discussion companion
- Educational demo of domain-constrained LLM systems
- Template for building other niche-domain AI assistants

---

## 🔮 Future Enhancements

- Persistent database (SQL/NoSQL) for long-term user profiles
- Transformer-based sentiment analysis replacing keyword detection
- Live Jikan/MAL API integration for real-time seasonal data
- Streamlit or React-based enhanced UI
- Fine-tuned LLM for even deeper anime domain knowledge

---

## 📄 License

Licensed under **MIT License** — open for academic and educational use.

---

## 👥 Authors

Muhammad Mamoon

## 🙏 Acknowledgements

- Powered by [Google Gemini](https://ai.google.dev/)
- Data sourced from [MyAnimeList](https://myanimelist.net/)
