# rag_enhanced.py
from music_data import MUSIC_CATALOG

CUSTOM_MUSIC_NOTES = """
MUSIC THERAPIST RECOMMENDATIONS:

For anxiety and stress relief:
- Weightless by Marconi Union is clinically proven to reduce anxiety by 65%.
- Classical piano pieces like Clair de Lune reduce cortisol levels.

For workout and high energy:
- Studies show songs above 140 BPM improve athletic performance.
- Blinding Lights by The Weeknd at 171 BPM is ideal for running or HIIT.
- HUMBLE. by Kendrick Lamar provides motivational lyrics and driving bass.

For focus and deep work:
- Lo-fi beats at 70-90 BPM minimize distraction while maintaining alertness.
- Classical instrumental pieces have zero lyrical interference.

For emotional processing:
- Slow songs at 60-80 BPM match a resting heartbeat and aid emotional release.
- Adele's Someone Like You is commonly cited in grief counseling contexts.
- Taylor Swift's Anti-Hero helps with self-reflection and identity work.
"""

GENRE_METADATA = {
    "Synth-pop":   {"energy": "high",    "context": "driving, exercise, nostalgia"},
    "Soul":        {"energy": "medium",  "context": "emotional moments, reflection"},
    "Pop/Soul":    {"energy": "high",    "context": "daily mood boost, morning"},
    "Classical":   {"energy": "low",     "context": "study, sleep, stress relief"},
    "Hip-Hop":     {"energy": "high",    "context": "motivation, gym, confidence"},
    "Indie Pop":   {"energy": "medium",  "context": "reflection, quirky moods"},
    "Ambient":     {"energy": "very low","context": "anxiety, sleep, meditation"},
    "Rock":        {"energy": "high",    "context": "epic moments, driving"},
    "Lo-Fi":       {"energy": "low",     "context": "studying, coding, chill work"},
    "Pop":         {"energy": "medium",  "context": "casual listening, fun"},
}


def retrieve_multi_source(user_mood: str, top_k: int = 3) -> dict:
    user_mood_lower = user_mood.lower()
    results = {}

    scored = []
    for song in MUSIC_CATALOG:
        score = 0
        for tag in song["mood"]:
            if tag in user_mood_lower or user_mood_lower in tag:
                score += 2
        if user_mood_lower in song["description"].lower():
            score += 1
        if user_mood_lower in song["genre"].lower():
            score += 1
        if score > 0:
            scored.append((score, song))
    scored.sort(key=lambda x: x[0], reverse=True)
    results["catalog"] = [s for _, s in scored[:top_k]]

    relevant_lines = []
    for line in CUSTOM_MUSIC_NOTES.strip().split("\n"):
        if user_mood_lower in line.lower() and len(line.strip()) > 10:
            relevant_lines.append(line.strip())
    results["expert_notes"] = relevant_lines[:3]

    matched_genres = []
    for genre, meta in GENRE_METADATA.items():
        if (user_mood_lower in meta["context"].lower() or
                user_mood_lower in meta["energy"].lower()):
            matched_genres.append(f"{genre} — {meta['context']}")
    results["genre_context"] = matched_genres[:3]

    print(f"\n[ENHANCED RAG] Mood: '{user_mood}'")
    print(f"  Source 1 (catalog):      {len(results['catalog'])} songs")
    print(f"  Source 2 (expert notes): {len(results['expert_notes'])} lines")
    print(f"  Source 3 (genre meta):   {len(results['genre_context'])} genres")

    return results


def format_multi_source_context(results: dict) -> str:
    context = ""

    if results["catalog"]:
        context += "SONGS FROM DATABASE:\n"
        for song in results["catalog"]:
            context += f"- {song['title']} by {song['artist']} "
            context += f"({song['genre']}, moods: {', '.join(song['mood'])})\n"
            context += f"  {song['description']}\n"
        context += "\n"

    if results["expert_notes"]:
        context += "EXPERT MUSIC THERAPY NOTES:\n"
        for line in results["expert_notes"]:
            context += f"- {line}\n"
        context += "\n"

    if results["genre_context"]:
        context += "GENRE CONTEXT:\n"
        for g in results["genre_context"]:
            context += f"- {g}\n"

    return context if context else "No specific data found for this mood."