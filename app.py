from flask import Flask, render_template, request, send_file, jsonify
import os
from datetime import datetime
from doc_pro_ai_service import send_document_to_ai_service
import json
import traceback
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Create downloads directory if it doesn't exist
DOWNLOADS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
DOCUMENTS_DIR = r"D:\ThoughtfocusRD\Peoples_group\documents"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

# Get API key from environment variable
API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY not found in environment variables")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/files', methods=['GET'])
def files_page():
    return render_template('files.html')

@app.route('/file-viewer', methods=['GET'])
def file_viewer():
    return render_template('file_viewer.html')

@app.route('/api/files', methods=['GET'])
def list_files():
    try:
        files = []
        for filename in os.listdir(DOWNLOADS_DIR):
            file_path = os.path.join(DOWNLOADS_DIR, filename)
            if os.path.isfile(file_path):
                files.append({
                    'name': filename,
                    'size': os.path.getsize(file_path),
                    'modified': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                })
        return jsonify({
            'status': 'success',
            'files': sorted(files, key=lambda x: x['modified'], reverse=True)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/view/<filename>')
def view_file(filename):
    try:
        file_path = os.path.join(DOWNLOADS_DIR, filename)
        if not os.path.exists(file_path):
            return jsonify({
                'status': 'error',
                'message': 'File not found'
            }), 404
            
        with open(file_path, 'r') as f:
            content = f.read()
            
        return jsonify({
            'status': 'success',
            'content': content,
            'filename': filename
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/process', methods=['POST'])
def process_document():
    if 'file' not in request.files:
        return jsonify({
            'status': 'error',
            'message': 'No file uploaded'
        }), 400
    
    file = request.files['file']
    instruction_id = request.form.get('instruction_id', '1')
    
    if file.filename == '':
        return jsonify({
            'status': 'error',
            'message': 'No file selected'
        }), 400
    
    # Save the uploaded file temporarily
    temp_file_path = os.path.join(DOWNLOADS_DIR, file.filename)
    file.save(temp_file_path)
    
    try:
        # Process the document using API_KEY from environment
        result = send_document_to_ai_service(temp_file_path, API_KEY, instruction_id)
        
        if result:
            # Generate timestamp for the response file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            # Get original filename without extension
            original_name = os.path.splitext(file.filename)[0]
            response_filename = f'{original_name}_response_{timestamp}.json'
            response_path = os.path.join(DOWNLOADS_DIR, response_filename)
            
            # Save the response to a file
            with open(response_path, 'w') as f:
                json.dump(result, f, indent=4)
            
            return jsonify({
                'status': 'success',
                'message': 'Document processed successfully',
                'response_file': response_filename
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to process document. Please check the API credentials and try again.'
            }), 500
            
    except Exception as e:
        error_message = str(e)
        print(f"Error processing document: {error_message}")
        print(traceback.format_exc())
        
        return jsonify({
            'status': 'error',
            'message': f'Error processing document: {error_message}'
        }), 500
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(
            os.path.join(DOWNLOADS_DIR, filename),
            as_attachment=True
        )
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error downloading file: {str(e)}'
        }), 404

@app.route('/api/folders', methods=['GET'])
def list_folders():
    try:
        folders = []
        for item in os.listdir(DOCUMENTS_DIR):
            item_path = os.path.join(DOCUMENTS_DIR, item)
            if os.path.isdir(item_path):
                folders.append(item)
        return jsonify({
            'status': 'success',
            'folders': sorted(folders)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/cyclical-run', methods=['POST'])
def cyclical_run():
    folder = request.form.get('folder')
    instruction_id = request.form.get('cyclical_instruction_id', '1')
    
    if not folder:
        return jsonify({
            'status': 'error',
            'message': 'No folder selected'
        }), 400
    
    folder_path = os.path.join(DOCUMENTS_DIR, folder)
    if not os.path.exists(folder_path):
        return jsonify({
            'status': 'error',
            'message': 'Selected folder does not exist'
        }), 400
    
    processed_files = 0
    
    try:
        # Get all PDF files in the folder
        pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
        
        for filename in pdf_files:
            file_path = os.path.join(folder_path, filename)
            
            # Process the document using API_KEY from environment
            result = send_document_to_ai_service(file_path, API_KEY, instruction_id)
            
            if result:
                # Generate timestamp for the response file
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                # Get original filename without extension
                original_name = os.path.splitext(filename)[0]
                response_filename = f'{original_name}_response_{timestamp}.json'
                response_path = os.path.join(DOWNLOADS_DIR, response_filename)
                
                # Save the response to a file
                with open(response_path, 'w') as f:
                    json.dump(result, f, indent=4)
                
                processed_files += 1
        
        return jsonify({
            'status': 'success',
            'message': f'Successfully processed {processed_files} files from {folder}',
            'processed_files': processed_files
        })
            
    except Exception as e:
        error_message = str(e)
        print(f"Error in cyclical run: {error_message}")
        print(traceback.format_exc())
        
        return jsonify({
            'status': 'error',
            'message': f'Error processing documents: {error_message}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 