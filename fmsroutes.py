import re

pattern = re.compile('"(.*?)"')

post_list = []
get_list = []
put_list = []
delete_list = []


def analyse_routes(file):
    for i, line in enumerate(open(file)):
        for match in re.finditer(pattern, line):
            if "post" in match.group().lower():
                post_list.append(match.group())
            if "get" in match.group().lower():
                get_list.append(match.group())
            if "put" in match.group().lower():
                put_list.append(match.group())
            if "delete" in match.group().lower():
                delete_list.append(match.group())
    print('File: ' + file)
    print(str(len(post_list)) + ' post operations detected')
    print(str(len(get_list)) + ' get operations detected')
    print(str(len(put_list)) + ' put operations detected')
    print(str(len(delete_list)) + ' delete operations detected \n')


analyse_routes(file='fiqroutes')
analyse_routes(file='crvroutes')
