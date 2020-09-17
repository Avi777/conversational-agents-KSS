# Code for my ML peeps
# Level: NOOB

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

bot_template = "BOT : {0}"

def respond(message):
    bot_message = "I can hear you! You said: " + message
    return bot_message


def send_message(message):
    response = respond(message)
    return bot_template.format(response)


while input != ':q':
    input = prompt(
        "USER: ",
        history=FileHistory("history.txt"),
        auto_suggest=AutoSuggestFromHistory(),
    )
    print(send_message(input),"\n")
