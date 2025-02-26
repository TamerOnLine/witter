import os
import requests
from dotenv import load_dotenv

# تحميل المتغيرات البيئية من ملف .env
load_dotenv()

# جلب مفتاح API من المتغيرات البيئية
API_KEY = os.getenv("API_KEY")

def test_api_key():
    """Tests if the API key is valid by making a request to OpenWeather API."""
    if not API_KEY:
        return "API_KEY not found. Please check your .env file."

    test_city = "Berlin"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={test_city}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    if response.status_code == 200:
        return "API_KEY is valid and working correctly."
    elif response.status_code == 401:
        return "Invalid API_KEY. Please check your credentials."
    else:
        return f"Failed to connect to API. Status code: {response.status_code}"

# تشغيل الاختبار
print(test_api_key())

