from __future__ import annotations
from enum import Enum

import platform
import os
import io
import subprocess
import traceback
import Xlib.display
from PIL import Image, ImageDraw, ImageFont, ImageGrab
try:
    import pyautogui
    pyautogui_installed = True
except Exception as e:
    print(f"Error importing pyautogui {e}")
    pyautogui_installed = False
from openai import OpenAI
from typing import List, Tuple
import base64
from dotenv import load_dotenv
import copy
from evaluation.prompts import text_vision_oracle_instructions, text_vision_ollava_instructions, few_shot_examples
from itertools import islice
import time
from transformers import AutoTokenizer
import torch
from transformers import LlavaNextProcessor, LlavaNextForConditionalGeneration

import requests
import json

# processor = LlavaNextProcessor.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf")
processor = LlavaNextProcessor.from_pretrained("llava-hf/llava-v1.6-vicuna-13b-hf")

model = LlavaNextForConditionalGeneration.from_pretrained("llava-hf/llava-v1.6-vicuna-13b-hf", torch_dtype=torch.float16, low_cpu_mem_usage=True) 
model.to("cuda:0")

class Models(Enum):
    GPT4V = 1
    OLlama = 2
    LlaVA = 3

class ActionInstance:
    def __init__(self, type: str, data: str, duration: int = None):
        self.type = type
        self.data = data
        self.duration = duration

