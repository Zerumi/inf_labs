import re


def parse_xml(xml_string):
    root_pattern = re.compile(r'<(\w+)(.*?)>(.*?)</\1>', re.DOTALL)
    attr_pattern = re.compile(r'(\w+)="([^"]+)"')
    xml_string = xml_string.strip()

    node_match = root_pattern.match(xml_string)
    result = []
    if node_match:
        tag_name = node_match.group(1)
        attributes = dict(attr_pattern.findall(node_match.group(2)))
        text = ''
        children = parse_xml(node_match.group(3).strip())
        if len(children) == 0:
            text = node_match.group(3)
        result.append({'name': tag_name, 'attributes': attributes, 'text': text, 'children': children})
        cursor = node_match.span()[1]
        while cursor < len(xml_string):
            temp_count = len(xml_string[cursor::])
            node_match = root_pattern.match(xml_string[cursor::].lstrip())
            if node_match:
                tag_name = node_match.group(1)
                attributes = dict(attr_pattern.findall(node_match.group(2)))
                text = ''
                children = parse_xml(node_match.group(3).strip())
                if len(children) == 0:
                    text = node_match.group(3)
                result.append({'name': tag_name, 'attributes': attributes, 'text': text, 'children': children})
                cursor += node_match.span()[1] + temp_count - len(xml_string[cursor::].lstrip())
    return result


def to_json_str(elements_xml, tab_count=0, is_first_iter=True):
    result = ''
    is_array = False
    union = union_by_name(elements_xml)
    if len(union) < len(elements_xml):
        is_array = True
    if is_first_iter:
        result += '{\n'
        tab_count += 1
    if is_array:
        for union_array_index in union:
            matched_non_single_element = len(union[union_array_index]) > 1
            if matched_non_single_element:
                result += '\t' * tab_count + '\"' + union_array_index + '\" : [\n'
                tab_count += 1
            for element in union[union_array_index]:
                if matched_non_single_element:
                    result += '\t' * tab_count + '{\n'
                    tab_count += 1
                for atr in element['attributes']:
                    result += '\t' * tab_count + '\"' + atr + '\":\"' + element['attributes'][atr] + '\",\n'
                if element['text']:
                    result += '\t' * tab_count + '\"' + element['name'] + '\":\"' + element['text'] + '\",\n'
                if element['children']:
                    result += to_json_str(element['children'], tab_count, False)
                if matched_non_single_element:
                    result = result.rstrip(',\n')
                    result += '\n'
                    tab_count -= 1
                    result += '\t' * tab_count + '},\n'
            if matched_non_single_element:
                result = result.rstrip(',\n')
                result += '\n'
            if len(union[union_array_index]) > 1:
                tab_count -= 1
                result += '\t' * tab_count + '],\n'
        result = result.rstrip(',\n')
        result += '\n'
    else:
        for element in elements_xml:
            if len(element['children']) > 1:
                result += '\t' * tab_count + '\"' + element['name'] + '\": {\n'
                tab_count += 1
            for atr in element['attributes']:
                result += '\t' * tab_count + '\"' + atr + '\":\"' + element['attributes'][atr] + '\",\n'
            if element['text']:
                result += '\t' * tab_count + '\"' + element['name'] + '\":\"' + element['text'] + '\",\n'
            if element['children']:
                result += to_json_str(element['children'], tab_count, False)
            if len(element['children']) > 1:
                tab_count -= 1
                result += '\t' * tab_count + '},\n'
        result = result.rstrip(',\n')
        result += '\n'
    if is_first_iter:
        result += '}\n'
    return result


def union_by_name(list_data):
    result_dict = {}

    for value in list_data:
        name = value["name"]
        if name in result_dict:
            result_dict[name].append(value)
        else:
            result_dict[name] = [value]

    return result_dict


def main():
    xml_str = open('input.xml').read()
    parsed_xml = parse_xml(xml_str)
    # print(parsed_xml)
    json_string = to_json_str(parsed_xml)
    # print(json_string)
    open('output_add2.json', 'w').write(json_string)
