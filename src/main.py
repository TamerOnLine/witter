from langchain_ollama import OllamaLLM
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
import requests
import os
from dotenv import load_dotenv

# تحميل المتغيرات البيئية
load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_weather(city: str) -> str:
    """Fetches weather data for a given city using OpenWeather API."""
    if not API_KEY:
        return "API_KEY is missing. Please check your .env file."

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"{city}: {weather_desc}, temperature: {temp}°C."
    return "Unable to fetch weather data. Please check the city name or try again later."

# تعريف الأداة
weather_tool = Tool(
    name="Weather API",  # تأكد أن الاسم هنا مطابق لما سيتم استدعاؤه لاحقًا
    func=get_weather,
    return_direct=True,
    description="Use this tool to fetch the weather conditions for any given city.",
)

# تهيئة النموذج LLM
llm = OllamaLLM(model="llama3.2")

# إنشاء الوكيل الذكي
agent = initialize_agent(
    tools=[weather_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

# تجربة الاستخدام

print("Available tools:", [tool.name for tool in agent.tools])

response = agent.invoke("What is the weather like in Berlin?")
print(response)
