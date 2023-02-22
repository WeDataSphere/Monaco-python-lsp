def filter_list_item1(item):
    if item["name"] in {"python引擎设置", "spark引擎设置"}:
        return True


def filter_list_item2(item):
    if item["key"] in {"python.version", "spark.python.version"}:
        return True
