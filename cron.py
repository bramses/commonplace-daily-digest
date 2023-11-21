import os
import datetime

# create a new folder for the day and put it in /daily
def create_folder():
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    path = os.path.join(os.getcwd() + '/daily/' + today)
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print("Folder already exists. Exiting...")
        exit(1)
    return path