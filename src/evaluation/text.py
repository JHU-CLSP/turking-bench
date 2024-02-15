from enum import Enum
from dotenv import load_dotenv
from openai import OpenAI
from evaluation.prompts import text_oracle_instructions, few_shot_examples
from itertools import islice
import time
import os
from anthropic import AI_PROMPT, HUMAN_PROMPT, AnthropicBedrock

class Models(Enum):
    GPT4 = 1
    OLlama = 2
    Claude = 3

class TextModel:
    def __init__(self, model: Models):
        self.model = model

    def get_text_baseline_action(self, input_name: str, html_code: str, num_demonstrations: int, use_relevant_html: bool) -> str:
        """
        This function is used in baselines for the text-vision benchmarks
        """
        raise NotImplementedError("This method should be implemented by the subclass.")

class GPT4Model(TextModel):
    def __init__(self):
        super().__init__(Models.GPT4)
        load_dotenv()
        self.client = OpenAI()

    def get_text_baseline_action(self, input_name: str, html_code: str, num_demonstrations: int, use_relevant_html: bool) -> str:
        messages = [{
            "role": "assistant",
            "content": text_oracle_instructions()
        }]

        for idx, instance in enumerate(islice(few_shot_examples(), num_demonstrations)):
            user_message = {
                "role": "user",
                "content": instance[3] if use_relevant_html else instance[0]
            }

            assistant_message = {
                "role": "assistant",
                "content": instance[2]
            }

            messages.append(user_message)
            messages.append(assistant_message)


        new_message = {
            "role": "user",
            "content": f"""
                        Input name: {input_name}
                        HTML:
                        {html_code}
                        """
        }

        messages.append(new_message)

        fail_count = 0
        response = None 
        while fail_count < 20:
            try: 
                response = self.client.chat.completions.create(
                    model="gpt-4-turbo-preview",
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
                print(f"Error getting action from GPT4 model {e}, trying again, current fail_count is {fail_count}")

        print(f"OpenAI Response: {response.choices[0].message.content}")
        return response.choices[0].message.content

class OLlamaTextModel(TextModel):
    def __init__(self):
        super().__init__(Models.OLlama)

    def get_text_baseline_action(self, input_name: str, html_code: str, num_demonstrations: int, use_relevant_html: bool) -> str:
        pass

class ClaudeTextModel(TextModel):
    def __init__(self):
        super().__init__(Models.Claude)
        load_dotenv()
        aws_secret_key = os.getenv("AWS_SECRET_KEY")
        aws_access_key = os.getenv("AWS_ACCESS_KEY")
        self.client = AnthropicBedrock(aws_access_key=aws_access_key, aws_secret_key=aws_secret_key, aws_region="us-east-1")

    def get_text_baseline_action(self, input_name: str, html_code: str, num_demonstrations: int, use_relevant_html: bool) -> str:
        system_instruction = f"""<instructions>
        {text_oracle_instructions()}
        </instructions>\n
        """

        prompt = system_instruction

        for idx, instance in enumerate(islice(few_shot_examples(), num_demonstrations)):
            prompt += f"{HUMAN_PROMPT}{instance[3] if use_relevant_html else instance[0]}{AI_PROMPT}{instance[2]}"


        new_message = f"""
                        Input name: {input_name}
                        HTML:
                        {html_code}
                        """
        prompt += f"{HUMAN_PROMPT}{new_message}{AI_PROMPT}"

        fail_count = 0
        response = None 
        while fail_count < 20:
            try: 
                completion = self.client.completions.create(
                    model="anthropic.claude-v2:1",
                    prompt=prompt,
                    stop_sequences=[HUMAN_PROMPT],
                    max_tokens_to_sample=100000,
                    temperature=0.5,
                    top_k=250,
                    top_p=0.5,
                )
                break
            except Exception as e:
                fail_count += 1
                time.sleep(30)
                print(f"Error getting action from Claude model {e}, trying again, current fail_count is {fail_count}")

        print(f"Claude response: {completion.completion}")
        return completion.completion