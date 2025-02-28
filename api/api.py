from fastapi import FastAPI
from core.main import get_weather
from core.run_ollama import OllamaHandler


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


# استعلام الطقس عبر API
@app.get("/weather/")
def weather(city: str):
    return {"weather": get_weather(city)}

# استعلام Ollama عبر API
ollama_handler = OllamaHandler()

@app.get("/ollama/")
def ollama_response(question: str):
    response = ollama_handler.explain_question_mark(question)
    return {"response": response}




