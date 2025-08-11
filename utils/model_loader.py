import os
import sys
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from utils.config_loader import load_config
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
log = CustomLogger().get_logger(__name__)


class ModelLoader:

    """ 
    A utility class to load embedding models and LLM models 
    """

    def __init__(self):

        load_dotenv()
        self._validate_env()
        self.config = load_config()
        log.info("Configuration Loaded successfully!", config_keys=list(self.config.keys()))


    def _validate_env(self):

        """
        Validating necessary environmental variables.
        Ensuring API Keys exists.
        """

        required_vars = ["GOOGLE_API_KEY", "GROQ_API_KEY", "OPENAI_API_KEY"]
        self.api_keys = {key: os.getenv(key) for key in required_vars}
        missing = [k for k, v in self.api_keys.items() if not v]
        
        if missing:
            log.error("Necessary environmental variables are missing", missing_vars = missing)
            raise DocumentPortalException("Missing environmental variables", sys)
        
        available_keys = [keys for keys, value in self.api_keys.items() if value]
        
        log.info("Environmental variables validated", available_keys = [keys for keys, value in self.api_keys.items() if value])


    def load_embedding(self):
        
        """
        Load and return the embedding model
        Load embedding model dynamically based on provider in config
        """

        try:
            log.info("Loading embedding model....")
            
            embedding_block = self.config["embedding_model"]

            embedding_model_provider = os.getenv("EMBEDDING_PROVIDER", "google")

            if embedding_model_provider not in embedding_block:
                log.error("Embedding model provider not in config", embedding_model_provider = embedding_model_provider)
                raise DocumentPortalException(f"Embedding model provider {embedding_model_provider} not in config")

            embedding_config = embedding_block[embedding_model_provider]
            embedding_model_name = embedding_config["model_name"]

            print("Embedding loaded....")

            if embedding_model_provider == 'google':
                return GoogleGenerativeAIEmbeddings(
                    model_name = embedding_model_name
                )
            else:
                return OpenAIEmbeddings(
                    model_name = embedding_model_name
                )
            
            
            
        except Exception as e:
            
            log.error("Error loading embedding model", error = str(e))
            raise DocumentPortalException("Failed to load embedding model", sys)



    def load_llm(self):
        """
        Load and return the llm model
        Load llm dynamically based on provider in config
        """
        try:
            
            llm_block = self.config['llm']
            
            llm_provider_key = os.getenv('LLM_PROVIDER', 'google')

            if llm_provider_key not in llm_block:
                log.error(f'LLM Provider key not found in config', llm_provider_key=llm_provider_key)
                raise DocumentPortalException(f"LLM Provider {llm_provider_key} not found in config", sys)

            llm_config = llm_block[llm_provider_key]
            provider = llm_config.get("provider")
            model_name = llm_config.get("model_name")

            log.info(f"Loading llm model {model_name}")

            if provider == "google":
                return ChatGoogleGenerativeAI(
                    model_name = model_name
                )
            elif provider == "openai":
                return ChatOpenAI(
                    model_name = model_name
                )
            else:
                return ChatGroq(
                    model_name = model_name
                )

        except Exception as e:
            
            log.exception(f"Failed to load LLM: {str(e)}")
            raise DocumentPortalException("Failed to load LLM", sys)



if __name__ == "__main__":
    print("hello World!")
    obj = ModelLoader()

    print("Loading Embedding models.....")
    obj.load_embedding()

