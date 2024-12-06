import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Utility to check file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/", methods=["GET", "POST"])
def upload_folder():
    if request.method == "POST":
        if 'folder' not in request.files:
            return render_template("upload.html", error="No folder selected.")
        
        files = request.files.getlist('folder')
        if not files:
            return render_template("upload.html", error="No files in the folder.")
        
        saved_files = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(save_path)
                saved_files.append(filename)
        
        if saved_files:
            return redirect(url_for("display_images"))
        else:
            return render_template("upload.html", error="No valid images found.")
    
    return render_template("upload.html")

@app.route("/display")
def display_images():
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template("display.html", images=images)

if __name__ == "__main__":
    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
