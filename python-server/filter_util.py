def filter_list_item1(item):
    if item["name"] in {"python引擎设置", "spark引擎设置"}:
        return True


def filter_list_item2(item):
    if item["key"] in {"python.version", "spark.python.version"}:
        return True


def read_file(file_path):
    with open(file_path, encoding='utf-8') as file_obj:
        lines = file_obj.readlines()
        num_lines = len(lines)
        content_lines = []
        if not lines[-1].endswith('\n'):
            lines[-1] += '\n'
        for line in lines:
            content_lines.append(line)
        content = ''.join(content_lines)
        result = {'content': content, 'num_lines': num_lines}
        return result

if __name__ == '__main__':
    print(read_file("pre-import/pre_compile_Import.py"))