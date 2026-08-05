import os
import zipfile
import webbrowser

project_dir = os.path.dirname(os.path.abspath(__file__))
zip_path = os.path.join(project_dir, "bca_face_attendance_render_package.zip")

print("====================================================")
print("Creating Render.com Deployment Zip Package...")
print("====================================================")

exclude_dirs = {'.git', '__pycache__', 'staticfiles', '.idea', '.vscode'}
exclude_files = {'db.sqlite3-journal', 'bca_face_attendance_render_package.zip'}

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file in exclude_files or file.endswith('.pyc'):
                continue
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, project_dir)
            zipf.write(full_path, arcname)

print(f"SUCCESS: Package created at: {zip_path}")
print("\nOpening GitHub in your browser...")
webbrowser.open("https://github.com/new")
