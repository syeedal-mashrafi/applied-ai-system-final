# 🎵 RAG Music Recommender — Applied AI System (Project 4)

## Base Project
**Project 3: Music Recommender Simulation**
The original system used content-based filtering to score songs by genre, mood, and energy level using a CSV dataset. It had no AI generation and no knowledge retrieval.

## What's New in Project 4
This version adds **Retrieval-Augmented Generation (RAG)**:
- A local music catalog acts as a knowledge base
- The system searches 3 sources before passing results to Claude
- Claude only recommends songs grounded in the database
- Input/output guardrails and logging added for reliability
- Agentic workflow with 4 observable reasoning steps
- Few-shot specialization for music therapist tone
- Full evaluation harness with pass/fail scoring

## Demo Walkthrough
[Watch the Loom video here](https://loom.com/share/db3cc2f6d0ac438d8906cba9b0d29899)

## System Architecture
See `assets/architecture_diagram.png`

## Setup Instructions
1. Clone this repo: `git clone https://github.com/syeedal-mashrafi/applied-ai-system-final`
2. Install dependencies: `pip install anthropic`
3. Set your API key: `$env:ANTHROPIC_API_KEY="your-key-here"`
4. Run the app: `python main.py`
5. Run the agent: `python agent.py`
6. Run tests: `python eval_harness.py`

## Sample Interactions

**Input:** "I'm feeling sad and heartbroken"
**Output:** Claude recommended "Someone Like You" by Adele and "Anti-Hero" by Taylor Swift with warm therapeutic explanations.

**Input:** "I want to focus and study"
**Output:** Claude recommended "Clair de Lune" by Debussy and "Lo-Fi Hip Hop Beats" based on calm focused mood tags.

**Input:** "" (empty)
**Output:** ⚠️ Input cannot be empty. (guardrail blocked it)

## Design Decisions
- Used keyword scoring instead of embeddings — simpler and more transparent
- Multi-source RAG pulls from catalog, expert notes, and genre metadata
- Logging added to app.log for every API call
- Input guardrails block empty, too-long, and banned inputs

## Testing Summary
8/9 automated tests passed. Overall score: 88.9%.
System is reliable for common moods.
Guardrails successfully blocked all invalid inputs.

## Reflection
This project taught me how RAG fundamentally changes AI reliability. Instead of hallucinating song titles, the AI is grounded in real data. Adding the agentic workflow showed me how breaking reasoning into steps makes AI decisions more transparent and trustworthy.

---

# 🎵 Music Recommender Simulation (Original Project 3)

## Project Summary

This project simulates a content-based music recommendation system. Given a user's taste profile (preferred genre, mood, and energy level), the system scores every song in a dataset and returns the top recommendations ranked by relevance. It works like a simplified version of what Spotify or TikTok do behind the scenes.

---

## How The System Works

### Real-World Context
Streaming platforms like Spotify and YouTube use two main approaches:
- **Collaborative Filtering**: Recommends based on what similar users liked
- **Content-Based Filtering**: Recommends based on the song's own attributes like genre, mood, and energy

This project uses **content-based filtering**.

### Algorithm Recipe
Each `Song` has: `genre`, `mood`, `energy` (0.0–1.0), `tempo_bpm`
Each `UserProfile` has: `favorite_genre`, `favorite_mood`, `target_energy`

**Scoring Rule:**
| Feature | Points | Condition |
|---|---|---|
| Genre | +2.0 | Exact match |
| Mood | +1.0 | Exact match |
| Energy | 0.0–1.0 | 1.0 - abs(song.energy - user.target_energy) |

Maximum possible score: **4.0 points**

**Data Flow:**
Input (User Prefs) → Score every song → Sort by score → Output (Top 5 Recommendations)

### Potential Bias
This system may over-prioritize genre since a genre match alone is worth +2.0 — twice as much as mood. Songs in underrepresented genres will rarely surface unless the user asks for them.

---

## Getting Started

### Setup
1. Create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
python -m src.main
```

### Running Tests
```bash
pytest
```

---

## Experiments You Tried

### Profile 1: High-Energy Pop Fan
- Settings: genre=pop, mood=happy, energy=0.85
- Top Result: Dynamite (BTS) — genre + mood match + high energy aligned perfectly
- Observation: All top 5 results were pop songs. Genre weight dominates strongly.

### Profile 2: Chill Hip-Hop Listener
- Settings: genre=hiphop, mood=chill, energy=0.40
- Top Result: Sunflower (Post Malone) — only hiphop/chill song, ranked first easily
- Observation: When genre and mood both match, the song tops the list regardless of energy.

### Profile 3: Intense Rock Lover
- Settings: genre=rock, mood=intense, energy=0.95
- Top Result: Enter Sandman (Metallica) — perfect genre, mood, and energy match
- Observation: Rock songs dominated. Classical songs scored near 0 for this profile.

### Weight Experiment
When I doubled the energy weight and halved the genre weight, low-energy classical songs climbed the rankings for low-energy profiles — showing how strongly weights shape results.

---

## Limitations and Risks

- Small catalog: Only 20 songs — real systems use millions
- No lyrics or language understanding
- Genre dominance creates filter bubbles — users rarely discover cross-genre songs
- No user history — the system treats every session identically
- Binary mood matching — no concept of similar moods

---

## Reflection

Building this recommender showed me how much a simple scoring formula shapes what a user sees. I was surprised that just by changing one weight, the entire ranking flipped. This mirrors real debates about Spotify's algorithm — it tends to lock users into what they already know.

Real music recommenders must balance accuracy (give users what they like) against discovery (show them something new). My system has no discovery mechanism at all.

See `model_card.md` for the full technical analysis.