import streamlit as st
import os
import uuid
from src.utils import *
from src.globals import *
import time
from src.documentsai import ocr_doc
from src.anthropic import get_base64_encoded_image,ocr_anthropic
from src.openai import encode_image,openai_ocr
from src.comparision import all_ocr_output,merge_documents_with_llm
from dotenv import load_dotenv
from google.oauth2 import service_account
from PIL import Image
import asyncio




st.set_page_config(page_title="PDF Process",
                   layout="centered",
                   initial_sidebar_state='collapsed',
                   )



def Home():
    load_dotenv()
    PROJECT_ID = os.getenv('PROJECT_ID')
    LOCATION =  os.getenv('LOCATION')  
    PROCESSOR_ID = os.getenv('PROCESSOR_ID') 
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    OPEN_AI_KEY = os.getenv('OPEN_AI_KEY')
   
    credentials = service_account.Credentials.from_service_account_info(st.secrets["gcs_connections"])

    uploaded_file = st.file_uploader("Choose a file...", type=["pdf"])

    if uploaded_file is not None:
        File_Dir_Path.pdf_folder_dir,File_Dir_Path.Extracted_Image_dir,File_Dir_Path.Extracted_txt_dir,File_Dir_Path.Zip_File_Dir = create_folders()

        delete_existing_files(File_Dir_Path.Extracted_Image_dir)
        delete_existing_files(File_Dir_Path.pdf_folder_dir)
        delete_existing_files(File_Dir_Path.Extracted_txt_dir)
        delete_existing_files(File_Dir_Path.Zip_File_Dir)

        if st.button(label="Submit",use_container_width=True):

        
               

                save_pdf_file_path = os.path.join(File_Dir_Path.pdf_folder_dir,uploaded_file.name)

                with open(save_pdf_file_path, "wb") as f:
                   f.write(uploaded_file.getbuffer())

                extract_image(save_pdf_file_path,File_Dir_Path.Extracted_Image_dir)
                list_images = get_all_images_paths_list(File_Dir_Path.Extracted_Image_dir)
                print(list_images)

             
                with st.container(border=True):
                    progress_bar = st.progress(0)
                with st.container(border=True):
                    st.info(f"Total number of pages in pdf file is {Count_Entity.Page_count_pdf}")
                    st.info(f"Total number of images in a extraced folder is {count_all_files(File_Dir_Path.Extracted_Image_dir)}")


                
                    

                for k,i in enumerate(list_images):
                        
                       
                        print(k,i)
                        status_text =f"OCR Processing...... {k + 1}/{Count_Entity.Page_count_pdf}"
                        progress_bar.progress(int(((k + 1)/(Count_Entity.Page_count_pdf))*100),text=status_text)
                        promt_txt=Prompt_txt_ocr
                        start_time = time.time()
                        t1,accuracy_docai = ocr_doc(
                                        PROJECT_ID=PROJECT_ID,
                                        LOCATION=LOCATION,
                                        PROCESSOR_ID=PROCESSOR_ID,
                                        FILE_PATH=i,
                                        credentials=credentials

                                    )
                       
                        
                        if int(accuracy_docai) > 80:
                            
                            t2,t3,tt_open,tt_anthropic = all_ocr_output(
                                                            
                                                            imgbase64_openai= f"data:image/png;base64,{encode_image(i)}",
                                                            imgbase64_anthropic=get_base64_encoded_image(i),
                                                            openai_key= OPEN_AI_KEY,
                                                            antropic_api= ANTHROPIC_API_KEY,
                                                            prompt=promt_txt,
                                                            openai_model="gpt-4o",
                                                            anthropic_model="claude-3-5-sonnet-20240620"
                                                           
                                                        )
                                            
                            resluts,token_oprn=merge_documents_with_llm(t1,t2,t3,OPEN_AI_KEY)
                            base_name = os.path.splitext(os.path.basename(i))[0]
                            write_txt_to_folder(File_Dir_Path.Extracted_txt_dir,base_name,resluts)
                            end_time = time.time()
                            elapsed_time_sec = end_time - start_time
    
                            # Convert to minutes and seconds
                            minutes = int(elapsed_time_sec // 60)
                            seconds = elapsed_time_sec % 60
                            with st.container(border=True):
                                 
                              st.success(f"Accuracy for page number {k+1} is {accuracy_docai:.2f} %",icon=":material/thumb_up:")
                              st.write(f"Time elapsed: {f'{minutes} min {seconds:.2f} sec' if minutes > 0 else f'{seconds:.2f} seconds'} || OpenAI's Total token: {tt_open+token_oprn}, Anthropic Toekn : {tt_anthropic}")
                              
                        else:
                              end_time = time.time()
                              elapsed_time_sec = end_time - start_time
    
                            # Convert to minutes and seconds
                              minutes = int(elapsed_time_sec // 60)
                              seconds = elapsed_time_sec % 60
                              with st.container(border=True):
                                st.error(f"Accuracy for page number {k+1} is {accuracy_docai:.2f} % ",icon="🔥")
                                st.warning(f"Please review the file manually, Page number is {k+1} of the file {uploaded_file.name}",icon="🚨")   
                                st.write(f"Time elapsed: {f'{minutes} min {seconds:.2f} sec' if minutes > 0 else f'{seconds:.2f} seconds'}")

                        
                countfile = count_all_files(File_Dir_Path.Extracted_txt_dir)
                if countfile > 0:
                    Zip_File_Name = os.path.join(File_Dir_Path.Zip_File_Dir,"zipoutput.zip")
                    zip_folder(File_Dir_Path.Extracted_txt_dir,Zip_File_Name)
                    with st.container(border=True):
                        st.info(f"Total number of Txt Files in a extraced folder is {countfile}") 
                        with open(Zip_File_Name, "rb") as fp:
                                st.download_button(
                                label="Download ZIP",
                                data=fp,
                                file_name="zipoutput.zip",
                                mime="application/zip",
                                use_container_width=True
                            )
                    

                # st.balloons()      
                    
            
            
            

        



if __name__ == '__main__':

    Home()        
