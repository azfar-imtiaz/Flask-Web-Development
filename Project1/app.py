from flask import Flask, request, render_template, send_file, session, g, flash
from flask.helpers import url_for
from flask.templating import render_template_string
from werkzeug.utils import redirect
from data_model import DataModel


app = Flask(__name__, static_url_path='/static')
app.secret_key = '2d1ea9a2a8734ab4885d5ab442e3e0c1'
model = DataModel(db_name='../ToDoList.db')


@app.before_request
def before_request():
    # NOTE: From my understanding, the session object maintains information throughout a whole session
    # This can be used to store a user object, such as a class object
    # The g object only stores information till a single, and is typically used to store basic information
    #   like username, or user ID
    g.user_id = None
    if 'user_id' in session:
        g.user_id = session['user_id']

@app.route('/', methods=['GET'])
def home():
    if 'user_id' in session:
        # g.user_id = session['user_id']
        # list_names = model.get_all_list_names(session['user_id'])
        session['current_list_id'] = None
        session['current_list_name'] = None
        list_names = model.get_all_list_names(g.user_id)
        list_names = [a[0] for a in list_names]        
        return render_template('dashboard.html', data=list_names)
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
        # session.pop('user_email', None)
        session.pop('user_id', None)
        user_email = request.form['user_email']
        password = request.form['password']
        db_password = model.check_password(user_email)
        if db_password is not None:
            db_password = db_password[0]
            if db_password == password:
                # session['user_email'] = user_email
                session['user_id'] = model.get_user_id(user_email)
                return redirect(url_for('home'))
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
        if request.form['action'] == 'View':
            list_id = list_id[0]
            return redirect(url_for('display_list_with_id', list_id=list_id, list_name=list_name))        
        elif request.form['action'] == 'Delete':
            return redirect(url_for('delete_list', list_name=list_name))

@app.route('/display_list/<int:list_id>/<string:list_name>')
def display_list_with_id(list_id, list_name):
    session['current_list_id'] = list_id
    session['current_list_name'] = list_name
    list_tasks = model.get_all_tasks(list_id)
    list_tasks_dict = {
        'list_id': list_id,
        'list_name': list_name,
        'list_tasks': list_tasks
    }
    return render_template('view_list.html', list_tasks_dict=list_tasks_dict)

@app.route('/check_off_items', methods=['POST'])
def check_off_items():
    marked_tasks_ids = request.form.getlist('task_id')
    if request.form['action'] == 'Complete':
        model.update_task_status(marked_tasks_ids, updated_task_status=1)
    elif request.form['action'] == 'Delete':
        model.delete_tasks(marked_tasks_ids)
    return redirect(url_for('display_list_with_id', list_id=session['current_list_id'], list_name=session['current_list_name']))

@app.route('/add_new_task', methods=['POST'])
def add_new_task():
    task_name = request.form['task_name']
    model.create_new_task(session['current_list_id'], task_name, status=0)
    return redirect(url_for('display_list_with_id', list_id=session['current_list_id'], list_name = session['current_list_name']))

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    return render_template('sign_up.html')

# This might not be needed
# @app.route('/dashboard', methods=['GET', 'POST'])
# def dashboard():
#     return render_template('dashboard.html')

@app.route('/create_new_list', methods=['POST'])
def create_new_list():
    list_name = request.form['list_name']
    model.create_new_list(g.user_id, list_name)
    return redirect(url_for('home'))

@app.route('/delete_list/<string:list_name>')
def delete_list(list_name):
    model.delete_list(g.user_id, list_name)
    return redirect(url_for('home'))

@app.route('/edit_list', methods=['POST'])
def edit_list():
    updated_list_name = request.form['updated_list_name']
    session['current_list_name'] = updated_list_name
    model.edit_list_name(
        session['current_list_id'], updated_list_name
    )
    return redirect(url_for('display_list_with_id', list_id=session['current_list_id'], list_name=session['current_list_name']))

# @app.route('/view_list', methods=['GET'])
# def view_list():
#     return render_template('view_list.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(port=7000, debug=True)