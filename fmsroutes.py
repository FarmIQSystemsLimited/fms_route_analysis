import re
import pprint

pattern = re.compile('"(.*?)"')


def process_dict_entry(first_domain_keyword_dict, route):
    route_list = route.replace('"', '')
    route_list = route_list.split('/')
    domain_key = route_list[0]
    if route_list[0] not in first_domain_keyword_dict.keys():
        first_domain_keyword_dict[domain_key] = {}
        first_domain_keyword_dict[domain_key]['Total Routes'] = 0
        first_domain_keyword_dict[domain_key]['Routes'] = []

    else:
        first_domain_keyword_dict[domain_key]['Routes'].append(route)
        first_domain_keyword_dict[domain_key]['Total Routes'] += 1


def clean_route(http_keyword, line):
    line = line.lstrip()
    line = line.replace('rest:' + http_keyword + ':/', '')
    return line


def analyse_routes(file):
    post_list = []
    get_list = []
    put_list = []
    delete_list = []

    first_domain_keyword_dict = {}

    for i, line in enumerate(open(file)):
        for match in re.finditer(pattern, line):
            route = match.group()
            if "post" in route.lower():
                route = clean_route(http_keyword='post', line=route)
                process_dict_entry(first_domain_keyword_dict, route)
                post_list.append(route)
            if "get" in route.lower():
                route = clean_route(http_keyword='get', line=route)
                process_dict_entry(first_domain_keyword_dict, route)
                get_list.append(route)
            if "put" in route.lower():
                route = clean_route(http_keyword='put', line=route)
                process_dict_entry(first_domain_keyword_dict, route)
                put_list.append(route)
            if "delete" in route.lower():
                route = clean_route(http_keyword='delete', line=route)
                process_dict_entry(first_domain_keyword_dict, route)
                delete_list.append(route)

    print('File: ' + file)
    print(str(len(post_list)) + ' post operations detected')
    print('e.g. ' + post_list[0])
    print(str(len(get_list)) + ' get operations detected')
    print('e.g. ' + get_list[0])
    print(str(len(put_list)) + ' put operations detected')
    print('e.g. ' + put_list[0])
    print(str(len(delete_list)) + ' delete operations detected')
    print('e.g. ' + delete_list[0])
    print('\n')

    pprint.pprint(first_domain_keyword_dict)

    print('Number of Top Level APIs: ' + str(len(first_domain_keyword_dict)))
    print('Number of Routes: ' + str(len(post_list) + len(get_list) + len(put_list) + len(delete_list)))


analyse_routes(file='fiqroutes')
