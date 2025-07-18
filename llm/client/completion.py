from openai import OpenAI
import sys

# Point to the local server
client = OpenAI(base_url="http://localhost:1306/v1", api_key="anything")

def chat_completions(prompt):
    """Sends a chat completion request to the server."""
    try:
        completion = client.chat.completions.create(
            model="luna-small",
            messages=[{"role": "user", "content": prompt}],
            stream=False,
        )
        print("Assistant: ", end="")
        content = completion.choices[0].message.content
        if content:
            print(content)
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    print("Starting chat client. Type 'exit' or 'quit' to end.")
    while True:
        user_prompt = input("You: ")
        if user_prompt.lower() in ["exit", "quit"]:
            break
        chat_completions(user_prompt)
