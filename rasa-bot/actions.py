# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from typing import Any, Text, Dict, List
import logging

import os
import pathlib
import json
from rasa_sdk import Action, Tracker
from rasa_sdk.events import BotUttered
from rasa_sdk.executor import CollectingDispatcher

PATH_SCRIPT = pathlib.Path(__file__).parent.absolute()
DIR_DATA = 'data'
DIR_RESPONSES = 'responses'

FILE_HOW_TO = 'how_to.json'


class ActionAskHowTo(Action):

    def name(self) -> Text:
        return "action_how_to"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        logging.info("[Debug] Intent: How To")
        try:
            concept = next(tracker.get_latest_entity_values(entity_type="concept")).lower()
            logging.info(f"[Debug] Concept {concept}")
            with open(os.path.join(PATH_SCRIPT, DIR_DATA, DIR_RESPONSES, FILE_HOW_TO), 'r') as fp:
                responses = json.load(fp)

            answer = responses[concept]
            dispatcher.utter_message(text=answer)
        except StopIteration:
            logging.info(f"[Debug] No concept detected")
            dispatcher.utter_message(text="I don't understand which subject you want to know how to use")
        except KeyError:
            logging.info(f"[Debug] No concept found")
            dispatcher.utter_message(template="utter_default")

        return []


class ActionDisplaySlot(Action):

    def name(self) -> Text:
        return "action_display_slot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        logging.info(f"Concept slot detected: {tracker.get_slot('concept')}")

        return []



