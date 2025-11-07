# The Pitch Visualizer

**Transform any story into a stunning visual storyboard — instantly.**

An AI-powered web app that converts narrative text into a **multi-panel visual storyboard** using **DALL·E 3** (or free image fallbacks). Perfect for pitches, storytelling, marketing, and creative writing.

---

## Live Demo

Run locally:  
→ **http://localhost:5001** (auto-assigned free port)

> No API key? No problem — beautiful **Unsplash placeholder images** appear instantly.

---

## Features

| Feature | Description |
|-------|-----------|
| **Text to Storyboard** | Paste 3+ sentences → auto-split into 3–6 scenes |
| **AI Image Generation** | Uses OpenAI DALL·E 3 for photorealistic or artistic images |
| **Free Fallback** | If no API key or billing limit → uses **Unsplash** (no cost) |
| **7 Visual Styles** | Digital Art, Photorealistic, Watercolor, Comic, Minimalist, etc. |
| **Prompt Preview** | Click "View AI Prompt" to see the exact DALL·E prompt |
| **Responsive Design** | Works on mobile, tablet, and desktop |
| **No Port Conflicts** | Auto-detects free port (5000, 5001, etc.) |
| **Secure** | `.env` file ignored via `.gitignore` |

---

## Screenshots

<div align="center">

  <img src="https://via.placeholder.com/800x500/764ba2/ffffff?text=Generated+Storyboard" alt="Output" width="48%" />
</div>

*Example: A tiny terrier vs. a fluffy cat → 4-panel comic-style storyboard*

---

## How It Works

1. **Text Segmentation** → NLTK splits narrative into logical scenes
2. **Prompt Engineering** → Keywords enhanced with visual descriptors
3. **Image Generation** → DALL·E 3 (or Unsplash fallback)
4. **Render Storyboard** → Responsive grid with captions and prompts

---


## Setup Instructions

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository
```bash
git clone <your-repo-url>
cd pitch-visualizer
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure API key
```bash
cp  .env
# Edit .env and add your OpenAI API key
```

5. Run the application
```bash
python app.py
```

6. Open browser to `http://localhost:5000`



## License
MIT
