from datetime import datetime
import os

# def FileExists(filepath):
#     if os.path.isfile(filepath):
#         return True
#     else:
#         return False

def WriteToFile():
    dir_path = '/home/karan/Airflow/'
    file_name = 't3.log'
    full_path = dir_path + file_name
    f = open(full_path, "a+")
    f.write("T3 Time start: {}\n".format(str(datetime.now())))
    f.close()
