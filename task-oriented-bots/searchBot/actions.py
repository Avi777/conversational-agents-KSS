from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import reprlib


class Search():
    
    def __init__(self, phrase):
        self.uri = 'https://api.duckduckgo.com'
        self.params = {
            'q': phrase,
            'format': 'json'
        }
        
    def fetch(self):
        response = requests.get(self.uri, params=self.params)
        a = response.json()
        answer = a.get('Answer')
        abstract_text = a.get('AbstractText')
        abstract_url = a.get('AbstractURL')
        related_topics = a.get('RelatedTopics')
        
        if answer:
            return answer
        elif abstract_text:
            return f"[{reprlib.repr(abstract_text)}]({abstract_url})"
        elif related_topics:
            redirect = related_topics[0]
            return f"[{redirect.get('Text')}]({redirect.get('FirstURL')}"
        else:
            return "Can't find answer"
            
        
    def __call__(self):
        return self.fetch()



class ActionSearch(Action):

    def name(self) -> Text:
        return "action_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        query = tracker.latest_message["text"].split(" ", 1)[1]
        answer = Search(query)()
        dispatcher.utter_message(text=answer)

        return []
