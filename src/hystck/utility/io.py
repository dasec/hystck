import os


def file_exists(path):
    return os.path.isfile(path)


def is_valid_attached_path_string(attached_path):
    # Gänsefüßchen handlen
    file_path_list = attached_path.split(',')

    if len(file_path_list) == 0:
        return False

    for file_path in file_path_list:
        if file_exists(file_path) is False:
            return False

    return True


def copy_file_to_shared_file_system(path):
    pass
