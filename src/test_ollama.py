from __future__ import annotations

import platform
import os
import io
import subprocess
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
from evaluation.prompts import text_vision_oracle_instructions, few_shot_examples
from itertools import islice
import time

import requests
import json

class OLlamaVisionModel():
    def __init__(self, model: str):
        self.model = model

    def get_vision_text_baseline_action(self, input_name: str, html_code: str, image_path: str, num_demonstrations: int, use_relevant_html: bool) -> str:
        with Image.open(image_path) as img:
            new_size = (int(img.width // 2.11), int(img.height // 2.11))
            resized_img = img.resize(new_size, Image.ANTIALIAS)

            buffer = io.BytesIO()
            resized_img.save(buffer, format="PNG")  
            img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        prompt = f"""
                {text_vision_oracle_instructions()}
                Input name: {input_name}
                HTML:
                {html_code}
                """
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "images": [img_base64],
            "stream": False 
        }

        response = requests.post(url, data=json.dumps(payload))
        model_response = (json.loads(response.text))["response"]
        print(f"OLlama response {model_response}")

        return model_response

if __name__ == "__main__":
    model = OLlamaVisionModel(model="llava")