import re
import os
from pprint import pprint

path = r"C:\Users\User\Desktop\dev\server\index.html"
page_dir = os.path.join(os.path.abspath(os.curdir), 'pages')
block_dir = os.path.join(os.path.abspath(os.curdir), 'block')
IMPORTS = set()

def parse(path):
    html = ''
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    matches = re.findall(r'class="(.*?)"', html)
    return matches

def make_dirs(classes):
    for class_html in classes:
        for key in class_html.split(' '):
            path = "blocks"
            block_element = key.split('__')
            block_element_mod = key.split('_')
            if len(block_element) == 1 and len(block_element_mod) == 1:
                path = os.path.join(path, key)
                make_dir(path)
                make_file_css(os.path.join(path, key), key)
            elif len(block_element) == 1 and len(block_element_mod) > 1:
                path = os.path.join(path, block_element_mod[0], '_' + block_element_mod[1])
                make_dir(path)
                make_file_css(os.path.join(path, key), key)
            elif len(block_element) == 2 and len(block_element_mod) == 3:
                path = os.path.join(path, block_element[0], '__' + block_element[1])
                make_dir(path)
                make_file_css(os.path.join(path, key), key)
            elif len(block_element) == 2 and len(block_element_mod) > 3:
                path = os.path.join(path, block_element[0], '__' + block_element_mod[2], '_' + block_element_mod[3])
                make_dir(path)
                make_file_css(os.path.join(path, key), key)


def make_dir(path):
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except:
            pass


def make_file_css(path, selector):
    if (selector != ""):
        dir_file = f"{path}.css"
        IMPORTS.add(f"@import url({os.path.join(os.pardir, dir_file)});\n")
        css_selector = f".{selector} {{\n\t\n}}"
        if not os.path.exists(dir_file):
            with open(dir_file, "w+", encoding="utf-8") as f:
                f.write(css_selector)

def make_imports_file(path):
    if (len(IMPORTS)):
        page_name = os.path.splitext(os.path.basename(path))[0]
        page_path = os.path.join(page_dir, page_name + ".css")
        with open(page_path, "w", encoding="utf-8") as f:
            imp = list(IMPORTS)
            block = ''
            oldblock = ''
            for n in sorted(imp):
                slesh = n.find(os.sep, 22)
                block = n[22: slesh]
                if (oldblock != block):
                    s = f"\n/*--- {block.upper()} ---*/\n\n"
                    f.write(s)
                    oldblock = block
                f.write(n)


if __name__ == '__main__':
    classes = parse(path)
    make_dir("blocks")
    make_dirs(classes)
    make_dir(page_dir)
    make_imports_file(path)

