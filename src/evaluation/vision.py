from __future__ import annotations
from enum import Enum

import platform
import os
import subprocess
import Xlib.display
from PIL import Image, ImageDraw, ImageFont, ImageGrab
import pyautogui

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

    def capture_screen(self, filename: str):
        file_path = os.path.join(self.dir, filename)

        if self.platform == "Darwin":
            subprocess.run(["screencapture", "-C", file_path])
        elif self.platform == "Linux":
            # Use xlib to prevent scrot dependency for Linux
            screen = Xlib.display.Display().screen()
            size = screen.width_in_pixels, screen.height_in_pixels
            screenshot = ImageGrab.grab(bbox=(0, 0, self.width, self.height))
            screenshot.save(file_path)

    # Function to draw text with a white rectangle background
    def draw_label_with_background(self, position: tuple, text: str, draw, font):
        # Draw the text
        fill_color = "green"
        draw.text(position, text, fill=fill_color, font=font, anchor="mm")

    def add_grid_to_image(self, old_image: str, new_image: str, num_grids: int = 1):
        """
        This function adds a grid to the image
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

        if False:
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

        self.actions.capture_screen("screenshot.png")
        self.actions.add_grid_to_image("screenshot.png", "screenshot_grid.png", 4)
            
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

if __name__ == "__main__":
    model = GPT4VModel()
    model.main("test")