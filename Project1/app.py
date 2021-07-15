from flask import Flask, render_template, send_file


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template('main_structure.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about_us.html')

@app.route('/terms_of_use', methods=['GET'])
def terms_of_use():
    return render_template('terms_of_use.html')

@app.route('/download_terms_of_use')#, methods=['GET'])
def download_terms_of_use():
    return send_file(
        'static/docs/Terms-and-Conditions.docx',
        attachment_filename="Terms-and-Conditions.docx"
    )

@app.route('/privacy', methods=['GET'])
def privacy():
    return render_template('privacy.html')

@app.route('/download_privacy_policy')#, methods=['GET'])
def download_privacy_policy():
    return send_file(
        'static/docs/Privacy_Policy.docx',
        attachment_filename="Privacy-Policy.docx"
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('dashboard.html')

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    return render_template('sign_up.html')

# This might not be needed
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/create_new_list', methods=['GET'])
def create_new_list():
    return render_template('create_new_list.html')

@app.route('/view_list', methods=['GET'])
def view_list():
    return render_template('view_list.html')

@app.route('/logout', methods=['POST'])
def logout():
    return render_template('main_structure.html')


if __name__ == '__main__':
    app.run(port=7000, debug=True)