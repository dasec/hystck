import os


def file_exists(path):
    return os.path.isfile(path)


def parse_attachment_string(attachment_path_list):
    if attachment_path_list is None:
        return None

    if len(attachment_path_list) > 1:
        return create_comma_separated_string_for_multiple_paths(attachment_path_list)

    elif len(attachment_path_list) == 1:
        return attachment_path_list[0]

    return None


def create_comma_separated_string_for_multiple_paths(attachment_path_list):
    attachment_string = ""
    for path in attachment_path_list[:-1]:
        attachment_string += path + ','
    return attachment_string + attachment_path_list[-1]


def copy_file_to_shared_file_system(path):
    pass
