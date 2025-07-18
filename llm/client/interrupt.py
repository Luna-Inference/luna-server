import requests

# The base URL of the server, matching the llm/server.py configuration
SERVER_URL = "http://localhost:1306"

def interrupt_inference():
    """Sends a POST request to the /v1/abort endpoint."""
    try:
        response = requests.post(f"{SERVER_URL}/v1/abort")
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        print("Successfully sent interrupt signal.")
        print("Server response:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    interrupt_inference()
