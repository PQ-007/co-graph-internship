from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables
api_key = os.getenv("WEATHER_API_KEY")


print(f"API Key: {api_key}")
