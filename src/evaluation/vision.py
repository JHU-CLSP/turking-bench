from __future__ import annotations
from enum import Enum

import platform
import os
import subprocess
import Xlib.display
from PIL import Image, ImageDraw, ImageFont, ImageGrab
import pyautogui
from openai import OpenAi
from typing import List
import base64
from dotenv import load_dotenv
import copy

class Models(Enum):
    GPT4V = 1

class ActionInstance:
    def __init__(self, type: str, data: str, duration: int = None):
        self.type = type
        self.data = data
        self.duration = duration

class Actions:
    def __init__(self):
        self.platform = platform.system()

        if (self.platform == "Darwin" or self.platform == "Windows"):
            self.width, self.height = pyautogui.size()

        self.dir = "screenshots"

    def click_percentage(self, x_percent: float, y_percent: float, duration: float = 0.2, circle_radius: int = 50, circle_duration: float = 0.5) -> str:
        """
        This function clicks on a percentage of the screen
        """
        x_pixel = int(self.width * x_percent)
        y_pixel = int(self.height * y_percent)

        pyautogui.moveTo(x_pixel, y_pixel, duration=duration)

        pyautogui.click(x_pixel, y_pixel)

        return "Successfully clicked"

    def keyboard_type(text: str) -> str:
        """
        This function types the given text
        """
        text = text.replace("\\n", "\n")
        for char in text:
            pyautogui.write(char)
        
        pyautogui.press("enter")

        return "Successfully typed"

    def capture_screen(self, filename: str) -> str:
        """
        Capture a screenshot of the current screen

        Return: Path to the screenshot
        """
        file_path = os.path.join(self.dir, filename)

        if self.platform == "Darwin":
            subprocess.run(["screencapture", "-C", file_path])
        elif self.platform == "Linux":
            # Use xlib to prevent scrot dependency for Linux
            screen = Xlib.display.Display().screen()
            size = screen.width_in_pixels, screen.height_in_pixels
            screenshot = ImageGrab.grab(bbox=(0, 0, self.width, self.height))
            screenshot.save(file_path)
        
        return file_path

    def draw_label_with_background(self, position: tuple, text: str, draw, font):
        """
        Draws some text on the picture
        """
        fill_color = "green"
        draw.text(position, text, fill=fill_color, font=font, anchor="mm")

    def add_grid_to_image(self, old_image: str, new_image: str, num_grids: int = 1) -> str:
        """
        This function adds a grid to the image

        Return: the path to the new image
        """

        old_path = os.path.join(self.dir, old_image)
        new_path = os.path.join(self.dir, new_image)

        image = Image.open(old_path)

        draw = ImageDraw.Draw(image)

        width, height = image.size
        print(f"width: {width}, height: {height} self.width: {self.width}, self.height: {self.height}")
        font_size = int(height/40)
        
        font = ImageFont.truetype("arial.ttf", font_size)

         # Calculate the background size based on the font size
        bg_width = int(font_size * 1.2)  # Adjust as necessary
        bg_height = int(font_size * 1.2)  # Adjust as necessary

        for x in range(0, num_grids):
            for y in range(0, num_grids):
                x_coord = x * (width/num_grids) + (width/num_grids)/2 - bg_width/2
                y_coord = y * (height/num_grids) + (height/num_grids)/2 - bg_height/2

                # Calculate the percentage of the width and height
                self.draw_label_with_background(
                    (x_coord, y_coord),
                    f"{x * num_grids + y}",
                    draw,
                    font
                )

        for x in range(0, num_grids):
            width_multiplier = width/num_grids;
            line = ((x * width_multiplier, 0), (x * width_multiplier, height))
            draw.line(line, fill="blue")

        for y in range(0, num_grids):
            height_multiplier = height/num_grids;
            line = ((0, y * height_multiplier), (width, y * height_multiplier))
            draw.line(line, fill="blue")
        
        # Save the image with the grid
        image.save(new_path)

        return new_path

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

        Params:
        objective - User inputted objective
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

        if False:
            while True:
                try:
                    response = self.get_next_action(messages)
                    action = self.parse_response(response)

                    assert "type" in action and "data" in action, "Action should have a type and data"
                except Exception as e:
                    print(f"Error getting next action and parsing the response {e}")
                    break

                if action["type"] == "DONE" or action["type"] == "UNKNOWN":
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
    
    def get_next_action(self, messages: List[str], image_path: str) -> str:
        """
        This function gets the response from the VLM
        """
        raise NotImplementedError("This method should be implemented by the subclass.")

    def parse_response(self, message: str) -> ActionInstance:
        """
        This function returns an action based on the response from the Vision Language Model
        """
        raise NotImplementedError("This method should be implemented by the subclass.")
    
    def execute_initial_click(self, action_data: str):
        """
        This function executes the initial click
        """
        pass

    def execute_action(self, action: ActionInstance) -> str:
        """
        This function executes the action returned by the Vision Language Model
        """
        
        assert action["type"] != "UNKNOWN" and action["type"] != "DONE", "Action type should not be UNKNOWN or DONE"

        match action["type"]:
            case "CLICK":
                return self.execute_initial_click(action["data"])
            case "TYPE":
                return self.actions.keyboard_type(action["data"])
            case _:
                raise ValueError("This action type is not implemented yet.")

class GPT4VModel(VisionModel):
    """
    This is the class for a Vision Language Model to solve tasks on a page
    """
    def __init__(self):
        super().__init__(Models.GPT4V)
        load_dotenv()
        self.client = OpenAi(os.getenv("OPENAI_API_KEY"))

    def get_main_prompt(self, objective: str):
        pass

    def get_next_action(self, prev_messages: List[str], message: str, image_path: str) -> str:
        """
        This function gets the next action for the GPT4V Model
        """
        try:
            with open(image_path, "rb") as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode("utf-8")
        except Exception as e:
            print(f"Error getting image {e}")
        
        messages = copy.deepcopy(prev_messages)
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": message},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{img_base64}"
                    }
                }
            ]
        })

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=messages,
                temperature=0,
                max_tokens=300,
            )

            content = response.choices[0].message.content
        except Exception as e:
            print(f"Error getting action from GPT4V model {e}")

        return content
    
    def parse_response(self, message: str) -> ActionInstance:
        """
        This function parses the response from the GPT4V Model
        """
        pass

if __name__ == "__main__":
    model = GPT4VModel()
    model.main("test")