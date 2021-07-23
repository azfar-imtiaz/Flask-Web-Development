from flask import Flask, request, render_template, send_file
from flask.helpers import url_for
from flask.templating import render_template_string
from werkzeug.utils import redirect
from data_model import DataModel


app = Flask(__name__)
model = DataModel(db_name='../ToDoList.db')


@app.route('/', methods=['GET'])
def home():
    # TODO: Some session verification stuff will happen here
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
    if request.method == 'POST':
        user_email = request.form['user_email']
        password = request.form['password']
        db_password = model.check_password(user_email)
        if db_password is not None:
            db_password = db_password[0]
            if db_password == password:
                # return redirect(url_for('home'))
                user_id = model.get_user_id(user_email)
                list_names = model.get_all_list_names(user_id)
                list_names = [a[0] for a in list_names]
                return render_template('dashboard.html', data=list_names)
            else:
                return render_template('main_structure.html', message='Wrong username or password')    
        else:
            return render_template('main_structure.html', message='Wrong username or password')
    return render_template('main_structure.html')

@app.route('/display_list', methods=['POST'])
def display_list():
    list_name = request.form['list_name']
    list_id = model.get_list_id(list_name)
    if list_id is not None:
        list_id = list_id[0]
        return redirect(url_for('display_list_with_id', list_id=list_id))
        

@app.route('/display_list/<list_id>')
def display_list_with_id(list_id):
    list_tasks = model.get_all_tasks(list_id)
    list_tasks_dict = {
        'list_id': list_id,
        'list_tasks': list_tasks
    }
    return render_template('view_list.html', list_tasks_dict=list_tasks_dict)

@app.route('/check_off_items/<int:list_id>', methods=['POST'])
def check_off_items(list_id):
    marked_tasks_ids = request.form['task_name']
    marked_tasks_ids = list(marked_tasks_ids)
    print(marked_tasks_ids)
    model.update_task_status(marked_tasks_ids, updated_task_status=1)
    return redirect(url_for('display_list_with_id', list_id=list_id))

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

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return render_template('main_structure.html')


if __name__ == '__main__':
    app.run(port=7000, debug=True)