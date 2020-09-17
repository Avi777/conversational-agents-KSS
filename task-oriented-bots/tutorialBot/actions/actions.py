from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction

from fuzzywuzzy import process, fuzz
import random
import ast

import pandas as pd

db = pd.read_csv("actions/data/question_answer.csv").dropna()


class ActionReviewInit(Action):
    def name(self) -> Text:
        return "action_review_init"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        content_name = tracker.latest_message["text"].split(" ", 1)[1]
        review_content_name = self.resolve_object_name(content_name)
        # print(content_name)

        if review_content_name:
            dispatcher.utter_message(text=f"Initializing {review_content_name} quiz! 😊")
        else:
            dispatcher.utter_message(
                text=f"Sorry, I could not find {content_name} quiz 😞"
            )
            return []

        return [
            SlotSet("content_name", review_content_name),
            SlotSet("question_count", 0),
            SlotSet("points", 0),
            FollowupAction("action_get_question"),
        ]

    def resolve_object_name(self, text, threshold=80):
        # print(db.head(5))
        titles = db["quiz_title"]
        a = process.extractOne(text, titles)
        if a[1] >= threshold:
            return a[0]
        return None


class ActionGetQuestion(Action):
    def name(self) -> Text:
        return "action_get_question"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        content_name = tracker.get_slot("content_name")
        count = int(tracker.get_slot("question_count"))

        try:
            question = db[db["quiz_title"] == content_name].iloc[count][
                "question_title"
            ]
        except:
            points = int(tracker.get_slot("points"))
            dispatcher.utter_message(text=f"Congratulations! you got {points} points!")
            return []

        choices = db[db["quiz_title"] == content_name].iloc[count]["answers"]
        choices = ast.literal_eval(choices)
        choices = random.sample(choices, len(choices))
        buttons = []
        for choice in choices:
            button = {"title": choice, "payload": '/choose{"answer": "%s"}' % choice}
            buttons.append(button)

        dispatcher.utter_message(text=question, buttons=buttons)

        # print(count, question, choices, buttons, sep="\n")
        return []


class ActionCheckAnswer(Action):
    def name(self) -> Text:
        return "action_check_answer"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        content_name = tracker.get_slot("content_name")
        count = int(tracker.get_slot("question_count"))
        answer = db[db["quiz_title"] == content_name].iloc[count]["correct_answers"]
        answer = ast.literal_eval(answer)[0]
        user_answer = tracker.get_slot("answer")

        points = int(tracker.get_slot("points"))
        if fuzz.ratio(answer, user_answer) > 90:
            dispatcher.utter_message(text="Great!")
            points += 1
        else:
            dispatcher.utter_message(text="Ummm...")

        count += 1

        # print(count, answer, user_answer, sep="\n")

        return [
            SlotSet("question_count", count),
            SlotSet("points", points),
            FollowupAction("action_get_question"),
        ]
