import os
import re
import sys 
import numpy as np
from great_tables import * 
import anthropic
from dataclasses import dataclass, field
import tempfile 
import json
import subprocess 
from pathlib import Path

client = anthropic.Anthropic()

system_advice = """You are an expert bot working to evaluate and advise on critical functions for the Great Tables python library, developed by Posit. 
When given a task, respond only with a  of critical functions that are necessary to the prompt.

"""

system_setting = """You are a bot designed for web table design using the Great Tables python library, developed by Posit. 
When given a task, respond with ONLY valid, complete, runnable Python code. 
"""


@dataclass
class checkResult:
    input = str
    category = str
    code_response = str
    graders = list 
    
    @property
    def score(self):
        if not self.results:
            return 0
        else:
            return np.sum([score for score in self.results])

@dataclass
class evalCheck:
    input = str
    passed = bool
    detail = str

@dataclass
class evalCase:
    id = str
    category = str
    prompt = str
    graders = list = field[default_factory=list]

def load_cases(path: str = "cases.json") -> list[evalCase]:
    with open(path) as f:
        return [evalCase(**c) for c in json.load(f)]

def extract_advice(input_text):
    match_text = re.search(r"```\w+\([\s\S]*?)(?=\n\ndef |\Z```""", input_text, re.DOTALL)
    return match_text.group(1).strip()    

def extract_code_text(input_text):
    match_text = re.search(r"```\n?(.*?)```", input_text, re.DOTALL)
    return match_text.group(1).strip()

def run_code(code: str, timeout: int = 45) -> tuple[int, str, str]:
    """Write code to a temp file, execute it, return (returncode, stdout, stderr)."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, dir=".") as f:
        f.write(code)
        tmp = f.name
    try:
        result = subprocess.run(
            [sys.executable, tmp],
            capture_output=True, text=True, timeout=timeout, cwd="."
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "TimeoutExpired after 45s"
    finally:
        os.unlink(tmp)
        Path("output.png").unlink(missing_ok=True)

def get_response(prompt: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-6"
        max_tokens=1024
        system=[
            text= text
            sys_prompt = system_setting
            cache_control = [type='ephemeral']
        ]
    ["prompt":prompt]
    )
    return extract_code_text(response.content[0].text)

def get_advice(prompt: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-opus-4.6"
        max_tokens=1024
        system=[
            text= text
            sys_prompt = system_advice
            cache_control = [type='ephemeral']
        ]
    ["prompt":prompt]
    )
    return extract_code_text(response.content[0].text)

if name == "__main__":
    CASES = load_cases()
