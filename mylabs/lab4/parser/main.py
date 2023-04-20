# я ненавижу пайтон
# РЕВОЛЮЦИЯ В СФЕРЕ ПАРСИНГА!!!
def parse_xml(xml_string):
    """
    Парсит XML-строку в коллекцию элементов.
    """

    # Список для хранения дочерних элементов
    children = []

    # Пока строка не пуста
    while xml_string:
        # Удаляем пробелы и переносы строк в начале и конце строки
        xml_string = xml_string.strip()

        # Ищем первый открывающий тег
        start_tag_start = xml_string.find('<')
        start_tag_end = xml_string.find('>')

        # Проверка на пролог
        if xml_string[start_tag_start:start_tag_start + 5] == '<?xml':
            xml_string = xml_string[start_tag_end + 1:].strip()
            continue

        # Если нашли открывающий тег
        if start_tag_start != -1 and start_tag_end != -1 and start_tag_start < start_tag_end:
            # Ищем имя тега
            tag_name_start = start_tag_start + 1
            tag_name_end = xml_string.find(' ', tag_name_start)
            if tag_name_end == -1 or tag_name_end > start_tag_end:
                tag_name_end = start_tag_end
            tag_name = xml_string[tag_name_start:tag_name_end]

            # Ищем закрывающий тег
            end_tag_start = xml_string.find('</' + tag_name + '>', tag_name_start + 1)
            test_for_duplicate = xml_string.find('<' + tag_name + '>', tag_name_start + 1)
            while test_for_duplicate < end_tag_start and test_for_duplicate != -1:
                end_tag_start = xml_string.find('</' + tag_name + '>', end_tag_start + 1)
                test_for_duplicate = xml_string.find('<' + tag_name + '>', test_for_duplicate + 1)
            end_tag_end = end_tag_start + len(tag_name) + 3

            # Ищем атрибуты тега
            attributes = {}
            attr_start = tag_name_end
            while True:
                attr_name_start = xml_string.find(' ', attr_start, start_tag_end)
                if attr_name_start == -1:
                    break
                attr_name_end = xml_string.find('=', attr_name_start)
                if attr_name_end == -1:
                    break
                attr_name = xml_string[attr_name_start:attr_name_end].strip()
                attr_value_start = xml_string.find('"', attr_name_end)
                if attr_value_start == -1:
                    break
                attr_value_end = xml_string.find('"', attr_value_start + 1)
                if attr_value_end == -1:
                    break
                attr_value = xml_string[attr_value_start + 1:attr_value_end]
                attributes[attr_name] = attr_value
                attr_start = attr_value_end

            # Ищем текст элемента
            text = ''
            text_start = start_tag_end + 1
            # Пропускаем пробелы
            while xml_string[text_start].isspace():
                text_start += 1
            if not xml_string[text_start] == '<':
                text_end = end_tag_start
                text = xml_string[text_start:text_end].strip()

            # Рекурсивно парсим дочерние элементы
            inner_xml_start = start_tag_end + 1
            inner_xml_end = end_tag_start
            inner_xml = xml_string[inner_xml_start:inner_xml_end]
            children.append({
                'name': tag_name,
                'attributes': attributes,
                'text': text,
                'children': parse_xml(inner_xml)
            })

            # Дополняем до массива, если можно
            while end_tag_end < len(xml_string):
                # Обрезаем строку
                xml_string_nextstart = xml_string.find('<', end_tag_end + 1)
                xml_string_nextstart_end = xml_string.find('>', xml_string_nextstart + 1)
                # вычисляем конец тега
                xml_string_nextstart_nameend = xml_string.find(' ', xml_string_nextstart + 1)
                if xml_string_nextstart_nameend == -1 or xml_string_nextstart_nameend > xml_string_nextstart_end:
                    xml_string_nextstart_nameend = xml_string_nextstart_end
                tagname = xml_string[xml_string_nextstart + 1:xml_string_nextstart_nameend]
                xml_closetagname = xml_string.find('</' + tagname + '>', xml_string_nextstart_end + 1)
                test_for_duplicate = xml_string.find('<' + tagname + '>', xml_string_nextstart_end + 1)
                while test_for_duplicate < xml_closetagname and test_for_duplicate != -1:
                    xml_closetagname = xml_string.find('</' + tagname + '>', xml_closetagname + 1)
                    test_for_duplicate = xml_string.find('<' + tagname + '>', test_for_duplicate + 1)
                xml_string_nextstop = xml_closetagname + len(tagname) + 3
                # Проверяем, что это не окончание какого-то тега
                if xml_string[xml_string_nextstart + 1] == '/':
                    break
                single_xml = xml_string[xml_string_nextstart:xml_string_nextstop]
                parsed_xml = parse_xml(single_xml)
                if len(parsed_xml) == 1:
                    children.append(parsed_xml[0])
                end_tag_end = xml_string_nextstop
        return children

    # Возвращаем список дочерних элементов
    return children


def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start + len(needle))
        n -= 1
    return start


# Переводит коллекцию элементов в JSON-формат. Часть информации безуспешно теряется =(
def elements_to_json_str(elements, tab_count=0, first_element=True, complicated_array=True):
    result = ''
    if len(elements) != 1 and complicated_array:
        result += '\t' * tab_count + '\"' + elements[0]['name'] + '\" : [\n'
        first_element = True
    for element in elements:
        remove_comma = False
        if first_element:
            result += '\t' * tab_count + '{\n'
            first_element = False
            tab_count += 1
        elif complicated_array:
            result += '\t' * tab_count + '\"' + element['name'] + '\": {\n'
            tab_count += 1
        for atr in element['attributes']:
            result += '\t' * tab_count + '\"' + atr + '\":\"' + element['attributes'][atr] + '\",\n'
        if element['text']:
            remove_comma = True
            result += '\t' * tab_count + '\"' + element['name'] + '\":\"' + element['text'] + '\",\n'
        if remove_comma and complicated_array:
            result = result.rstrip(',\n')
            result += '\n'
        if element['children']:
            if element['children'][0]['children'] or element['children'][0]['attributes']:
                result += elements_to_json_str(element['children'], tab_count, False)
            else:
                result += elements_to_json_str(element['children'], tab_count, False, False)
        if complicated_array:
            tab_count -= 1
            result += '\t' * tab_count + '},\n'
    result = result.rstrip(',\n')
    result += '\n'
    if len(elements) != 1 and complicated_array:
        result += '\t' * tab_count + ']\n'
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
            result += '\t' * tab_count + '\"' + union_array_index + '\" : [\n'
            for element in union[union_array_index]:
                result += '\t' * tab_count + '{\n'
                tab_count += 1
                for atr in element['attributes']:
                    result += '\t' * tab_count + '\"' + atr + '\":\"' + element['attributes'][atr] + '\",\n'
                if element['text']:
                    result += '\t' * tab_count + '\"' + element['name'] + '\":\"' + element['text'] + '\",\n'
                if element['children']:
                    result += to_json_str(element['children'], tab_count, False)
                if is_array:
                    tab_count -= 1
                    result += '\t' * tab_count + '},\n'
            result = result.rstrip(',\n')
            result += '\n'
            result += '\t' * tab_count + ']\n'
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
        result += '}'
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


elements_from_xml = parse_xml(open('input.xml').read())
print(elements_from_xml)
open('output.json', mode='w').write(to_json_str(elements_from_xml))
