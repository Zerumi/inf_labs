# я... синдзи икари
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


def to_markdown_str(elements_xml, current_head_count=1):
    if current_head_count > 6:
        current_head_count = 6
    result = ''
    is_array = False
    union = union_by_name(elements_xml)
    if len(union) < len(elements_xml):
        is_array = True
    if is_array:
        for union_array_index in union:
            matched_non_single_element = len(union[union_array_index]) > 1
            index = 1
            for element in union[union_array_index]:
                if matched_non_single_element:
                    result += '\n' + union_array_index + str(index) + '\n\n'  # start complex element
                    result += '|||\n'
                    result += '|---|---|\n'
                for atr in element['attributes']:
                    result += '| *' + atr + '* | *' + element['attributes'][atr] + '* |\n'
                if element['text']:
                    result += '| ' + element['name'] + ' | ' + element['text'] + ' |\n'
                if element['children']:
                    result += to_markdown_str(element['children'])
                index += 1
                if matched_non_single_element:
                    result += '\n'
        result += '\n'
    else:
        for element in elements_xml:
            if len(element['children']) > 1:
                result += '#' * current_head_count + ' ' + element['name'] + ':\n\n'  # single element
                result += '|||\n'
                result += '|---|---|\n'
            for atr in element['attributes']:
                result += '| *' + atr + '* | *' + element['attributes'][atr] + '* |\n'  # attr
            if element['text']:
                result += '| ' + element['name'] + ' | ' + element['text'] + ' |\n'  # text
            if element['children']:
                result += to_markdown_str(element['children'], current_head_count + 1)
            if len(element['children']) > 1:
                result += '\n'
        result += '\n'
    return result.rstrip()


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
open('output_add4.md', mode='w').write(to_markdown_str(elements_from_xml))
