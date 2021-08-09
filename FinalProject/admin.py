from flask import Blueprint, request, session, flash, g
from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import redirect

import utils
import config
from data_model import DataModel

admin_page = Blueprint('admin_page', __name__, template_folder='templates')
model = DataModel(db_name=config.PATH_TO_DB)

@admin_page.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'admin' in session:
        return redirect(url_for('.admin_dashboard'))
    else:
        return render_template('admin_login.html')

@admin_page.route('/admin_login', methods=['POST'])
def admin_login():
    session.pop('admin', None)
    username = request.form['username']
    password = request.form['password']
    admin_verification_status = model.verify_admin(username, password)
    if admin_verification_status:
        session['admin'] = True
        return render_template('admin_dashboard.html')
    else:
        flash("Incorrect username or password!", category='login-error')
        return render_template('admin_login.html')

@admin_page.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if request.method == 'POST':
        action = request.form['action']
        if action == 'all_users':
            return redirect(url_for('.admin_all_users_view', page_num=1))
        elif action == 'all_lists':
            return redirect(url_for('.admin_all_lists_view', page_num=1))
        elif action == 'logout':
            return redirect(url_for('.admin_logout'))
    return render_template('admin_dashboard.html')

@admin_page.route('/admin/admin_options', methods=['POST'])
def admin_dashboard_option_selection():
    try:
        selected_option = request.form['option']
        if selected_option == 'user_signup':
            session['limit_users'] = False
            return redirect(url_for('.admin_all_users_view', page_num=1))
        elif selected_option == 'user_signup_24':
            session['limit_users'] = True
            return redirect(url_for('.admin_all_users_view', page_num=1))
        elif selected_option == 'lists_created':
            session['limit_lists'] = False
            return redirect(url_for('.admin_all_lists_view', page_num=1))
        elif selected_option == 'lists_created_24':
            session['limit_lists'] = True
            return redirect(url_for('.admin_all_lists_view', page_num=1))
    except KeyError:
        return redirect(url_for('.admin_dashboard'))

@admin_page.route('/admin/users/<int:page_num>')
def admin_all_users_view(page_num):
    users = model.get_all_users(order='DESC')
    if session['limit_users'] is True:
        users = utils.filter_items(users, date_index=-1)

    lower_limit = 0
    upper_limit = config.ROWS_TO_DISPLAY_PER_PAGE
    if len(users) > config.ROWS_TO_DISPLAY_PER_PAGE:
        # this is so that later when displaying a page of results less than 50 rows,
        #   we know that previously, we have displayed a page full of 50 rows
        g.next_page_accessed = True
        if page_num > 1:
            for _ in range(1, page_num):
                lower_limit += config.ROWS_TO_DISPLAY_PER_PAGE
                upper_limit += config.ROWS_TO_DISPLAY_PER_PAGE
        # this is stop the page_num going below 1
        elif page_num <= 1:
            page_num = 1

        users = users[lower_limit: upper_limit]
        if len(users) > 0:
            data = {
                'page_num': page_num,
                'users': users
            }
            return render_template('admin_all_users_view.html', data=data)
        else:
            return redirect(url_for('.admin_all_users_view', page_num=page_num-1 if page_num > 1 else page_num))
    else:
        # this try-catch block is to try to limit the next button increasing the page numbers
        #   endlessly in the case when users are less than 50 altogether
        # TODO: In the case of users being less than 50 altogether, clicking on Next does 
        #   increase the page_num to 2, can't figure out how to fix...
        try:
            g.next_page_accessed
            data = {
                'page_num': page_num,
                'users': users
            }
        except AttributeError:
            page_num = 1
            data = {
                'page_num': page_num,
                'users': users
            }
        return render_template('admin_all_users_view.html', data=data)

@admin_page.route('/admin/users/next_page', methods=['POST'])
def users_view_next_page():
    next_prev_page_num = request.form['page_num']
    return redirect(url_for('.admin_all_users_view', page_num=next_prev_page_num))

