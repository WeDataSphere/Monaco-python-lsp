import re

def filter_list_item1(item):
    if item["name"] in {"python引擎设置", "spark引擎设置"}:
        return True


def filter_list_item2(item):
    if item["key"] in {"python.version", "spark.python.version"}:
        return True


def read_file(file_path):
    with open(file_path, encoding='utf-8') as file_obj:
        lines = file_obj.readlines()
        num_imports = 0
        content_lines = []
        for line in lines:
            if re.match(r'^\s*(import|from\s+\S+\s+import)\s+', line):
                num_imports += 1
            content_lines.append(line)
        content = ''.join(content_lines)
        num_lines = len(lines)
        result = {'content': content, 'num_lines': num_lines, 'num_imports': num_imports}
        return result
