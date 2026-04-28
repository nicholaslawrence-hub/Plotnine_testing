import os
import sys
import dspy
from src.pipeline import compile, run, eval_dataset
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

dspy.configure(lm=dspy.LM("anthropic/claude-sonnet-4-6", api_key=GEMINI_API_KEY))

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"

    if cmd == "compile":
        compile()
    elif cmd == "run":
        prompt = " ".join(sys.argv[2:])
        run(prompt)
    elif cmd == "eval":
        eval_dataset()