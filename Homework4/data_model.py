import sqlite3


class DataModel:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def retrieve_data_single(self, sql_command):
        self.cursor.execute(sql_command)
        results = self.cursor.fetchone()
        return results[0]

    def retrieve_data_multiple(self, sql_command):
        self.cursor.execute(sql_command)
        results = self.cursor.fetchall()
        return results

    def insert_data(self, sql_command):
        self.cursor.execute(sql_command)
        self.commit()

    # def commit(self):
    #     self.connection.commit()

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

    def get_user(self, email):
        query = '''
            SELECT * FROM Users
            WHERE Email = '{}';
        '''.format(email)
        result = self.retrieve_data_single(query)
        return result

    def get_all_users(self):
        query = '''
            SELECT * FROM Users;
        '''
        results = self.retrieve_data_multiple(query)
        return results

    #####################################################
    ###        CRUD operations for Lists table        ###
    #####################################################

    def create_new_list(self, user_id, list_name):
        query = '''
            INSERT INTO Lists (UserID, ListName)
            VALUES ('{}', '{}');
        '''.format(user_id, list_name)
        self.insert_data(query)

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
            WHERE UserID = '{}' AND ListName = '{list_name}';
        '''.format(user_id, list_name)
        result = self.retrieve_data_single(query)
        return result

    def delete_list(self, user_id, list_name):
        # TODO: Here, we should first delete all tasks in the Tasks table pertaining
        #   to this ListID
        query = '''
            DELETE FROM Lists
            WHERE UserID = '{}' AND ListName = '{}';
        '''.format(user_id, list_name)
        self.insert_data(query)
        
    #####################################################
    ###        CRUD operations for Tasks table        ###
    #####################################################

    def create_new_task(self, list_id, task_name, status):
        query = '''
            INSERT INTO Tasks (ListID, TaskName, Status)
            VALUES ('{}', '{}', '{}');
        '''.format(list_id, task_name, status)
        self.insert_data(query)

    def update_task_name(self, list_id, task_id, updated_task_name):
        # NOTE: ListID might not be required here
        query = '''
            UPDATE Tasks
            SET TaskName = '{}'
            WHERE list_id = '{}' and task_id = '{}';
        '''.format(updated_task_name, list_id, task_id)
        self.insert_data(query)

    def update_task_status(self, list_id, task_id, updated_task_status):
        # NOTE: ListID might not be required here
        query = '''
            UPDATE Tasks
            SET Status = '{}'
            WHERE list_id = '{}' and task_id = '{}';
        '''.format(updated_task_status, list_id, task_id)
        self.insert_data(query)

    def delete_all_tasks(self, list_id):
        query = '''
            DELETE FROM Tasks
            WHERE ListID = '{}';
        '''.format(list_id)
        self.insert_data(query)

    def delete_task(self, task_id):
        query = '''
            DELETE FROM Tasks
            WHERE TaskID = '{}';
        '''.format(task_id)
        self.insert_data(query)

    def get_all_tasks(self, list_id):
        query = '''
            SELECT TaskID, TaskName, Status FROM Tasks
            WHERE ListID = '{}';
        '''.format(list_id)
        results = self.retrieve_data_multiple(query)
        return results