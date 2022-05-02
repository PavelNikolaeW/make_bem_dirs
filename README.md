The script receives a file name with HTML markup as input and creates a nested file structure using the BEM methodology.

usage: main.py [-h] [-p SET_DIR_PAGES] [-b SET_DIR_BLOCKS] [-r RESET] [-f FILE] [-a ADD_CLASS [ADD_CLASS ...]] [-d REMOVE_CLASS [REMOVE_CLASS ...]]
               [--remove-import REMOVE_IMPORT [REMOVE_IMPORT ...]] [--add-import ADD_IMPORT [ADD_IMPORT ...]] [-s SHOW]

options:
  -h, --help            show this help message and exit
  -p SET_DIR_PAGES, --set-dir-pages SET_DIR_PAGES
  set directory for page.css
  -b SET_DIR_BLOCKS, --set-dir-blocks SET_DIR_BLOCKS
                        set directory for bem blocks
  -r RESET, --reset RESET
                        set catalog for pages <pages> and for blocks <blocks>
  -f FILE, --file FILE  file with markup
  -a ADD_CLASS [ADD_CLASS ...], --add-class ADD_CLASS [ADD_CLASS ...]
                        If there is no class in the html markup, but it needs to be included, it needs to be added to the local list
  -d REMOVE_CLASS [REMOVE_CLASS ...], --remove-class REMOVE_CLASS [REMOVE_CLASS ...]
                        remove class from local list
  --remove-import REMOVE_IMPORT [REMOVE_IMPORT ...]
                        remove additional files
  --add-import ADD_IMPORT [ADD_IMPORT ...]
                        add additional files
  -s SHOW, --show SHOW  show local wariable
