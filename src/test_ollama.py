from __future__ import annotations

import os
import io
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageGrab
from typing import List, Tuple, Union, Literal
import base64
from dotenv import load_dotenv
import copy
from evaluation.prompts import text_oracle_instructions, text_vision_oracle_instructions, few_shot_examples
from itertools import islice
import time
from pydantic import BaseModel

import requests
import json

class OLlamaTextModel():
    def __init__(self, model: str):
        self.model = model

    def get_text_baseline_action(self, input_name: str, html_code: str, num_demonstrations: int, use_relevant_html: bool) -> str:
        if num_demonstrations == 0:
            return ""

        prompt = f"""
<s> [INST] <<SYS>>
{text_oracle_instructions()}
<</SYS>>        
{few_shot_examples()[0][3] if use_relevant_html else few_shot_examples()[0][0]}[/INST]
{few_shot_examples()[0][2]}</s>
"""
        for idx, instance in enumerate(islice(few_shot_examples(), num_demonstrations)):
            if idx == 0:
                continue
            prompt += f"""
<s> [INST] {instance[3] if use_relevant_html else instance[0]} [/INST] {instance[2]}</s>
""" 

        prompt += f"""
<s> [INST]
Input name: {input_name}
HTML:
{html_code}
[/INST]
"""
        
        print(f"Prompt: {prompt}")

        url = "http://localhost:11434/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False 
        }

        response = requests.post(url, data=json.dumps(payload))
        model_response = (json.loads(response.text))["response"]
        print(f"OLlama response {model_response}")

        return model_response

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
    model = OLlamaTextModel(model="llama2")
    input_name = "weakener_rationale1_relevant"
    relevant_html = """
HTML:
        <input id="weakener_rationale1_understandable" name="weakener_rationale1_gibberish_understandable_grammatical" onclick="toggle_gibberish('weakener_rationale1')" type="radio" value="understandable"> <label for="understandable">The rationale is not perfectly grammatical, but I can understand it.</label><br>
        <input id="weakener_rationale1_grammatical" name="weakener_rationale1_gibberish_understandable_grammatical" onclick="toggle_gibberish('weakener_rationale1')" type="radio" value="grammatical" checked=""> <label for="grammatical">The rationale is grammatical.</label></div>
        </td>
      </tr>
      <tr>
        <td><input id="weakener_rationale1_relevant" name="weakener_rationale1_relevant" type="checkbox" checked=""> The rationale is on topic with respect to the premise and hypothesis.</td>
      </tr>
      <tr>
        <td><input id="weakener_rationale1_correct" name="weakener_rationale1_correct" type="checkbox"> The rationale is factually correct or likely true.</td>
      </tr>
      <tr>
        <td><input id="weakener_rationale1_explains" name="weakener_rationale1_explains" type="checkbox"> The rationale may explain why the rationale weakens the hypothesis.</td>
      </tr>
    </tbody>
  </table>
"""
    res = model.get_text_baseline_action(input_name, relevant_html, 3, True)