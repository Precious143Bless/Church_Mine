from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os

def serve_index(request):
    """Serve the main index.html from root directory"""
    return render(request, 'index.html')

def test_frontend(request):
    """Test if frontend files are accessible"""
    frontend_path = os.path.join(os.path.dirname(__file__), '../../frontend')
    files = os.listdir(frontend_path) if os.path.exists(frontend_path) else []
    
    return HttpResponse(f"""
    <h1>Frontend Files Check</h1>
    <p>Frontend folder path: {frontend_path}</p>
    <p>Files found: {len(files)}</p>
    <ul>
        {''.join([f'<li>{file}</li>' for file in files])}
    </ul>
    <h2>Debug Info:</h2>
    <ul>
        <li>BASE_DIR: {os.path.dirname(os.path.dirname(__file__))}</li>
        <li>Static files dirs configured</li>
    </ul>
    <a href="/">Go back</a>
    """)