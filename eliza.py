# Example: Rule-based chatbots(Also Noob)

import re
import random
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter


ElizaCompleter = WordCompleter(
    ["do you think ", "do you remember ", "I want ", "if "],
    sentence=True,
    match_middle=True,
)

bot_template = "BOT : {0}"

# A dictionary of questions, patterns as keys and
# lists of appropriate responses as values
rules = {
    "I want (.*)": [
        "What would it mean if you got {0}",
        "Why do you want {0}",
        "What's stopping you from getting {0}",
    ],
    "do you remember (.*)": [
        "Did you think I would forget {0}",
        "Why haven't you been able to forget {0}",
        "What about {0}",
        "Yes .. and?",
    ],
    "do you think (.*)": ["if {0}? Absolutely.", "No chance"],
    "if (.*)": [
        "Do you really think it's likely that {0}",
        "Do you wish that {0}",
        "What do you think about {0}",
        "Really--if {0}",
    ],
}

# match messages against some common patterns and extract phrases
def match_rule(rules, message):
    for pattern, responses in rules.items():
        match = re.search(pattern, message)
        if match is not None:
            response = random.choice(responses)
            var = match.group(1) if "{0}" in response else None
            return response, var
    return "default", None


# make responses grammatically coherent
# transform the extracted phrases from first to second person and vice versa
def replace_pronouns(message):
    message = message.lower()
    # Replace 'me' with 'you'
    if "me" in message:
        return re.sub("me", "you", message)
    if "my" in message:
        return re.sub("my", "your", message)
    if "your" in message:
        return re.sub("your", "my", message)
    if "you" in message:
        return re.sub("you", "me", message)

    return message


def respond(message):
    response, phrase = match_rule(rules, message)
    if "{0}" in response:
        # Replace the pronouns in the phrase
        phrase = replace_pronouns(phrase)
        response = response.format(phrase)
    return response


def send_message(message):
    response = respond(message)
    return bot_template.format(response)


while input != ':q':
    input = prompt(
        "USER: ",
        history=FileHistory("history.txt"),
        auto_suggest=AutoSuggestFromHistory(),
        completer=ElizaCompleter,
    )
    print(send_message(input),"\n")


# send_message("do you remember your last birthday")
# send_message("do you think humans should be worried about AI")
# send_message("I want a robot friend")
# send_message("what if you could be anything you wanted")
