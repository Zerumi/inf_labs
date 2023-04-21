# после этого мир кажется светлым и прекрасным
# написано сразу после окончания написания ручного парсера
import xmltodict
import json

xml = open('input.xml').read()

ordered_dict = xmltodict.parse(xml)

json_str = json.dumps(ordered_dict, ensure_ascii=False, indent=4)

open('output_add1.json', 'w').write(json_str)
