from flask import Flask, render_template, send_from_directory, abort
from werkzeug.utils import safe_join
import os

app = Flask(__name__)

# Directory where the files are stored
FILES_DIR = "files"

@app.route("/")
@app.route("/<path:subpath>")
def index(subpath=""):
    try:
        # Calculate full path within the files directory
        full_path = os.path.join(FILES_DIR, subpath)
        
        if not os.path.exists(full_path):
            abort(404)
        
        # Check if the path is a directory or a file
        if os.path.isdir(full_path):
            # List contents of the directory
            contents = os.listdir(full_path)
            files = [f for f in contents if os.path.isfile(os.path.join(full_path, f))]
            directories = [d for d in contents if os.path.isdir(os.path.join(full_path, d))]
            return render_template("index.html", files=files, directories=directories, current_path=subpath)
        else:
            # If it's a file, download it
            return send_from_directory(os.path.dirname(full_path), os.path.basename(full_path), as_attachment=True)
    except Exception as e:
        return str(e)

@app.route("/download/<filename>")
def download_file(filename):
    try:
        # Securely join the filename to the files directory
        filepath = safe_join(FILES_DIR, filename)
        # Send the file for downloading
        return send_from_directory(FILES_DIR, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
