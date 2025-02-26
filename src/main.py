import os
import requests
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool

# تحميل المتغيرات البيئية
load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_weather(city: str) -> str:
    """Fetches weather data for a given city using OpenWeather API."""
    if not API_KEY:
        return "API_KEY is missing. Please check your .env file."

    # تنظيف اسم المدينة لإزالة أي علامات اقتباس أو مسافات غير ضرورية
    city = city.strip().replace("'", "").replace('"', "")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"{city}: {weather_desc}, temperature: {temp}°C."
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except requests.exceptions.ConnectionError:
        return "Connection error! Check your internet connection."
    except requests.exceptions.Timeout:
        return "Request timed out! Try again later."
    except requests.exceptions.RequestException as err:
        return f"An error occurred: {err}"

# تعريف الأداة
weather_tool = Tool(
    name="Use the Weather API",
    func=get_weather,
    description="Fetches the current weather for a given city.",
    return_direct=True
)

# تهيئة النموذج LLM
llm = OllamaLLM(model="llama3.2")

# إنشاء الوكيل الذكي
agent = initialize_agent(
    tools=[weather_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    allowed_tools=["Use the Weather API"],
    handle_parsing_errors=True
)

# تجربة الاستخدام
print("Available tools:", [tool.name for tool in agent.tools])

while True:
    city = input("Enter a city name (or type 'exit' to quit): ")
    if city.lower() == 'exit':
        print("Exiting...")
        break
    response = agent.invoke(f"What is the weather like in {city}?")
    print(response)