@admin_page.route('/admin/users/<int:user_id>', methods=['POST'])
def admin_user_view(user_id):
    user_info = model.get_user(user_id)
    user_lists_names = model.get_all_list_names(user_id)
    return render_template('admin_user_view.html', data={
        'user_info': user_info,
        'list_names': user_lists_names
    })

@admin_page.route('/admin/users/delete_user', methods=['POST'])
def admin_delete_user():
    user_id = request.form['user_id']
    model.delete_user(user_id)
    return redirect(url_for('.admin_all_users_view', page_num=1))

@admin_page.route('/admin/lists/<int:page_num>')
def admin_all_lists_view(page_num):
    lists = model.get_all_lists()
    # lists = utils.replace_user_ids_with_usernames(lists, model)
    if session['limit_lists']:
        lists = utils.filter_items(lists, date_index=-1)

    lower_limit = 0
    upper_limit = config.ROWS_TO_DISPLAY_PER_PAGE
    if len(lists) > config.ROWS_TO_DISPLAY_PER_PAGE:
        # this is so that later when displaying a page of results less than 50 rows,
        #   we know that previously, we have displayed a page full of 50 rows
        g.next_page_accessed = True
        if page_num > 1:
            for _ in range(1, page_num):
                lower_limit += config.ROWS_TO_DISPLAY_PER_PAGE
                upper_limit += config.ROWS_TO_DISPLAY_PER_PAGE
        # this is stop the page_num going below 1
        elif page_num <= 1:
            page_num = 1

        lists = lists[lower_limit: upper_limit]
        if len(lists) > 0:
            data = {
                'page_num': page_num,
                'lists': lists
            }
            return render_template('admin_all_lists_view.html', data=data)
        else:
            return redirect(url_for('.admin_all_lists_view', page_num=page_num-1 if page_num > 1 else page_num))
    else:
        # this try-catch block is to try to limit the next button increasing the page numbers
        #   endlessly in the case when lists are less than 50 altogether
        # TODO: In the case of lists being less than 50 altogether, clicking on Next does 
        #   increase the page_num to 2, can't figure out how to fix...
        try:
            g.next_page_accessed
            data = {
                'page_num': page_num,
                'lists': lists
            }
        except AttributeError:
            page_num = 1
            data = {
                'page_num': page_num,
                'lists': lists
            }
        return render_template('admin_all_lists_view.html', data=data)
    
@admin_page.route('/admin/lists/next_page', methods=['POST'])
def lists_view_next_page():
    next_prev_page_num = request.form['page_num']
    return redirect(url_for('.admin_all_lists_view', page_num=next_prev_page_num))

@admin_page.route('/admin/lists/<int:list_id>', methods=['POST'])
def admin_list_view(list_id):
    list_info = model.get_list(list_id)
    list_info = utils.replace_user_id_with_username_in_list(list_info, model)
    list_tasks_incomplete = model.get_all_task_names(list_id, task_status=0)
    print("Incomplete tasks: ", list_tasks_incomplete)
    list_tasks_complete = model.get_all_task_names(list_id, task_status=1)
    print("Complete tasks: ", list_tasks_complete)
    return render_template('admin_list_view.html', data={
        'list_info': list_info,
        'task_names_complete': list_tasks_complete,
        'task_names_incomplete': list_tasks_incomplete
    })

@admin_page.route('/admin/lists/delete_list', methods=['POST'])
def admin_delete_list():
    list_id = request.form['list_id']
    model.delete_list(list_id)
    return redirect(url_for('.admin_all_lists_view', page_num=1))

@admin_page.route('/admin/logout', methods=['GET'])
def admin_logout():
    session.pop('admin', None)
    session.pop('limit_users', None)
    session.pop('limit_lists', None)
    return redirect(url_for('.admin'))