import re
from prompt_toolkit import prompt

bot_template = "BOT : {0}"


def find_name(message):
    name = None
    # pattern for checking if the keyword occurs
    name_keyword = re.compile("name|call")
    # pattern for finding capitalized words
    name_pattern = re.compile("[A-Z][a-z]*")
    if name_keyword.search(message):
        name_words = name_pattern.findall(message)
        if len(name_words) > 0:
            name = " ".join(name_words)
    return name


def respond(message):
    name = find_name(message)
    if name is None:
        return "Hi there!"
    else:
        return "Hello, {0}".format(name)


def send_message(message):
    response = respond(message)
    return bot_template.format(response)


while 1:
    input = prompt("USER: ")
    print(send_message(input))


# send_message("my name is Daisy Daisy")
# send_message("call me sexy")
# send_message("People call me Bond, James Bond.")
