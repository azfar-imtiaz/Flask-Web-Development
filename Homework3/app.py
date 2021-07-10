from flask import Flask, render_template


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

@app.route('/privacy', methods=['GET'])
def privacy():
    return render_template('privacy.html')

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    return render_template('sign_up.html')

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