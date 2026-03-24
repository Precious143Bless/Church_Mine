import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def check_files():
    """Check if all required files exist"""
    
    print("=" * 50)
    print("Church Registry System - File Check")
    print("=" * 50)
    
    # Check root directory
    root_files = ['index.html']
    print("\nChecking root directory:")
    for file in root_files:
        if os.path.exists(file):
            print(f"  ✓ {file} - OK")
        else:
            print(f"  ✗ {file} - MISSING")
    
    # Check frontend folder
    frontend_path = 'frontend'
    if os.path.exists(frontend_path):
        print(f"\nChecking {frontend_path}/ folder:")
        frontend_files = [
            'login.html', 'dashboard.html', 'members.html', 
            'member_detail.html', 'member_form.html', 'sacraments.html',
            'sacrament_form.html', 'pledges.html', 'pledge_form.html',
            'payments.html', 'reports.html'
        ]
        
        for file in frontend_files:
            full_path = os.path.join(frontend_path, file)
            if os.path.exists(full_path):
                print(f"  ✓ {file} - OK")
            else:
                print(f"  ✗ {file} - MISSING")
        
        # Check CSS
        css_path = os.path.join(frontend_path, 'assets', 'style', 'style.css')
        if os.path.exists(css_path):
            print(f"  ✓ css/style.css - OK")
        else:
            print(f"  ✗ css/style.css - MISSING")
        
        # Check JS
        js_path = os.path.join(frontend_path, 'assets','script', 'app.js')
        if os.path.exists(js_path):
            print(f"  ✓ js/app.js - OK")
        else:
            print(f"  ✗ js/app.js - MISSING")
    else:
        print(f"\n✗ {frontend_path}/ folder does not exist!")
    
    # Check backend
    backend_path = 'backend'
    if os.path.exists(backend_path):
        print(f"\nChecking backend/ folder:")
        backend_files = ['manage.py', 'requirements.txt']
        for file in backend_files:
            full_path = os.path.join(backend_path, file)
            if os.path.exists(full_path):
                print(f"  ✓ {file} - OK")
            else:
                print(f"  ✗ {file} - MISSING")
    else:
        print(f"\n✗ backend/ folder does not exist!")
    
    print("\n" + "=" * 50)
    print("To fix missing files, ensure all HTML files are in the frontend/ folder")
    print("Then run: cd backend && python manage.py runserver")
    print("=" * 50)

if __name__ == "__main__":
    check_files()