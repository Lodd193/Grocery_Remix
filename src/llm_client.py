"""
LMStudio API client for Grocery Remix.
Handles connection to local LMStudio server running Llama 3.1 8B Instruct.
"""

from openai import OpenAI


class LMStudioClient:
    """Client for interacting with LMStudio's local API."""

    def __init__(self, base_url="http://localhost:1234/v1", api_key="lm-studio"):
        """
        Initialize LMStudio client.

        Args:
            base_url: LMStudio server URL (default: http://localhost:1234/v1)
            api_key: API key (LMStudio doesn't require real key, but library needs one)
        """
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key  # LMStudio doesn't validate this, but OpenAI client requires it
        )
        self.model = "meta-llama-3.1-8b-instruct"

    def generate_response(self, prompt, system_prompt=None, temperature=0.7, max_tokens=1000):
        """
        Generate a response from the LLM.

        Args:
            prompt: User prompt/question
            system_prompt: System prompt to set context (optional)
            temperature: Sampling temperature (0.0-1.0, higher = more creative)
            max_tokens: Maximum tokens to generate

        Returns:
            str: Generated response from the LLM
        """
        messages = []

        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })

        messages.append({
            "role": "user",
            "content": prompt
        })

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

            return response.choices[0].message.content

        except Exception as e:
            raise ConnectionError(f"Failed to connect to LMStudio: {str(e)}")

    def test_connection(self):
        """
        Test connection to LMStudio server.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            response = self.generate_response(
                prompt="Say 'Hello' if you can hear me.",
                max_tokens=50
            )
            return True
        except Exception as e:
            print(f"Connection test failed: {str(e)}")
            return False


if __name__ == "__main__":
    # Test the connection
    print("Testing LMStudio connection...")
    client = LMStudioClient()

    if client.test_connection():
        print("[OK] Successfully connected to LMStudio!")

        # Try a simple recipe query
        print("\nTesting recipe generation...")
        response = client.generate_response(
            system_prompt="You are a helpful chef assistant that suggests recipes.",
            prompt="I have chicken, rice, and broccoli. Suggest a simple recipe.",
            temperature=0.7,
            max_tokens=500
        )
        print(f"\nResponse:\n{response}")
    else:
        print("[FAILED] Could not connect to LMStudio.")
        print("\nMake sure:")
        print("1. LMStudio is running")
        print("2. The server is started (click 'Start Server' in LMStudio)")
        print("3. meta-llama-3.1-8b-instruct model is loaded")