class Actions:
    def __init__(self):
        self.platform = platform.system()

        # if (self.platform == "Darwin" or self.platform == "Windows"):
        if pyautogui_installed:
            self.width, self.height = pyautogui.size()

        self.dir = "screenshots"

    def click_percentage(self, x_percent: float, y_percent: float, duration: float = 0.2, circle_radius: int = 50, circle_duration: float = 0.5) -> str:
        """
        This function clicks on a percentage of the screen
        """
        if not pyautogui_installed:
            raise Exception("Pyautogui is not installed")

        x_pixel = int(self.width * x_percent)
        y_pixel = int(self.height * y_percent)

        pyautogui.moveTo(x_pixel, y_pixel, duration=duration)

        pyautogui.click(x_pixel, y_pixel)

        return "Successfully clicked"

    def keyboard_type(text: str) -> str:
        """
        This function types the given text
        """
        if not pyautogui_installed:
            raise Exception("Pyautogui is not installed")

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

    def draw_label_with_background(self, position: Tuple[int, int], text: str, draw, font):
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
        image_path = self.actions.capture_screen("screenshot.png")

        if False:
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
    
    def execute_click_instance(self, top_left: Tuple[int, int], bottom_right: Tuple[int, int], chosen: int, left: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
        top_left - tuple of the top left corner of the image we are currently considering
        bottom_right - tuple of the bottom right corner of the grid we are currently considering
        chosen - the grid number we chose
        left - number of iterations in the recursion that we need to continue
        """
        if left == 0: return (top_left, bottom_right)

        # figure out new top_left and bottom_right
        # crop out an image with those coordinates, explode it up in size, and get_next_action
        # call execute_click_instance out again with the new top_left and bottom_right and chosen coord
        pass

    def execute_action(self, action: ActionInstance) -> str:
        """
        This function executes the action returned by the Vision Language Model
        """
        
        assert action["type"] != "UNKNOWN" and action["type"] != "DONE", "Action type should not be UNKNOWN or DONE"

        match action["type"]:
            case "CLICK":
                return self.execute_click_instance(int(action["data"]))
            case "TYPE":
                return self.actions.keyboard_type(action["data"])
            case _:
                raise ValueError("This action type is not implemented yet.")

    def get_vision_text_baseline_action(self, input_name: str, html_code: str, image_path: str, num_demonstrations: int, use_relevant_html: bool) -> str:
        """
        This function is used in baselines for the text-vision benchmarks
        """
        raise NotImplementedError("This method should be implemented by the subclass.")

class OLlamaVisionModel(VisionModel):
    def __init__(self, model: str):
        super().__init__(Models.OLlama)
        self.model = model

    def get_main_prompt(self, objective: str) -> str:
        pass

    def get_vision_text_baseline_action(self, input_name: str, html_code: str, image_path: str, num_demonstrations: int, use_relevant_html: bool) -> str:
        with Image.open(image_path) as img:
            new_size = (int(img.width // 2.11), int(img.height // 2.11))
            resized_img = img.resize(new_size, Image.ANTIALIAS)

            buffer = io.BytesIO()
            resized_img.save(buffer, format="PNG")  
            img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        prompt = "\{\{" + text_vision_ollava_instructions() + "\}\}\nUSER: \{\{" + f"""
Input name: {input_name}
HTML:
{html_code}
ASSISTANT:"""
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "images": [img_base64],
            "stream": False 
        }

        response = requests.post(url, data=json.dumps(payload))
        model_response = (json.loads(response.text))["response"]
        print(f"OLlama Vision response {model_response}")

        return model_response

class GPT4VModel(VisionModel):
    """
    This is the class for a Vision Language Model to solve tasks on a page
    """
    def __init__(self):
        super().__init__(Models.GPT4V)
        load_dotenv()
        self.client = OpenAI(api_key = "" )
        self.log_dir = "logs"
        os.makedirs(self.log_dir, exist_ok=True)

    gpt_tokenizer = AutoTokenizer.from_pretrained("gpt2", max_length=1e5)

    # def count_tokens(self, s: str):
    #     tokens = self.gpt_tokenizer.tokenize(s)
    #     # GPT2 uses Byte-level BPE, which will include space as part of the word.
    #     # But for the first word of a sentence, there is no space before it.
    #     # So, we remove all the added spaces ("Ġ").
    #     tokens_unchanged = copy.deepcopy(tokens)
    #     tokens = [t.lstrip("Ġ") for t in tokens]
    #     return tokens_unchanged, tokens
    
    # def count_tokens(self, messages):
    #     total_tokens = []
    #     unchanged_tokens = []
        
    #     for message in messages:
    #         content = message.get('content', [])
    #         if isinstance(content, list):
    #             for item in content:
    #                 if 'text' in item:
    #                     tokens = self.gpt_tokenizer.tokenize(item['text'])
    #                     unchanged_tokens.extend(tokens)
    #                     total_tokens.extend([t.lstrip("Ġ") for t in tokens])
    #                 elif 'image_url' in item:
    #                     # Assuming base64 image URL length is considered, you can decide if you want to count it
    #                     tokens = self.gpt_tokenizer.tokenize(item['image_url']['url'])
    #                     unchanged_tokens.extend(tokens)
    #                     total_tokens.extend([t.lstrip("Ġ") for t in tokens])
    #         else:
    #             tokens = self.gpt_tokenizer.tokenize(content)
    #             unchanged_tokens.extend(tokens)
    #             total_tokens.extend([t.lstrip("Ġ") for t in tokens])
        
    #     return unchanged_tokens, len(total_tokens)

    def get_unique_filename(base_path: str, filename: str, extension: str) -> str:
        """
        Generate a unique filename by appending a number if the filename already exists.
        
        :param base_path: The directory where the file will be saved.
        :param filename: The base name of the file without extension.
        :param extension: The extension of the file (e.g., '.txt', '.png').
        :return: A unique filename with the format 'filename.extension' or 'filename_n.extension'.
        """
        full_path = os.path.join(base_path, f"{filename}{extension}")
        counter = 1
        
        while os.path.exists(full_path):
            full_path = os.path.join(base_path, f"{filename}_{counter}{extension}")
            counter += 1
        
        return full_path
    
    def save_token_data(self, unchanged_tokens, num_tokens, input_name, api_tokens):
        base_path = self.log_dir
        filename = f"{input_name}_tokens"
        extension = ".txt"
        
        file_path = self.get_unique_filename(base_path, filename, extension)
        
        with open(file_path, "w") as f:
            f.write(f"Token count: {num_tokens}\n\n")
            f.write(f"Token count from OpenAI call: {api_tokens}\n\n")
            f.write("\n".join(unchanged_tokens))
        
        return file_path

    def get_next_image_path(self):
        i = 1
        while os.path.exists(f"{self.log_dir}/screenshot_{i}.png"):
            i += 1
        return f"{self.log_dir}/screenshot_{i}.png"

    def save_html_code(self, html_code, input_name):
        file_path = f"{self.log_dir}/{input_name}_html.txt"
        with open(file_path, "w") as f:
            f.write(html_code)
        return file_path

    def save_messages(self, messages, input_name):
        file_path = f"{self.log_dir}/{input_name}_messages.json"
        with open(file_path, "w") as f:
            json.dump(messages, f, indent=4)
        return file_path

    def get_main_prompt(self, objective: str):
        pass

    def get_vision_text_baseline_action(self, input_name: str, html_code: str, image_path: str, num_demonstrations: int, use_relevant_html: bool) -> str:
        messages = [{
            "role": "assistant",
            "content": text_vision_oracle_instructions()
        }]

        for idx, instance in enumerate(islice(few_shot_examples(), num_demonstrations)):
            with Image.open(instance[1]) as img:
                new_size = (int(img.width // 2.11), int(img.height // 2.11))
                resized_img = img.resize(new_size, Image.ANTIALIAS)

                img_save_path = self.get_next_image_path()
                resized_img.save(img_save_path, format="PNG")

                buffer = io.BytesIO()
                resized_img.save(buffer, format="PNG")  
                img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

            user_message = {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": instance[3] if use_relevant_html else instance[0]
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{img_base64}"
                        }
                    }
                ]
            }

            assistant_message = {
                "role": "assistant",
                "content": instance[2]
            }

            messages.append(user_message)
            messages.append(assistant_message)


        with Image.open(image_path) as img:
            new_size = (int(img.width // 2.11), int(img.height // 2.11))
            resized_img = img.resize(new_size, Image.ANTIALIAS)

            buffer = io.BytesIO()
            resized_img.save(buffer, format="PNG")  
            img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        new_message = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"""
                        Input name: {input_name}
                        HTML:
                        {html_code}
                        """
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{img_base64}"
                    }
                }
            ]
        }

        messages.append(new_message)

        self.save_html_code(html_code, input_name)
        self.save_messages(messages, input_name)
        # unchanged_tokens, number_tokens = self.count_tokens(messages)

        fail_count = 0
        response = None 
        while fail_count < 20:
            try: 
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    temperature=1,
                    max_tokens=256,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )

                break
            except Exception as e:
                fail_count += 1
                time.sleep(30)
                print(f"Error getting action from GPT4V model {e}, trying again, current fail_count is {fail_count}")
        response_tokens = "None"
        try:
            response_tokens = response['usage']['total_tokens']
        except Exception as e:
            response_tokens = f"Error encountered - {e}"
        print(f"Response tokens - {response_tokens}")
        # self.save_token_data(unchanged_tokens, number_tokens, input_name, response_tokens)
        return response.choices[0].message.content

    def get_next_action(self, prev_messages: List[str], message: str, image_path: str) -> str:
        """
        This function gets the next action for the GPT4V Model
        """
        try:
            with Image.open(image_path) as img:
                new_size = (int(img.width // 2.11), int(img.height // 2.11))
                resized_img = img.resize(new_size, Image.ANTIALIAS)

                buffer = io.BytesIO()
                resized_img.save(buffer, format="JPEG")  
                img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
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
                model="gpt-4o",
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

class LLaVAModel(VisionModel):
    """
    This is the class for a Vision Language Model to solve tasks on a page
    """
    def __init__(self):
        super().__init__(Models.GPT4V)
        self.log_dir = "logs"

    def get_main_prompt(self, objective: str):
        pass

    def process_image(base64_image):
        # Decode the base64 image
        image_data = base64.b64decode(base64_image)
        image = Image.open(io.BytesIO(image_data))

        # Resize the image
        new_size = (int(image.width // 2.11), int(image.height // 2.11))
        resized_image = image.resize(new_size, Image.LANCZOS)

        # Convert the image to a format compatible with the model
        buffer = io.BytesIO()
        resized_image.save(buffer, format="PNG")
        resized_image = Image.open(buffer)

        return resized_image

    def get_vision_text_baseline_action(self, input_name: str, html_code: str, image_path: str, num_demonstrations: int, use_relevant_html: bool) -> str:
        messages = [{
            "role": "assistant",
            "content": [{
                            "type": "text",
                            "text": text_vision_oracle_instructions()
            }]
        }]

        for idx, instance in enumerate(islice(few_shot_examples(), num_demonstrations)):
            with Image.open(instance[1]) as img:
                new_size = (int(img.width // 2.11), int(img.height // 2.11))
                resized_img = img.resize(new_size, Image.ANTIALIAS)

                img_save_path = self.get_next_image_path()
                resized_img.save(img_save_path, format="PNG")

                buffer = io.BytesIO()
                resized_img.save(buffer, format="PNG")  
                img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

            user_message = {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": instance[3] if use_relevant_html else instance[0]
                    },
                    {
                        "type": "image"
                    }
                ]
            }

            assistant_message = {
                "role": "assistant",
                "content": instance[2]
            }

            messages.append(user_message)
            messages.append(assistant_message)


        with Image.open(image_path) as img:
            new_size = (int(img.width // 2.11), int(img.height // 2.11))
            resized_img = img.resize(new_size, Image.ANTIALIAS)

            buffer = io.BytesIO()
            resized_img.save(buffer, format="PNG")  
            # img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            img_base64 = buffer.getvalue()

        new_message = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"""
                        Input name: {input_name}
                        HTML:
                        {html_code}\n
                        Give the response with a valid command beginning with self.actions for input name {input_name}, NOTHING ELSE. Provide both input name and input value in the command. No other text. The end of your answer should be the end of the command.
                        """
                },
                {
                    "type": "image"
                }
            ]
        }

        # Process the image
        image = Image.open(image_path)

        messages.append(new_message)
        
        # self.save_html_code(html_code, input_name)
        # self.save_messages(messages, input_name)
        # unchanged_tokens, number_tokens = self.count_tokens(messages)
        print(messages)
        fail_count = 0
        response = None 
        while fail_count < 20:
            try:
                prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
                # print(prompt)
                inputs = processor(prompt, image, return_tensors="pt").to("cuda:0")
                output = model.generate(**inputs, max_new_tokens=100)
                # print(inputs)
                # print(output)
                answer = (processor.decode(output[0], skip_special_tokens=True)).split('ASSISTANT:')[-1].strip()
                print(f"FINAL LLAVA RESPONSE = {answer}")
                break
            except Exception as e:
                fail_count += 1
                time.sleep(30)
                print(f"Error getting action from Llava model {e}, trying again, current fail_count is {fail_count}")
                print(traceback.format_exc())
        response_tokens = "None"
        # try:
        #     response_tokens = response['usage']['total_tokens']
        # except Exception as e:
        #     response_tokens = f"Error encountered - {e}"
        # print(f"Response tokens - {response_tokens}")
        # self.save_token_data(unchanged_tokens, number_tokens, input_name, response_tokens)
        return answer

    def get_next_action(self, prev_messages: List[str], message: str, image_path: str) -> str:
        """
        This function gets the next action for the GPT4V Model
        """
        return "None"
        # try:
        #     with Image.open(image_path) as img:
        #         new_size = (int(img.width // 2.11), int(img.height // 2.11))
        #         resized_img = img.resize(new_size, Image.ANTIALIAS)

        #         buffer = io.BytesIO()
        #         resized_img.save(buffer, format="JPEG")  
        #         img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        # except Exception as e:
        #     print(f"Error getting image {e}")
        
        # messages = copy.deepcopy(prev_messages)
        # messages.append({
        #     "role": "user",
        #     "content": [
        #         {"type": "text", "text": message},
        #         {
        #             "type": "image_url",
        #             "image_url": {
        #                 "url": f"data:image/jpeg;base64,{img_base64}"
        #             }
        #         }
        #     ]
        # })

        # try:
        #     response = self.client.chat.completions.create(
        #         model="gpt-4o",
        #         messages=messages,
        #         temperature=0,
        #         max_tokens=300,
        #     )

        #     content = response.choices[0].message.content
        # except Exception as e:
        #     print(f"Error getting action from GPT4V model {e}")

        # return content
    
    def parse_response(self, message: str) -> ActionInstance:
        """
        This function parses the response from the GPT4V Model
        """
        pass

if __name__ == "__main__":
    model = OLlamaVisionModel(model="llava")
    model.main("test")