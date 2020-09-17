from prompt_toolkit import prompt
import spacy
from sklearn import svm

nlp = spacy.load("en_core_web_md")


class Intent:
    GREET = "GREET"
    JOKE = "JOKE"
    BYE = "BYE"
    THANK = "THANK"


train_x = [
    "Hi",
    "Hello",
    "Hi How are you?",
    "Good Morning",
    "bye",
    "good night",
    "take care",
    "Cool. Thanks",
    "Thanks!",
    "Thank you",
    "Tell me a joke",
    "joke"
]

train_y = [
    Intent.GREET,
    Intent.GREET,
    Intent.GREET,
    Intent.GREET,
    Intent.BYE,
    Intent.BYE,
    Intent.BYE,
    Intent.THANK,
    Intent.THANK,
    Intent.THANK,
    Intent.JOKE,
    Intent.JOKE,
]


def train(train_x, train_y):
    docs = [nlp(text) for text in train_x]
    train_x_word_vectors = [x.vector for x in docs]

    clf_svm = svm.SVC(kernel="linear")
    clf_svm.fit(train_x_word_vectors, train_y)

    return clf_svm


def predict(clf, test_x):
    test_docs = [nlp(text) for text in test_x]
    test_x_word_vectors = [x.vector for x in test_docs]

    return clf.predict(test_x_word_vectors)


if __name__ == "__main__":
    clf = train(train_x, train_y)
    print("Intent Classifier Trained")
    print("="*25)
    while input != ':q':
        input = prompt("MESSAGE: ")
        print(f"INTENT : {predict(clf,[input])}","\n")
