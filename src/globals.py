from dataclasses import dataclass
from pathlib import Path


############################################# Out Folder and File Path ###############################

@dataclass(frozen=True)
class File_Dir_Path:

    pdf_process_dir:Path 
    pdf_folder_dir:Path 
    Extracted_Image_dir:Path
    Extracted_txt_dir:Path 
    Zip_File_Dir:Path



############################################# File and Page Count Variable ###############################


@dataclass
class Count_Entity:

    Page_count_pdf:int

    Total_Image_count:int





Prompt_txt_ocr = """ 

Perform OCR on the following document. The document may contain either *handwritten cursive text* or *printed text*. 

Follow the instructions based on the type of content:  

1. *If the document contains handwritten cursive text*:    
 - Recognize and extract the *handwritten cursive content* with high accuracy.    
 - Pay attention to the connected and flowing nature of cursive handwriting.    
 - Preserve the structure and context of the handwritten sections.    
 - Handle any ambiguous or unclear characters by using the surrounding context.     
- Focus on capturing subtle details of inconsistent handwriting, ensuring clarity in transcription.  

2. *If the document contains printed text*:     
- Recognize and extract the *printed text* with high precision.     
- Preserve the formatting, including any spacing, line breaks, and other structural elements of the printed document.     
- Ensure accuracy in character recognition, especially in densely printed areas or where noise may be present.    
- Handle any distortions or imperfections in the image to ensure a clean extraction of the printed text.  

For both types of content:
 - Return the extracted text only in a structured format, maintaining the original layout and line breaks where applicable.  
- Do not give page number. 
- Return Text only nothing  else.

"""





