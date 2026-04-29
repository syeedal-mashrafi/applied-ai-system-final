# few_shot.py
import anthropic
from rag_enhanced import retrieve_multi_source, format_multi_source_context

client = anthropic.Anthropic()

FEW_SHOT_EXAMPLES = [
    {"role": "user", "content": "I'm feeling sad and lonely."},
    {"role": "assistant", "content": "I hear you — loneliness can feel really heavy. I'd suggest 'Someone Like You' by Adele. Therapeutically speaking, music that mirrors our emotions first helps us feel understood before gradually lifting our mood. After a few listens, try transitioning to something warmer like 'Anti-Hero' by Taylor Swift."},
    {"role": "user", "content": "I need energy for the gym."},
    {"role": "assistant", "content": "Research shows songs above 140 BPM reduce perceived exertion. I recommend 'Blinding Lights' by The Weeknd at 171 BPM — its driving synth-pop keeps your pace consistent. Pair it with 'HUMBLE.' by Kendrick Lamar for motivational lyrics when you hit a tough set."},
    {"role": "user", "content": "I'm trying to focus and study."},
    {"role": "assistant", "content": "For deep cognitive work, the key is minimizing lyrical interference. 'Clair de Lune' by Debussy is my top recommendation — its slow patterns reduce cognitive load while keeping you alert. If you need a gentle energy bump, Lo-Fi Hip Hop Beats at 70-90 BPM work wonderfully."},
]


def get_specialized_recommendation(user_mood: str, context: str) -> str:
    messages = FEW_SHOT_EXAMPLES.copy()
    messages.append({
        "role": "user",
        "content": f"I'm feeling: {user_mood}\n\nRelevant songs:\n{context}\n\nGive me a music therapist-style recommendation."
    })

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=400,
        system="You are a certified music therapist with 10 years of clinical experience. You ground your recommendations in research. You ONLY recommend songs provided to you.",
        messages=messages
    )
    return response.content[0].text.strip()


def compare_baseline_vs_specialized(user_mood: str, context: str):
    print("\n" + "="*55)
    print("BASELINE vs SPECIALIZED COMPARISON")
    print("="*55)

    baseline_resp = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=200,
        messages=[{"role": "user", "content": f"Recommend music for someone feeling: {user_mood}\n\nSongs: {context}"}]
    )
    baseline = baseline_resp.content[0].text.strip()
    specialized = get_specialized_recommendation(user_mood, context)

    print(f"\n📋 BASELINE ({len(baseline.split())} words):\n{baseline}")
    print(f"\n🎓 SPECIALIZED ({len(specialized.split())} words):\n{specialized}")
    print(f"\n📊 Word difference: +{len(specialized.split()) - len(baseline.split())} words")
    print("="*55)
    return specialized


if __name__ == "__main__":
    from rag_enhanced import retrieve_multi_source, format_multi_source_context
    mood = input("Enter a mood to test specialization: ")
    results = retrieve_multi_source(mood)
    context = format_multi_source_context(results)
    compare_baseline_vs_specialized(mood, context)