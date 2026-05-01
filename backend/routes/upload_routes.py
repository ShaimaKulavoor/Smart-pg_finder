"""
Upload routes for image files
"""

from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename

# Create blueprint
bp = Blueprint('upload', __name__, url_prefix='/api')

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload-image', methods=['POST'])
def upload_image():
    """
    Upload an image file
    
    Request:
        file (multipart/form-data): Image file
        
    Response:
        {
            'status': 'success',
            'image_url': '/uploads/filename.jpg'
        }
    """
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'No file selected'
            }), 400
        
        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({
                'status': 'error',
                'message': f'File type not allowed. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({
                'status': 'error',
                'message': f'File too large. Maximum size: {MAX_FILE_SIZE / (1024 * 1024)}MB'
            }), 400
        
        # Save file with secure name
        filename = secure_filename(file.filename)
        # Add timestamp to avoid filename conflicts
        import time
        filename = f"{int(time.time())}_{filename}"
        
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Return image URL (relative path accessible from frontend)
        image_url = f'/uploads/{filename}'
        
        return jsonify({
            'status': 'success',
            'image_url': image_url,
            'filename': filename
        }), 201
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Upload failed: {str(e)}'
        }), 500


@bp.route('/delete-image/<filename>', methods=['DELETE'])
def delete_image(filename):
    """
    Delete an uploaded image
    
    Args:
        filename: Name of file to delete
        
    Response:
        {
            'status': 'success',
            'message': 'Image deleted'
        }
    """
    try:
        # Security: prevent directory traversal
        filename = secure_filename(filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Ensure file is in upload folder
        if not os.path.abspath(filepath).startswith(os.path.abspath(UPLOAD_FOLDER)):
            return jsonify({
                'status': 'error',
                'message': 'Invalid file path'
            }), 400
        
        # Check if file exists
        if not os.path.exists(filepath):
            return jsonify({
                'status': 'error',
                'message': 'File not found'
            }), 404
        
        # Delete file
        os.remove(filepath)
        
        return jsonify({
            'status': 'success',
            'message': 'Image deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Delete failed: {str(e)}'
        }), 500
