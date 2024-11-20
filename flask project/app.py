from flask import Flask, render_template, request, redirect, url_for, flash
import os
import random  # For simulating results

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['TEMPLATES_AUTO_RELOAD'] = True  # Auto-reload templates when changed

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'nii', 'nii.gz'}

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Mock function to simulate tumor detection and survival prediction
def mock_diagnosis():
    # Simulating detection of brain tumor (Yes/No)
    tumor_detected = random.choice([True, False])

    # Simulating survival prediction in months if a tumor is detected
    survival_prediction = random.randint(6, 36) if tumor_detected else None

    return tumor_detected, survival_prediction


@app.route('/')
def home():
    # Initially, there are no results to display, so we pass None for both
    return render_template('home.html', tumor_detected=None, survival_prediction=None)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        # Simulating the tumor diagnosis and survival prediction
        tumor_detected, survival_prediction = mock_diagnosis()

        # Pass the results back to the home page to be displayed in the table
        return render_template('home.html', tumor_detected=tumor_detected, survival_prediction=survival_prediction)

    else:
        flash('Invalid file type. Only NIfTI files are allowed.')
        return redirect(request.url)


if __name__ == '__main__':
    app.run(debug=True)
