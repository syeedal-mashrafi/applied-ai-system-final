# main.py
import anthropic
import logging
from rag_enhanced import retrieve_multi_source, format_multi_source_context

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

client = anthropic.Anthropic()

def validate_input(user_input: str):
    if not user_input or len(user_input.strip()) == 0:
        return False, "Input cannot be empty."
    if len(user_input) > 200:
        return False, "Input too long. Please keep it under 200 characters."
    banned = ["hack", "exploit", "ignore previous", "jailbreak"]
    for word in banned:
        if word in user_input.lower():
            return False, "Invalid input detected."
    return True, ""


def get_recommendation(user_mood: str) -> str:
    results = retrieve_multi_source(user_mood, top_k=3)
    context = format_multi_source_context(results)

    rag_prompt = f"""You are a music recommendation assistant.
A user is feeling: "{user_mood}"

I have searched THREE sources for you:
{context}

Using the information above, recommend the best 1-2 songs for this user's mood.
Mention ONE relevant insight from the expert notes if applicable.
Explain in 2-3 sentences why each song fits. Be warm and conversational."""

    logging.info(f"Sending RAG prompt for mood: {user_mood}")

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=500,
        messages=[{"role": "user", "content": rag_prompt}]
    )

    answer = response.content[0].text
    logging.info(f"Response received.")
    return answer


def validate_output(response: str):
    if len(response) < 20:
        return False, "Response too short."
    return True, response


def main():
    print("🎵 RAG Music Recommender — Project 4")
    print("=" * 45)
    print("Tell me how you're feeling and I'll recommend songs!")
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("How are you feeling? → ").strip()

        if user_input.lower() in ["quit", "exit", "q"]:
            print("Thanks for using the music recommender!")
            break

        is_valid, error_msg = validate_input(user_input)
        if not is_valid:
            print(f"⚠️  {error_msg}\n")
            logging.warning(f"Invalid input blocked: {user_input}")
            continue

        print("\n🔍 Searching music database...")
        recommendation = get_recommendation(user_input)

        is_valid_out, result = validate_output(recommendation)
        if not is_valid_out:
            print("⚠️  Something went wrong. Please try again.\n")
            continue

        print(f"\n🎵 Recommendation:\n{recommendation}\n")
        print("-" * 45 + "\n")


if __name__ == "__main__":
    main()