import re
import pprint
import json
import os.path
import types
import csv

constants = types.SimpleNamespace()
constants.PUT = "put"
constants.GET = "get"
constants.POST = "post"
constants.DELETE = "delete"

pattern = re.compile('"(.*?)"')


def process_dict_entry(first_domain_keyword_dict, route, http_keyword):
    route_item = route.replace('"', '')
    route_list = route_item
    route_list = route_list.split('/')
    domain_key = route_list[0]
    if route_list[0] == 'get' or route_list[0] == 'post':
        domain_key = route_list[1]
    if domain_key not in first_domain_keyword_dict.keys():
        first_domain_keyword_dict[domain_key] = {}
        first_domain_keyword_dict[domain_key]['Total Routes'] = 0
        first_domain_keyword_dict[domain_key]['GET Routes'] = []
        first_domain_keyword_dict[domain_key]['POST Routes'] = []
        first_domain_keyword_dict[domain_key]['PUT Routes'] = []
        first_domain_keyword_dict[domain_key]['DELETE Routes'] = []

    first_domain_keyword_dict[domain_key][http_keyword.upper() + ' Routes'].append(route_item)
    first_domain_keyword_dict[domain_key]['Total Routes'] += 1


def clean_route(http_keyword, line):
    line = line.lstrip()
    line = line.replace('rest:' + http_keyword + ':/', '')
    return line


def analyse_routes(file):
    first_domain_keyword_dict = {}

    for i, line in enumerate(open(file)):
        for match in re.finditer(pattern, line):
            route = match.group()
            if constants.POST in route.lower():
                route = clean_route(http_keyword='post', line=route)
                process_dict_entry(first_domain_keyword_dict, route, constants.POST)

            if constants.GET in route.lower():
                route = clean_route(http_keyword='get', line=route)
                process_dict_entry(first_domain_keyword_dict, route, constants.GET)

            if constants.PUT in route.lower():
                route = clean_route(http_keyword='put', line=route)
                process_dict_entry(first_domain_keyword_dict, route, constants.PUT)

            if constants.DELETE in route.lower():
                route = clean_route(http_keyword='delete', line=route)
                process_dict_entry(first_domain_keyword_dict, route, constants.DELETE)

    pprint.pprint(first_domain_keyword_dict)

    print('\n Number of Top Level Keywords: ' + str(len(first_domain_keyword_dict)))

    with open('complete_api_route_dict.json', 'w') as file:
        file.write(json.dumps(first_domain_keyword_dict, indent=4, sort_keys=True))

    subdirectory = 'individual_dicts'
    try:
        os.mkdir(subdirectory)
    except FileExistsError:
        pass

    for item in first_domain_keyword_dict.items():
        file_name = item[0] + '.json'
        with open(os.path.join(subdirectory, file_name), 'w') as output_file:
            output_file.write(json.dumps(item, indent=4, sort_keys=True))

    route_counts = {}
    for item in first_domain_keyword_dict.items():
        route_counts[item[0]] = item[1]['Total Routes']
    pprint.pprint(sorted(route_counts.items(), key=lambda x: x[1]))

    with open('route_stats.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=route_counts.keys())
        writer.writeheader()
        writer.writerow(route_counts)


analyse_routes(file='fiqroutes')
