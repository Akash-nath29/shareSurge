from io import BytesIO
from flask import Flask, render_template, request, send_file, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class File(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(100), nullable = False)
    data = db.Column(db.LargeBinary)
    
    def __init__(self, filename, data):
        self.filename = filename
        self.data = data

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        file = request.files['fileUpload']
        upload = File(filename=file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()
    files_available = File.query.all()
    return render_template('index.html', files = files_available)

@app.route('/download/<int:file_id>')
def download(file_id):
    download = File.query.get_or_404(file_id)
    return send_file(BytesIO(download.data), download_name=download.filename, as_attachment=True)

@app.route('/delete/<int:file_id>')
def delete(file_id):
    deleted_file = File.query.get_or_404(file_id)
    db.session.delete(deleted_file)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="80")