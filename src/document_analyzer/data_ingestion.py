import os
import sys
import fitz
from pathlib import Path
from datetime import datetime
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException


class DocumentHandler:

    """
    Handles PDF saving and reading operations
    Automatically logs all actions and supports session based organization
    """

    def __init__(self, data_dir=None, session_id=None):
        
        self.log = CustomLogger.get_logger(__name__)
        self.data_dir = data_dir or os.getenv('DATA_STORAGE_PATH', os.path.join(os.getcwd(),"data","document_analysis"))

        self.session_id = session_id or f"session_{datetime.strftime("%Y%m%d_%H_%M_%S")}.log"
        self.session_path = os.path.join(self.data_dir, self.session_id)
        os.makedirs(self.session_path,exist_ok=True)
        


    def save_pdf(self, uploaded_file):
        try:
            filename = os.path.basename(uploaded_file.name)

            if not filename.lower().endswith('.pdf'):
                ValueError("Invalid file type. Only PDF is allowed!")

            save_path = os.path.join(self.session_path, filename)
            with open(save_path, 'wb') as f:
                if hasattr(uploaded_file, "read"):
                    f.write(uploaded_file.read())
                else:
                    f.write(uploaded_file.getbuffer())
            
            self.log.info('PDF saved successfully', filename=filename, save_path=save_path, session_id=self.session_id)    

        except Exception as e:
            self.log.error(f"Error in saving PDF {e}")
            raise DocumentPortalException(f"An Error occured while saving PDF {str(e)}", e)
        

    def read_pdf(self, pdf_path):
        try:
            text_chunks=[]
            with fitz.open(pdf_path) as doc:
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    text_chunks.append(f'\n--------{page_num+1}------\n{page.get_text()}')
            text = '\n'.join(text_chunks)
            self.log.info("PDF read successfully", pdf_path = pdf_path, session_id = self.session_id, pages = len(text_chunks))
            return text
        except Exception as e:
            self.log.error(f"Error in reading PDF", error=str(e), pdf_path=pdf_path, session_id=self.session_id)
            raise DocumentPortalException(f"Could not read PDF {pdf_path}", e)