from anthropic import AI_PROMPT, HUMAN_PROMPT, AnthropicBedrock
import os
from dotenv import load_dotenv

load_dotenv()
aws_secret_key = os.getenv("AWS_SECRET_KEY")
aws_access_key = os.getenv("AWS_ACCESS_KEY")

client = AnthropicBedrock(aws_access_key=aws_access_key, aws_secret_key=aws_secret_key, aws_region="us-east-1")

system = f"""<instructions>
Please only give the location of universities when asked.
</instructions>\n
"""
prompt = f"{system}{HUMAN_PROMPT} hey! can you tell me what you know about Johns Hopkins?{AI_PROMPT}It is a university located in Baltimore. {HUMAN_PROMPT} What can you tell me about Harvard? {AI_PROMPT}"

completion = client.completions.create(
    model="anthropic.claude-v2:1",
    prompt=prompt,
    stop_sequences=[HUMAN_PROMPT],
    max_tokens_to_sample=100000,
    temperature=0.5,
    top_k=250,
    top_p=0.5,
)
print(completion.completion)