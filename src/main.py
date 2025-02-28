import os
import logging
import requests
from dotenv import load_dotenv
from run_ollama import OllamaHandler
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
LOGGER = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_weather(city: str) -> str:
    """
    Fetches weather data for a given city using OpenWeather API.
    """
    if not API_KEY:
        return "API_KEY is missing. Please check your .env file."

    # Clean city name to remove unnecessary quotes or spaces
    city = city.strip().replace("'", "").replace('"', "")

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric"}

    try:
        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]

        return f"{city}: {weather_desc}, temperature: {temp}°C."
    
    except requests.exceptions.HTTPError as http_err:
        LOGGER.error(f"HTTP error occurred: {http_err}")
        return f"HTTP error occurred: {http_err}"
    
    except requests.exceptions.ConnectionError:
        LOGGER.error("Connection error! Check your internet connection.")
        return "Connection error! Check your internet connection."
    
    except requests.exceptions.Timeout:
        LOGGER.error("Request timed out! Try again later.")
        return "Request timed out! Try again later."
    
    except requests.exceptions.RequestException as err:
        LOGGER.error(f"An error occurred: {err}")
        return f"An error occurred: {err}"

# Define the tool
weather_tool = Tool(
    name="Use the Weather API",
    func=get_weather,
    description="Fetches the current weather for a given city.",
    return_direct=True,
)

handler = OllamaHandler()

# Create the intelligent agent
agent = initialize_agent(
    tools=[weather_tool],
    llm=handler.llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    allowed_tools=["Use the Weather API"],
    handle_parsing_errors=True,
)

LOGGER.info("Available tools: %s", [tool.name for tool in agent.tools])

# Interactive session for weather queries
while True:
    city = input("Enter a city name (or type 'exit' to quit): ").strip()
    
    if city.lower() == "exit":
        LOGGER.info("Exiting...")
        print("Exiting...")
        break
    
    response = agent.invoke(f"What is the weather like in {city}?")
    print(response)
