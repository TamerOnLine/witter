import logging
import json
import sys
from typing import ClassVar, Optional

from langchain_ollama import OllamaLLM
from pydantic import BaseModel, Field

# Configure logging for error tracking
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)


class OllamaHandler(BaseModel):
    """
    Handles interaction with the Ollama LLM model.
    """

    MODEL_NAME: ClassVar[str] = "llama3.2"
    model: str = Field(default=MODEL_NAME)
    llm: Optional[OllamaLLM] = None

    def __init__(self, **data):
        """
        Initializes the class correctly using Pydantic.
        """
        super().__init__(**data)
        object.__setattr__(self, "llm", self.get_llm())

    def get_llm(self) -> Optional[OllamaLLM]:
        """
        Initializes and returns an instance of OllamaLLM.
        """
        try:
            if not isinstance(self.model, str) or not self.model.strip():
                raise ValueError("Invalid model name provided.")

            return OllamaLLM(
                model=self.model,
                system_message=(
                    "Analyze the text and provide a clear summary in valid JSON format."
                ),
                output_format="json",
                strict_mode=True,
                return_direct=True,
            )
        except Exception as e:
            LOGGER.error(f"Error initializing the model: {e}")
            return None

    def _call(self, prompt: str, stop: Optional[str] = None) -> str:
        """
        Implements the LLM API expected by LangChain.
        """
        return self.explain_question_mark(prompt)

    def explain_question_mark(self, question: str) -> str:
        """
        Uses the LLM model to explain the given question.
        """
        if self.llm is None:
            return "Error: Model initialization failed."

        try:
            response = self.llm.invoke(question)
            return response
        except Exception as e:
            LOGGER.error(f"Error invoking the model: {e}")
            return f"Error retrieving response: {e}"

    def interactive_mode(self) -> None:
        """
        Interactive console interface for user input.
        """
        print("Welcome! Enter your question (or 'exit' to quit):")

        while True:
            user_input = input("\nYour question: ").strip()

            if user_input.lower() in {"exit", "quit"}:
                print("\nProgram terminated. Goodbye!")
                sys.exit(0)

            if not user_input:
                print(" Please enter a valid question.")
                continue

            explanation = self.explain_question_mark(user_input)

            print("\nModel response:\n")
            try:
                parsed_response = (
                    json.loads(explanation) if isinstance(explanation, str) else explanation
                )
                print(json.dumps(parsed_response, indent=2, ensure_ascii=False))
            except json.JSONDecodeError:
                print(explanation)


if __name__ == "__main__":
    handler = OllamaHandler()
    handler.interactive_mode()
