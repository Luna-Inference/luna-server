from openai import OpenAI
import sys

# Point to the local server
client = OpenAI(base_url="http://localhost:1306/v1", api_key="anything")

def stream_chat(prompt):
    """Streams a chat completion response from the server."""
    try:
        stream = client.chat.completions.create(
            model="luna-small",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
        print("Assistant: ", end="")
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                sys.stdout.write(content)
                sys.stdout.flush()
        print()
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    print("Starting chat client. Type 'exit' or 'quit' to end.")
    while True:
        user_prompt = input("You: ")
        if user_prompt.lower() in ["exit", "quit"]:
            break
        stream_chat(user_prompt)
