import base64
from anthropic import Anthropic
from pathlib import Path

# MODEL_NAME = "claude-3-opus-20240229"




def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as image_file:
        binary_data = image_file.read()
        base_64_encoded_data = base64.b64encode(binary_data)
        base64_string = base_64_encoded_data.decode('utf-8')
        return base64_string
    


def ocr_anthropic(image_strin:base64,api_key,prompt:str,MODEL_NAME:str):
    client = Anthropic(api_key=api_key)

    message_list = [
                        {
                            "role": 'user',
                            "content": [
                                {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": image_strin}},
                                {"type": "text", "text": prompt}
                                #"Transcribe this text. Only output the text and nothing else."
                            ]
                        }
                    ]

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=4000,
        messages=message_list
    )
    
    total_tokens = response.usage.input_tokens + response.usage.output_tokens
    return response.content[0].text , total_tokens
   



