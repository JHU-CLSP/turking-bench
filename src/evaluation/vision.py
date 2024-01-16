from __future__ import annotations
from enum import Enum

class Models(Enum):
    GPT4V = 1

class MyActions:
    def __init__(self, type: str, data: str, **kwargs):
        self.type = type
        self.data = data

        if "duration" in kwargs:
            self.duration = kwargs["duration"] # how long it took to execute the action

class VisionModel:
    """
    Base Vision Model class for all vision models
    """

    def __init__(self, model: Models):
        self.model = model

    def main(self, objective: str):
        """
        This is the main function for the Vision Language Model
        """
        assistant_message = {
            "role": "assistant",
            "content": "Hello, I am your assistant. How can I help you?"
        }
        user_message = {
            "role": "user",
            "content": self.get_main_prompt(objective)
        }

        messages = [assistant_message, user_message]

        while True:
            try:
                response = self.get_next_action(messages)
                action = self.parse_response(response)

                assert "type" in action and "data" in action, "Action should have a type and data"
            except Exception as e:
                print(e)
                break

            if action["type"] == "DONE":
                break

            response = self.execute_action(action)

            message = {
                "role": "assistant",
                "content": response
            }

            messages.append(message)
            
    def get_main_prompt(objective: str) -> str:
        """
        This function returns the prompt for the Vision Language Model
        """
        raise NotImplementedError("This method should be implemented by the subclass.")
    
    def get_next_action(self, messages: str) -> str:
        """
        This function gets the response from the VLM
        """
        raise NotImplementedError("This method should be implemented by the subclass.")

    def parse_response(self, messages: str) -> MyActions:
        """
        This function returns an action based on the response from the Vision Language Model
        """
        raise NotImplementedError("This method should be implemented by the subclass.")

    def execute_action(self, action: MyActions) -> str:
        """
        This function executes the action returned by the Vision Language Model
        """
        raise NotImplementedError("This method should be implemented by the subclass.")


class GPT4VModel:
    """
    This is the class for a Vision Language Model to solve tasks on a page
    """

    def get_next_action(self, messages: str):
        """
        This function gets the next action for the GPT4V Model
        """
        # send a request to GPT4V with messages

    def execute_action(self, action: MyActions) -> str:
        """
        This function executes the action returned by the GPT4V Model
        """

        if action.type == "CLICK":
            self.click(action.data)

    def click(self, data: str):
        """
        This function clicks on an element on the page
        """