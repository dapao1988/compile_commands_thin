import json
import argparse
import string


def filter(filter_list, json_array_list):
    """
    select compile_command.json json object according to your filter list

    :param filter_list: origin filter txt, about your source file path
    :param json_array_list: json list in compile_command.json
    :return: json object list
    """
    thinned_json_array = []

    for json_object in json_array_list:
        need_save = False
        for filter_path in filter_list:
            if filter_path.startswith('#'):
                continue
            file_path = json_object.get('file')
            file_in_filter = filter_path in file_path
            if file_in_filter:
                need_save = True
                break

        if need_save and json_object not in thinned_json_array:
            thinned_json_array.append(json_object)
    return thinned_json_array

def remove_redundance(filter_list):
    """
    remove space and wildcard symbol in source file path,
    e.x. 'frameworks/av/*' -> 'frameworks/av'

    :param filter_list: json array list
    :return: list
    """
    filter_thin = []

    for file_path in filter_list:
        path=file_path.replace('/*', '')
        path=path.strip()
        filter_thin.append(path)

    return filter_thin

def generate_file_path(json_array_list):
    """
    to remove the detailed filename in the end of line
    :param filter_list: lines of filter path
    :param json_array_list: list of jsonArray
    :return: list of jsonArray after removing lines not in filter
    """
    path_list = []

    for json_object in json_array_list:
        file_path = json_object.get('file')
        index=file_path.rfind('/')
        file_path = file_path[0:index]
        print(file_path)
        if file_path not in path_list:
            path_list.append(file_path)
    return path_list

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--filterlist", required=True, help="filter list file for included")
    ap.add_argument("-i", "--inputfile", required=True, help="filter list file for included")
    arg = vars(ap.parse_args())
    print(arg['filterlist'])
    print(arg['inputfile'])

    with open(arg['inputfile']) as f:
        data = json.load(f)

    with open(arg['filterlist']) as filter_file:
        filter_list = filter_file.readlines()

    print("original filter:",filter_list)

    filter_list=remove_redundance(filter_list)
    print("preprocess filter:",filter_list)
    path_list = generate_file_path(data)

    data = filter(filter_list, data)

#    for key in data:
#        # print(json.dumps(key, indent=4, sort_keys=True))
#        print(key['file'])

    output_file=arg['inputfile']+'.bk'
    with open(output_file, 'w') as o:
        json.dump(data, o, indent=4, sort_keys=True)

    output_path_file = arg['inputfile'] + '.path.txt'
    path_list.sort()
    with open(output_path_file, 'w') as op:
        for path in path_list:
            op.write(path+'\n')
