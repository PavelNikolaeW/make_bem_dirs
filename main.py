from sys import argv 
import re
import os

page_dir = os.path.join(os.curdir, 'pages')
block_dir = os.path.join(os.curdir, 'blocks')
IMPORTS = set()
NO_BEM_BLOCKS = f"""
/*--- NO BEM BLOCKS ---*/

@import url({os.pardir}/vendor/normalize.css);
@import url({os.pardir}/fonts/fonts.css);
@import url({os.pardir}/variables/colors.css);
"""
def parse(path):
		html = ''
		with open(path, "r", encoding="utf-8") as f:
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
		if (selector != ""):
				dir_file = f"{path}.css"
				IMPORTS.add(f"@import url({os.path.join(os.pardir, dir_file[2:])});\n")
				css_selector = f".{selector} {{\n\t\n}}"
				if not os.path.exists(dir_file):
						try:
								with open(dir_file, "w+", encoding="utf-8") as f:
										f.write(css_selector)
						except:
								print("FAIL make dir path = " + dir_file)

def make_imports_file(path):
		if (len(IMPORTS)):
				page_name = os.path.splitext(os.path.basename(path))[0]
				page_path = os.path.join(page_dir, page_name + ".css")
				with open(page_path, "w", encoding="utf-8") as f:
						f.write(NO_BEM_BLOCKS)
						imp = list(IMPORTS)
						block = ''
						oldblock = ''
						for n in sorted(imp, reverse=True):
								slesh = n.find(os.sep, 14 + len(block_dir))
								block = n[14 + len(block_dir): slesh]
								if (oldblock != block):
										s = f"\n/*--- {block.upper()} ---*/\n\n"
										f.write(s)
										oldblock = block
								f.write(n.replace(os.sep, "/", 15))


if __name__ == '__main__':
		path = ''
		if (len(argv) == 1):
				if os.path.exists('index.php'):
						path = 'index.php'
				elif os.path.exists('index.html'):
						path = 'index.html'
		elif (len(argv) > 1):
				if os.path.exists(argv[1]):
						path = argv[1]
				elif os.path.exists(argv[1] + '.php'):
						path = argv[1] + '.php'
				elif os.path.exists(argv[1] + '.html'):
						path = argv[1] + '.html'
		if (path != ''):
				classes = parse(path)
				make_dirs(classes)
				make_dir(page_dir)
				make_imports_file(path)
		else:
			print("i didn't find the file")


