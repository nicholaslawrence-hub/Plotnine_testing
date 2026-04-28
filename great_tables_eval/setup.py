import os
import dspy
from langsmith import Client
from dotenv import load_dotenv
from pathlib import Path
import random

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

API_KEY = os.getenv('LANGCHAIN_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
DATASET_NAME = os.getenv('LANGCHAIN_PROJECT')
print("LANGCHAIN:", os.getenv("LANGCHAIN_API_KEY"))

client = Client(api_key=API_KEY)

all_prompts = [
    "make a great_tables schedule from this CSV",
    "format my Caltrain data into a styled route table",
    "Help me create a route table with illustrations for a commuter rail.",
    "format this transit route table",
    "create a train schedule",
    "make me a timetable, then export it in html",
    "departure board",
    "make a commuter schedule with stop times",
    "create a rail timetable"
    "I want the fare zones color coded in red",
    "group my stops by zone and stripe the rows",
    "handle NaN values for express trains that skip stops",
    "make it look like an official printed schedule",
]

random.seed(42)
random.shuffle(all_prompts)
split = int(len(all_prompts) * 0.7)
train_prompts = all_prompts[:split]
test_prompts  = all_prompts[split:]

def push_dataset(name, prompts):
    existing = [d.name for d in client.list_datasets()]
    if name in existing:
        print(f"Dataset '{name}' exists, deleting and recreating...")
        client.delete_dataset(dataset_name=name)
 
    dataset = client.create_dataset(
        name,
        description="User prompts for transit route table skill generation eval"
    )
    client.create_examples(
        inputs=[{"prompt": p} for p in prompts],
        dataset_name=DATASET_NAME,
    )
    return dataset

def load_trainset_from_langsmith(DATASET_NAME):
    examples = list(client.list_examples(dataset_name=DATASET_NAME))
    trainset = [
        dspy.Example(user_prompt=ex.inputs["prompt"]).with_inputs("user_prompt")
        for ex in examples
    ]
    print(f"Loaded {len(trainset)} examples into DSPy trainset")
    for ex in trainset:
        print(f"  - {ex.user_prompt}")
    return trainset

if __name__ == "__main__":
    push_dataset("transit-skill-train", train_prompts)
    push_dataset("transit-skill-test",  test_prompts)
    print(f"\Trainset ready: {len(train_prompts)} examples, \nTest-set ready: {len(test_prompts)} examples.")