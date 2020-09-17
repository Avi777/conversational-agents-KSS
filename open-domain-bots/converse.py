from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
import requests
import time
from nltk.tokenize import sent_tokenize

bot_template = "BLENDER: {0}"


def converse(message):
    url = "http://0.0.0.0:37456"
    payload = {"text": message}
    r = requests.post(url, json=payload)
    return r.json().get("text", None)


def remove_question(message):
    s = sent_tokenize(message)
    return " ".join([x for x in s if "?" not in x])


def send_message(message):
    start = time.time()
    response = converse(message)
    try:
        refactored_response = remove_question(message)
    except:
        pass
    response_time = time.time() - start
    with open("conversation.txt", "a+") as fh:
        fh.write(f"{response_time}\n{message}\n{response}\n{refactored_response}\n\n")
    return bot_template.format(response)


while 1:
    input = prompt(
        "CHANDRA: ",
        history=FileHistory("history.txt"),
        auto_suggest=AutoSuggestFromHistory(),
    )
    print(send_message(input), "\n")
