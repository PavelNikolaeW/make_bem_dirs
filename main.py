from sys import argv
import argparse
import re
import os
import my_env


def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--set-dir-pages', default='', help="set directory for page.css")
    parser.add_argument('-b', '--set-dir-blocks', default='', help='set directory for bem blocks')
    parser.add_argument('-r', '--reset', type=bool, default=False, help='set catalog for <pages> pages and for blocks <blocks>')
    parser.add_argument('-f', '--file', default='', help="file with markup")
    parser.add_argument('-a', '--add-class', default='', nargs="+", help='If there is no class in the html markup, but it needs to be included, it needs to be added to the local list')
    parser.add_argument('-d', '--remove-class', help='remove class from local list', nargs="+")
    parser.add_argument('--remove-import', help='remove additional files', nargs="+")
    parser.add_argument('--add-import', help='add additional files', nargs="+")
    parser.add_argument('-s', '--show', help='show local wariable', type=bool, default=False)
    return parser


page_dir = os.path.join(*my_env.page_dir.split('/'))
block_dir = os.path.join(*my_env.block_dir.split('/'))
ENV = os.path.join(os.path.dirname(__file__), 'my_env.py')
IMPORTS = set()

def parse(path):
		html = ''
		with open(os.path.join(*path.split('/')), "r", encoding="utf-8") as f:
				html = f.read()
				matches = re.findall(r'class="(.*?)"', html)
				return matches


def make_dirs(classes):
		make_dir(block_dir)
		for class_html in classes:
				for key in class_html.split(' '):
						path = block_dir
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
						print("FAIL make dir path = " + path)


def make_file_css(path, selector):
		n = len(block_dir.split(os.sep)) - 1
		if (selector != ""):
				dir_file = f"{path}.css"
				IMPORTS.add(f"@import url({os.path.join(my_env.transition, *dir_file.split(os.sep)[n:])});\n")
				css_selector = f".{selector} {{\n\t\n}}"
				if not os.path.exists(dir_file):
						try:
								with open(dir_file, "w+", encoding="utf-8") as f:
										f.write(css_selector)
						except:
								print("FAIL make dir path = " + dir_file)


def make_imports_file(path):
		make_dir(page_dir)
		block_name = block_dir.split(os.sep)[-1]
		if (len(IMPORTS)):
				page_name = os.path.splitext(os.path.basename(path))[0]
				page_path = os.path.join(page_dir, page_name + ".css")
				with open(page_path, "w", encoding="utf-8") as f:
						imp = list(IMPORTS)
						block = ''
						oldblock = ''
						for str_import in sorted(imp, reverse=True):
								print(str_import)
								start_block = (str_import.find(block_name) + len(block_name) + 1)
								end_block = str_import.find(os.sep, start_block + 1)
								if (end_block == -1):
										str_import = "\n" + str_import
								else:
										block = str_import[start_block: end_block]
								if (oldblock != block):
										f.write(f"\n/*--- {block.upper()} ---*/\n\n")
										oldblock = block
								f.write(str_import.replace(os.sep, "/", 15))


def change_local_var(var, new_val, add=False, remove=False):
		new_env = []
		with open(ENV, 'r', encoding='utf-8') as f:
				line = f.readline()
				while line:
						key, val = line.split(' = ')
						if key == var:
								if add:
										val = set(val.strip("'\n ").split(' ') + new_val)
										val = f"'{' '.join(list(val))}'"
								elif remove:
										val = set(val.strip("'\n ").split(' ')) - set(new_val)
										val = f"'{' '.join(list(val))}'"
								else:
										val = f"'{new_val}'"
								print(f"variable <{var}> set in {val}")
						new_env.append(f'{key} = {val.strip()}')
						line = f.readline()
		with open(ENV, 'w', encoding='utf-8') as f:
				for line in new_env:
						print(line, file=f)

def add_class(classes):
		change_local_var('classes', classes, add=True)

if __name__ == '__main__':
		parser = createParser()
		namespace = parser.parse_args(argv[1:])
		if namespace.add_class:
				change_local_var('classes', namespace.add_class, add=True)
		if namespace.remove_class:
				change_local_var('classes', namespace.remove_class, remove=True)
		if namespace.add_import:
				change_local_var('imports', namespace.add_import, add=True)
		if namespace.remove_import:
				change_local_var('imports', namespace.remove_import, remove=True)
		if namespace.reset:
				change_local_var('page_dir', 'pages')
				change_local_var('block_dir', 'blocks')
		if namespace.show:
				with open(ENV, 'r') as f:
						print(f.read())
		if namespace.set_dir_pages != '':
				change_local_var('page_dir', namespace.set_dir_pages)
		if namespace.set_dir_blocks != '':
				change_local_var('block_dir', namespace.set_dir_blocks)
		if namespace.file != '':
				change_local_var('file', namespace.file)

		classes = parse(my_env.file) + my_env.classes.split(' ')
		for path in my_env.imports.split(' '):
				if (path != ''):
						IMPORTS.add(f"@import url({path});\n")
		make_dirs(classes)
		make_imports_file(my_env.file)