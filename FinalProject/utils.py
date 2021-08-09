from datetime import datetime

import config

def filter_items(all_items, date_index=-1):
    '''
        This function filters items (users or items) by selecting only 
        those that were added in the last 24 hours
    '''
    filtered_items = []
    current_time = datetime.now()
    for item in all_items:
        insertion_time = item[date_index]
        insertion_time = datetime.strptime(insertion_time, "%Y-%m-%d %H:%M:%S")
        time_diff = current_time - insertion_time
        time_diff_total_seconds = time_diff.total_seconds()
        # Here, 3600 is the total number of seconds in an hour
        diff_in_hours = divmod(time_diff_total_seconds, 3600)[0]
        if diff_in_hours <= config.TIME_LIMIT_SINCE_CREATION:
            filtered_items.append(item)
    return filtered_items

def replace_user_id_with_username_in_list(ls, model):
    '''
        This function replaces the user ID in the list with the 
        corresponding username
    '''
    user_id = ls[1]
    username = model.get_user_name_from_id(user_id)
    updated_list = [
        ls[0],
        username,
        ls[2],
        ls[3]
    ]
    return updated_list