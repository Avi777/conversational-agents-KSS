from typing import Any, Text, Dict, List, Union
import datetime
from dateutil import parser

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from actions.parsing import parse_duckling_time, get_entity_details, get_reminder_title
from rasa_sdk.events import ReminderScheduled, ReminderCancelled
from rasa_sdk.events import SlotSet, FollowupAction, AllSlotsReset


class ActionInitReminder(Action):
    def name(self) -> Text:
        return "action_init_reminder"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        r = tracker.latest_message["text"]
        try:
            reminder = get_reminder_title(r)
        except:
            reminder = None
        
        return [
            SlotSet("reminder_title", reminder),
            FollowupAction("set_reminder_form"),
        ]


class ReminderForm(FormAction):
    def name(self) -> Text:
        return "set_reminder_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["reminder_title", "time"]
        

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "reminder_title": [
                self.from_entity(entity="reminder_title"),
                self.from_text(intent="set_reminder"),
                self.from_text()],
            "time": self.from_entity(entity="time"),
        }


    def validate_time(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate time value."""

        timeentity = get_entity_details(tracker, "time")
        parsedtime = parse_duckling_time(timeentity)
        # print(timeentity,parsedtime)
        if not parsedtime:
            dispatcher.utter_message(text="No time man!")
            return {"time": None}
        return parsedtime


    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        return []

    

class ActionSetReminder(Action):
    """Schedules a reminder, supplied with the last message's entities."""

    def name(self) -> Text:
        return "action_set_reminder"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        reminder_title = tracker.get_slot("reminder_title")
        date_time = parser.parse(tracker.get_slot("time"))

        # print(tracker.latest_message.get("entities"))
        reminder = ReminderScheduled(
            "EXTERNAL_reminder",
            trigger_date_time=date_time.replace(tzinfo=None),
            timestamp=date_time.timestamp(),
            entities={"reminder_title": reminder_title},
            name=reminder_title,
            kill_on_user_message=False,
        )

        # print(reminder_title, date_time, reminder,sep='\n')

        dispatcher.utter_message("Reminder Set!")
        return [reminder]


class ActionReactToReminder(Action):
    def name(self) -> Text:
        return "action_react_to_reminder"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        reminder_title = next(tracker.get_latest_entity_values("reminder_title"),"Reminder!")
        dispatcher.utter_message(f"Reminder: {reminder_title}")

        return []