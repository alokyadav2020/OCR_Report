from src.anthropic import ocr_anthropic
from src.openai import openai_ocr
from src.documentsai import ocr_doc
from openai import OpenAI



def all_ocr_output(imgbase64_openai,imgbase64_anthropic,openai_key,antropic_api,prompt,openai_model,anthropic_model):

    

    ocr_by_openai, Ttokaen_openai = openai_ocr(imgbase64_openai,openai_key,models=openai_model,prompt=prompt)

    # print(ocr_by_openai)

    ocr_by_anthropic,Ttokaen_anthropic=ocr_anthropic(imgbase64_anthropic,antropic_api,MODEL_NAME=anthropic_model,prompt=prompt)

    

    return  ocr_by_openai, ocr_by_anthropic ,Ttokaen_openai,Ttokaen_anthropic




ptm=""" 
I have three OCR outputs from the same document. Each OCR result may have missing sentences, incorrect text, or variations in formatting. 
I want you to analyze the three versions and create one perfect document by combining all the accurate and missing content.

 Your task is to:
    - Identify missing sentences or text in any of the documents.
    - Resolve inconsistencies or differences.
    - Combine all the content into one coherent, accurate document.
    - Ensure that the final document is well-formatted and complete.

    Please return the merged document. Nothing else.


"""


# Your OpenAI API key
# openai.api_key = 'your-api-key'

# Function to call OpenAI API with the documents and prompt
def merge_documents_with_llm(doc1, doc2, doc3,openai_key,Usr_pmt=ptm):
    prompt_user = f"""

    {Usr_pmt}
    

    Here are the documents:

    1. Document 1:
    {doc1}

    2. Document 2:
    {doc2}

    3. Document 3:
    {doc3}

   
    
    """
    
    # # Call OpenAI API
    # response = openai.Completion.create(
    #     engine="GPT-4o",  # Use a GPT-3.5 model
    #     prompt=prompt,
    #     max_tokens=5990,  # Adjust max_tokens based on your needs
    #     temperature=0.2  # Low temperature for a more deterministic output
    #)

    client = OpenAI(api_key=openai_key)

    completion = client.chat.completions.create(
                                                    model="gpt-4o",
                                                    messages=[
                                                        {"role": "system", "content": "You are a helpful assistant."},
                                                        {
                                                            "role": "user",
                                                            "content": prompt_user
                                                        }
                                                    ]
                                                )
    result = completion.choices[0].message.content
    total_token = completion.usage.total_tokens
    return result,total_token


