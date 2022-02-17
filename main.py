import re
import os
from pprint import pprint

path = r"./your/html/file"

def parse(path):
    html = ''
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    matches = re.findall(r'class="(.*?)"', html)
    return matches

def make_dirs(classes):
    imports = set()
    for class_html in classes:
        for key in class_html.split(' '):
            path = "blocks"
            block_element = key.split('__')
            block_element_mod = key.split('_')
            if len(block_element) == 1 and len(block_element_mod) == 1:
                path = os.path.join(path, key)
                make_dir(path)
                make_file_css(os.path.join(path, key), key)
                imports.add(f"@import url({os.path.join('..', path, key)});")
            elif len(block_element) == 1 and len(block_element_mod) > 1:
                path = os.path.join(path, block_element_mod[0], '_' + block_element_mod[1])
                make_dir(path)
                make_file_css(os.path.join(path, key), key)
                imports.add(f"@import url({os.path.join('..', path, key)});")
            elif len(block_element) == 2 and len(block_element_mod) == 3:
                path = os.path.join(path, block_element[0], '__' + block_element[1])
                make_dir(path)
                make_file_css(os.path.join(path, key), key)
                imports.add(f"@import url({os.path.join('..', path, key)});")
            elif len(block_element) == 2 and len(block_element_mod) > 3:
                path = os.path.join(path, block_element[0], '__' + block_element_mod[2], '_' + block_element_mod[3])
                make_dir(path)
                make_file_css(os.path.join(path, key), key)
                imports.add(f"@import url({os.path.join('..', path, key)});")
    return imports


def make_dir(path):
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except:
            pass


def make_file_css(path, selector):
    dir_file = f"{path}.css"
    css_selector = f".{selector} {{\n\t\n}}"
    if not os.path.exists(dir_file):
        with open(dir_file, "w+", encoding="utf-8") as f:
            f.write(css_selector)


if __name__ == '__main__':
    classes = parse(path)
    make_dir("blocks")
    imports = make_dirs(classes)
    pprint(imports)
