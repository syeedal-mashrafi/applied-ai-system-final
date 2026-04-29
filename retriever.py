# retriever.py
from music_data import MUSIC_CATALOG

def retrieve_songs(user_mood: str, top_k: int = 3) -> list:
    user_mood_lower = user_mood.lower()
    scored_songs = []

    for song in MUSIC_CATALOG:
        score = 0
        for mood_tag in song["mood"]:
            if mood_tag in user_mood_lower or user_mood_lower in mood_tag:
                score += 2
        if user_mood_lower in song["description"].lower():
            score += 1
        if user_mood_lower in song["genre"].lower():
            score += 1
        if score > 0:
            scored_songs.append((score, song))

    scored_songs.sort(key=lambda x: x[0], reverse=True)
    results = [song for _, song in scored_songs[:top_k]]

    print(f"\n[RAG LOG] User mood: '{user_mood}'")
    print(f"[RAG LOG] Retrieved {len(results)} songs:")
    for r in results:
        print(f"  - {r['title']} by {r['artist']}")

    return results


def format_context(songs: list) -> str:
    if not songs:
        return "No specific songs found in the database for this mood."

    context = "Here are relevant songs from the music database:\n\n"
    for song in songs:
        context += f"- **{song['title']}** by {song['artist']}\n"
        context += f"  Genre: {song['genre']} | Mood tags: {', '.join(song['mood'])}\n"
        context += f"  About: {song['description']}\n\n"
    return context