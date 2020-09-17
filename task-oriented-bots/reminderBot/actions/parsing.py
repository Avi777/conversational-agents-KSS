from dateutil import relativedelta, parser
from typing import Dict, Text, Any, Optional
from rasa_sdk import Tracker
import datetime
import pytz
from tzlocal import get_localzone

import spacy

nlp = spacy.load("en_core_web_sm")


def get_entity_details(
    tracker: Tracker, entity_type: Text
) -> Optional[Dict[Text, Any]]:
    all_entities = tracker.latest_message.get("entities", [])
    entities = [e for e in all_entities if e.get("entity") == entity_type]
    if entities:
        return entities[0]


def check_timeinfo_validity(value):
    parsed = parser.parse(value)
    current = datetime.datetime.now(tz=get_localzone())
    if parsed.time() == datetime.time(0):
        return None
    # check if reminder time is greater than current time
    if parsed.date() > current.date():
        return value
    elif parsed.date() == current.date() and parsed.time() > current.time():
        return value
    else:
        tdelta = datetime.timedelta(days=1)
        return str(parsed + tdelta)


def add_timezone_info(datetime_info, grain):
    local_tz = get_localzone()
    if grain in ["minute", "hour", "day"]:
        return str(parser.parse(datetime_info).replace(tzinfo=local_tz))
    else:
        return str(parser.parse(datetime_info).astimezone(local_tz))


def format_isotime_by_grain(isotime, grain=None):
    value = parser.isoparse(isotime)
    grain_format = {
        "second": "%I:%M:%S%p, %A %b %d, %Y",
        "day": "%A %b %d, %Y",
        "week": "%A %b %d, %Y",
        "month": "%b %Y",
        "year": "%Y",
    }
    timeformat = grain_format.get(grain, "%I:%M%p, %A %b %d, %Y")
    time_formatted = value.strftime(timeformat)
    return time_formatted


def parse_duckling_time(timeentity: Dict[Text, Any]) -> Optional[Dict[Text, Any]]:
    try:
        timeinfo = timeentity.get("additional_info", {})
    except AttributeError:
        return {"time": None, "time_formatted": None}
    if timeinfo.get("type") == "value":
        grain = timeinfo.get("grain")
        # add timezone info
        value = add_timezone_info(timeinfo.get("value"), grain)
        # check timeinfo validity
        value = check_timeinfo_validity(value)
        if value == None:
            return {"time": None, "time_formatted": None}

        parsedtime = {
            "time": value,
            "time_formatted": format_isotime_by_grain(value, grain),
        }
        return parsedtime


def parse_sentence(text):
    doc = nlp(text)
    dep_labels = ["nsubj", "nsubjpass", "dobj", "iobj", "compound", "pobj", "attr"]
    pos_labels = ["NOUN", "PROPN"]
    lemma_labels = ["remind", "reminder"]
    candidates = []
    for t in doc:
        if (
            t.dep_ in dep_labels
            and t.pos_ in pos_labels
            and t.lemma_ not in lemma_labels
        ):
            entity = str(t)
            pobj_flag = True if t.dep_ == "pobj" else False

            supporting_tokens = t.ancestors
            verb = noun = ""
            verb_flag = noun_flag = False

            for supporting_token in supporting_tokens:
                if supporting_token.pos_ in ["VERB", "ADJ"]:
                    verb = str(supporting_token) + " "
                    verb_flag = True
                elif supporting_token.pos_ in pos_labels:
                    noun = " " + str(supporting_token)
                    noun_flag = True
                candidates.append((verb + entity + noun, pobj_flag, verb_flag))
    return candidates


def get_reminder_title(text):
    # choose the best candidate
    # Harcoded rules based on heuristics and logic
    candidates = parse_sentence(text)
    reminder_titles = []
    for candidate in candidates:
        if not candidate[1]:
            return candidate[0]
        elif len(candidate[0].split()) == 1:
            reminder_titles.append(candidate[0])
        elif not candidate[2]:
            reminder_titles.append(candidate[0])

    if reminder_titles:
        return reminder_titles[-1]

    try:
        return candidates[-1][0]
    except:
        return None
