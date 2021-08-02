from datetime import datetime

def filter_users(all_users):
    '''
        This function filters users by selecting only those that were
        added in the last 24 hours
    '''
    filtered_users = []
    current_time = datetime.now()
    for user in all_users:
        insertion_time = user[-1]
        insertion_time = datetime.strptime(insertion_time, "%Y-%m-%d %H:%M:%S")
        time_diff = current_time - insertion_time
        time_diff_total_seconds = time_diff.total_seconds()
        # Here, 3600 is the total number of seconds in an hour
        diff_in_hours = divmod(time_diff_total_seconds, 3600)
        if diff_in_hours <= 24:
            filtered_users.append(user)
    return filtered_users