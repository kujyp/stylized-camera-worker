import os


def convert_path_sep(local_path):
    return local_path.replace("/", os.sep)


def mkdir_unless_exist(local_path):
    dirs = local_path.split(os.sep)
    path = ''
    for dir in dirs:
        if dir == '':
            # it means ABSOLUTE PATH
            path = '/'
            continue

        next_path = path + dir + os.sep
        try:
            os.stat(next_path)
        except:
            print('Make dir : \t\t\t\t\t' + next_path)
            os.mkdir(next_path)
        path = next_path