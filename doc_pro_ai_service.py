import requests
import time
import hashlib
import hmac
from siggen import generate_signature

def get_signature() -> str:
    """Generate signature using HMAC SHA-256."""
   
    return generate_signature();

def send_document_to_ai_service(file_path: str, api_key: str, instruction_id: str = '1') -> dict:
    """
    Send document to AI service for processing.
    
    Args:
        file_path (str): Path to the document file
        api_key (str): API key for authentication
        instruction_id (str): Instruction ID for processing (default: '1')
    
    Returns:
        dict: Response from the API
    """
    # API endpoint
    url = "https://peoplesgroup-client-api.vector.yanaimpl.com/api/v1/doc-pro-ai-service-synchronous"
    
    
    # Generate signature
    signature , timestamp = get_signature()
    
    # For debugging
    print(f"Using signature: {signature}")
    
    # Prepare headers
    headers = {
        'X-API-Timestamp': timestamp,
        'X-API-Signature': signature,
        'X-API-Key': api_key
    }
    
    # Get filename from path
    filename = file_path.split('\\')[-1]
    
    # Prepare form data
    files = {
        'file': (filename, open(file_path, 'rb'), 'application/pdf')
    }
    
    data = {
        'model': 'gpt-4o-mini',
        'output_type': 'text',
        'instruction_id': instruction_id
    }
    
    try:
        # Send POST request
        response = requests.post(url, headers=headers, files=files, data=data)
        
        # Print request details for debugging
        print("\nRequest Details:")
        print(f"URL: {url}")
        print(f"Headers: {headers}")
        print(f"Data: {data}")
        print(f"Files: {filename}")
        
        # Check for specific error status codes
        if response.status_code == 401:
            print(f"\nResponse Headers: {response.headers}")
            print(f"Response Content: {response.text}")
            raise Exception("Authentication failed. Please check your API key and signature generation.")
        elif response.status_code == 403:
            raise Exception("Access forbidden. Please check your API permissions.")
        elif response.status_code == 404:
            raise Exception("API endpoint not found.")
        elif response.status_code >= 500:
            raise Exception("Server error occurred. Please try again later.")
        
        response.raise_for_status()  # Raise an exception for other bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response content: {e.response.text}")
        return None
    finally:
        # Close the file
        files['file'][1].close()
