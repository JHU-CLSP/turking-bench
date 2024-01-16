from __future__ import annotations
from enum import Enum

import pyautogui
import platform
import os
import subprocess
import Xlib.display

class Models(Enum):
    GPT4V = 1

class ActionInstance:
    def __init__(self, type: str, data: str, **kwargs):
        self.type = type
        self.data = data

        if "duration" in kwargs:
            self.duration = kwargs["duration"] # how long it took to execute the action

class Actions:
    def __init__(self):
        self.platform = platform.system()

        if (self.platform == "Darwin" or self.platform == "Windows"):
            self.width, self.height = pyautogui.size()

        self.dir = "screenshots"

    def click_percentage(self, x_percent: float, y_percent: float, duration: float = 0.2, circle_radius: int = 50, circle_duration: float = 0.5):
        """
        This function clicks on a percentage of the screen
        """
        x_pixel = int(self.width * x_percent)
        y_pixel = int(self.height * y_percent)

        pyautogui.moveTo(x_pixel, y_pixel, duration=duration)

        pyautogui.click(x_pixel, y_pixel)

    def keyboard_type(text: str):
        """
        This function types the given text
        """
        text = text.replace("\\n", "\n")
        for char in text:
            pyautogui.write(char)
        
        pyautogui.press("enter")

    def capture_screen(self, filename):
        file_path = os.path.join(self.dir, filename)

        if self.platform == "Darwin":
            subprocess.run(["screencapture", "-C", file_path])
        elif self.platform == "Linux":
            # Use xlib to prevent scrot dependency for Linux
            screen = Xlib.display.Display().screen()
            size = screen.width_in_pixels, screen.height_in_pixels
            screenshot = ImageGrab.grab(bbox=(0, 0, self.width, self.height))
            screenshot.save(file_path)


class VisionModel:
    """
    Base Vision Model class for all vision models
    """

    def __init__(self, model: Models):
        self.model = model
        self.actions = Actions()

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

    def parse_response(self, messages: str) -> ActionInstance:
        """
        This function returns an action based on the response from the Vision Language Model
        """
        raise NotImplementedError("This method should be implemented by the subclass.")

    def execute_action(self, action: ActionInstance) -> str:
        """
        This function executes the action returned by the Vision Language Model
        """
        raise NotImplementedError("This method should be implemented by the subclass.")


class GPT4VModel(VisionModel):
    """
    This is the class for a Vision Language Model to solve tasks on a page
    """
    def __init__(self):
        super().__init__(Models.GPT4V)

    def get_main_prompt(self, objective: str):
        pass

    def get_next_action(self, messages: str):
        """
        This function gets the next action for the GPT4V Model
        """
        # send a request to GPT4V with messages