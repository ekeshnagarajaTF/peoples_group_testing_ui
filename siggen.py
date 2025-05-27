import hmac 
import hashlib 
import time 
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_signature(): 

    api_key = os.getenv('API_KEY') 
    api_secret = os.getenv('API_SECRET')
    timestamp = str(int(time.time()))
    

    message = f"{timestamp}|{api_key}" 
    # Create the HMAC-SHA256 signature 
    signature = hmac.new( 
        api_secret.encode(), 
        message.encode(), 
        hashlib.sha256 
    ).hexdigest() 
    print(f"Signature: {signature}")
    print(f"Timestamp: {timestamp}")

    return signature, timestamp

  