from re import DEBUG
import sqlite3


class DataModel:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def retrieve_data_single(self, sql_command):
        self.cursor.execute(sql_command)
        results = self.cursor.fetchone()
        return results

    def retrieve_data_multiple(self, sql_command):
        self.cursor.execute(sql_command)
        results = self.cursor.fetchall()
        return results

    def insert_data(self, sql_command):
        self.cursor.execute(sql_command)
        self.commit()

    def commit(self):
        self.connection.commit()

    def close_connection(self):
        self.connection.close()
        self.cursor.close()

    #####################################################
    ###        CRUD operations for Users table        ###
    #####################################################

    def add_user(self, email, password, username):
        query = '''
            INSERT INTO Users (Email, Password, Username)
            VALUES ('{}', '{}', '{}');
        '''.format(email, password, username)
        self.insert_data(query)

    # this function selects the user by email
    def get_user(self, email):
        query = '''
            SELECT * FROM Users
            WHERE Email = '{}';
        '''.format(email)
        result = self.retrieve_data_single(query)
        return result

    # this function selects the user by user_id
    def get_user(self, user_id):
        query = '''
            SELECT * FROM Users
            WHERE UserID = '{}';
        '''.format(user_id)
        result = self.retrieve_data_single(query)
        return result

    def get_all_users(self, order='ASC'):
        query = '''
            SELECT * FROM Users
            ORDER BY UserID {};
        '''.format(order)
        results = self.retrieve_data_multiple(query)
        return results

    def check_password(self, user_email):
        query = '''
            SELECT Password FROM Users WHERE Email = '{}';
        '''.format(user_email)
        result = self.retrieve_data_single(query)
        return result

    def get_user_id(self, user_email):
        query = '''
            SELECT UserID FROM Users WHERE Email = '{}';
        '''.format(user_email)
        result = self.retrieve_data_single(query)
        return result[0]

    def get_user_name(self, user_email):
        query = '''
            SELECT Username FROM Users WHERE Email = '{}';
        '''.format(user_email)
        result = self.retrieve_data_single(query)
        return result[0]

    def get_user_name_from_id(self, user_id):
        query = '''
            SELECT Username FROM Users WHERE UserID = '{}';
        '''.format(user_id)
        result = self.retrieve_data_single(query)
        return result[0]

    def delete_user(self, user_id):
        # First, we select and delete all lists created by this user
        query = '''
            SELECT ListID, ListName FROM Lists
            WHERE UserID = '{}';
        '''.format(user_id)
        result = self.retrieve_data_multiple(query)
        for row in result:
            list_id = row[0]
            list_name = row[1]
            self.delete_list(user_id, list_id, list_name)
        
        # Now, we delete the user itself
        query = '''
            DELETE FROM Users
            WHERE UserID = '{}';
        '''.format(user_id)
        self.insert_data(query)

    #####################################################
    ###        CRUD operations for Lists table        ###
    #####################################################

    def create_new_list(self, user_id, list_name):
        existing_lists_for_user = self.get_all_list_names(user_id)
        existing_lists_for_user = [a[0].lower() for a in existing_lists_for_user]
        if list_name.lower() not in existing_lists_for_user:
            query = '''
                INSERT INTO Lists (UserID, ListName)
                VALUES ('{}', '{}');
            '''.format(user_id, list_name)
            self.insert_data(query)
            return True
        return False

    def edit_list_name(self, list_id, updated_list_name):
        query = '''
            UPDATE Lists
            SET ListName = '{}'
            WHERE ListID = '{}';
        '''.format(updated_list_name, list_id)
        self.insert_data(query)

    def get_all_lists(self):
        query = '''
            SELECT * FROM Lists;
        '''
        result = self.retrieve_data_multiple(query)
        return result

    def get_all_list_names(self, user_id):
        query = '''
            SELECT ListName from Lists
            WHERE UserID = '{}';
        '''.format(user_id)
        results = self.retrieve_data_multiple(query)
        return results

    def get_list(self, user_id, list_name):
        query = '''
            SELECT * FROM Lists
            WHERE UserID = '{}' AND ListName = '{}';
        '''.format(user_id, list_name)
        result = self.retrieve_data_single(query)
        return result

    def get_list(self, list_id):
        query = '''
            SELECT * FROM Lists
            WHERE ListID = '{}';
        '''.format(list_id)
        result = self.retrieve_data_single(query)
        return result

    def get_list_id(self, user_id, list_name):
        query = '''
            SELECT ListID FROM Lists
            WHERE UserID = '{}' AND ListName = '{}'
        '''.format(user_id, list_name)
        result = self.retrieve_data_single(query)
        return result

    def delete_list(self, list_id, user_id=None, list_name=None):
        # We first delete all tasks in the Tasks table pertaining to this ListID
        query = '''
            DELETE FROM Tasks
            WHERE ListID = '{}';
        '''.format(list_id)
        self.insert_data(query)

        # Then we delete the list itself
        if user_id is not None and list_name is not None:
            query = '''
                DELETE FROM Lists
                WHERE UserID = '{}' AND ListName = '{}';
            '''.format(user_id, list_name)            
        else:
            query = '''
                DELETE FROM Lists
                WHERE ListID = '{}';
            '''.format(list_id)
        self.insert_data(query)
        
    #####################################################
    ###        CRUD operations for Tasks table        ###
    #####################################################

    def create_new_task(self, list_id, task_name, status):
        tasks_in_list = self.get_all_tasks(list_id)
        task_names_in_list = [a[1].lower() for a in tasks_in_list]
        # if task doesn't exist in this list, add it
        if task_name.lower() not in task_names_in_list:
            query = '''
                INSERT INTO Tasks (ListID, TaskName, Status)
                VALUES ('{}', '{}', '{}');
            '''.format(list_id, task_name, status)
            self.insert_data(query)
            return True
        # if task already exists...
        else:
            existing_task = [a for a in tasks_in_list if task_name.lower() == a[1].lower()]
            existing_task_id = existing_task[0][0]
            existing_task_status = existing_task[0][2]
            # if task has been marked as complete, change its status to incomplete
            if existing_task_status == 1:
                existing_task_id = tuple([str(existing_task_id)])
                self.update_task_status(existing_task_id, updated_task_status=0)
                return True
            # if task is already incomplete, return False, which results in "Task already exists" message
            else:
                return False

    def update_task_name(self, list_id, task_id, updated_task_name):
        # NOTE: ListID might not be required here
        query = '''
            UPDATE Tasks
            SET TaskName = '{}'
            WHERE list_id = '{}' and task_id = '{}';
        '''.format(updated_task_name, list_id, task_id)
        print(query)
        self.insert_data(query)

    def update_task_status(self, task_ids, updated_task_status):
        # NOTE: Here, task_ids is a tuple
        query = '''
            UPDATE Tasks
            SET Status = {}
            WHERE TaskID IN ({});
        '''.format(updated_task_status, ','.join(task_ids))
        print(query)
        self.insert_data(query)

    def delete_all_tasks(self, list_id):
        query = '''
            DELETE FROM Tasks
            WHERE ListID = '{}';
        '''.format(list_id)
        self.insert_data(query)

    def delete_tasks(self, task_ids):
        query = '''
            DELETE FROM Tasks
            WHERE TaskID IN ({});
        '''.format(','.join(task_ids))
        self.insert_data(query)

    def get_all_tasks(self, list_id):
        query = '''
            SELECT TaskID, TaskName, Status FROM Tasks
            WHERE ListID = '{}';
        '''.format(list_id)
        results = self.retrieve_data_multiple(query)
        return results

    def get_all_task_names(self, list_id, task_status):
        query = '''
            SELECT TaskName FROM Tasks
            WHERE ListID = '{}' AND Status = '{}';
        '''.format(list_id, task_status)
        results = self.retrieve_data_multiple(query)
        return results

    #####################################################
    ###        CRUD operations for Admin table        ###
    #####################################################

    def verify_admin(self, username, password):
        query = '''
            SELECT AdminID FROM Administrator
            WHERE Username = '{}' AND Password = '{}'
            LIMIT 1;
        '''.format(username, password)
        results = self.retrieve_data_multiple(query)
        if len(results) == 1:
            return True
        return False