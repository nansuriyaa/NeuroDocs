import os
import sys
from pathlib import Path
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger


class DocumentAnalyzer:
    """
    Analyzes documents using a pre-trained model
    Automatically logs all actions and supports session based organization
    """
    def __init__(self):
        try:
            self.log = CustomLogger.get_logger(__name__)
        except Exception as e:
            pass

