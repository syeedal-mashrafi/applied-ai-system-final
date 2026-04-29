# agent.py
import anthropic
from rag_enhanced import retrieve_multi_source, format_multi_source_context

client = anthropic.Anthropic()

def run_agent(user_input: str) -> str:
    print("\n" + "="*50)
    print("🤖 AGENT REASONING TRACE")
    print("="*50)

    print("\n[Step 1] Classifying mood...")
    classification_prompt = f"""The user said: "{user_input}"
Classify this into ONE of these mood categories:
- energetic
- sad
- calm
- happy
- reflective
- anxious
Reply with ONLY the category name. Nothing else."""

    response1 = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=20,
        messages=[{"role": "user", "content": classification_prompt}]
    )
    mood_category = response1.content[0].text.strip().lower()
    print(f"  → Classified mood as: '{mood_category}'")

    print(f"\n[Step 2] Retrieving songs for mood: '{mood_category}'...")
    retrieved = retrieve_multi_source(mood_category, top_k=3)
    context = format_multi_source_context(retrieved)
    print(f"  → Found {len(retrieved.get('catalog', []))} catalog songs")

    print(f"\n[Step 3] Evaluating retrieved songs...")
    eval_prompt = f"""The user mood is: "{user_input}" (classified as: {mood_category})
Retrieved songs:
{context}
Rate how well these songs fit on a scale of 1-10.
Identify the ONE best match and why in one sentence.
Format:
FIT SCORE: [number]/10
BEST MATCH: [song title]
REASON: [one sentence]"""

    response2 = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=100,
        messages=[{"role": "user", "content": eval_prompt}]
    )
    evaluation = response2.content[0].text.strip()
    print(f"  → Evaluation:\n{evaluation}")

    print(f"\n[Step 4] Generating final recommendation...")
    final_prompt = f"""You are a warm, friendly music assistant.
User mood: "{user_input}"
Mood category: {mood_category}
Internal evaluation: {evaluation}
Available songs:
{context}
Write a final recommendation. Recommend 1-2 songs. Be conversational.
Keep it to 3-4 sentences total."""

    response3 = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=300,
        messages=[{"role": "user", "content": final_prompt}]
    )
    final_answer = response3.content[0].text.strip()
    print(f"\n[Step 4 complete]")
    print("="*50 + "\n")
    return final_answer


if __name__ == "__main__":
    print("🎵 Agentic Music Recommender")
    print("Type 'quit' to exit.\n")
    while True:
        user_input = input("How are you feeling? → ").strip()
        if user_input.lower() in ["quit", "exit"]:
            break
        if not user_input:
            print("⚠️  Please enter something.\n")
            continue
        result = run_agent(user_input)
        print(f"\n🎵 Recommendation:\n{result}\n")