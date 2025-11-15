from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


MODEL = "gpt-4.1"
TEMPERATURE_FIRST = 0    
TEMPERATURE_REST = 0.1        
MAX_TOKENS = 750
NUM_DISKS = 4                 
K_THRESHOLD = 2              
USE_RED_FLAGGING = True       



