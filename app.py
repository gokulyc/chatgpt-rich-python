import openai
from dotenv import load_dotenv
import os
import sys
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from pathlib import Path
from datetime import datetime

load_dotenv(".env")

console = Console()
RESULTS_DIR = Path("results")
current_time_stamp_str = datetime.utcnow().strftime("%Y_%m_%d_%H_%M_%S")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    console.print("OPENAI_API_KEY not found !!!", style="white on red")
    sys.exit(1)
openai.api_key = OPENAI_API_KEY


def print_or_save_rich_markdown(text_md, console=console, path_to_save: Path = None):
    if path_to_save is not None:
        (path_to_save / "result.md").open(mode="a").writelines([text_md])
    else:
        md = Markdown(text_md)
        console.print(md)


messages: list[dict] = [
    {"role": "system", "content": "You are a helpful assistant."},
]


while True:
    # question = "How to use hatch to build python package?"
    question = Prompt.ask("Ask a question, Answered by gpt-3.5-turbo OR type Stop?")
    assert len(question) > 0
    if question.lower() == "stop":
        console.print("User Exit.", style="white on green")
        sys.exit(0)
    try:
        (RESULTS_DIR / current_time_stamp_str).mkdir()
    except FileExistsError:
        pass
    (RESULTS_DIR / current_time_stamp_str / "question.txt").open(mode="a").writelines(
        [
            question + "\n",
        ]
    )

    messages.append(
        {
            "role": "user",
            "content": question,
        },
    )

    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    console.print(res)
    reply_content = res["choices"][0]["message"]["content"]
    console.print(reply_content, style="white on blue")
    messages.append({"role": "assistant", "content": reply_content})

    print_or_save_rich_markdown(
        reply_content,
        path_to_save=RESULTS_DIR / current_time_stamp_str,
    )
