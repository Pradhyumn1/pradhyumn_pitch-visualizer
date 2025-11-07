from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

try:
    response = client.images.generate(
        model="dall-e-3",
        prompt="a simple test image of a cat",
        size="1024x1024",
        n=1
    )
    print("✓ Success! Image URL:", response.data[0].url)
except Exception as e:
    print("✗ Error:", str(e))