Для использования просто запустите скрипт в рабочей дериктории. Так же можно указать (имя файла) без расширения или с ним, например index или index.php, по умолчанию скрипт ищет index.php и index.html. Скрипт создаст папку blocks и в ней папки для блоков, а в них папки для элементов и модификаторов, а в них соответсвующие файлы. Так же появится папка pages, а в ней (имя файла).css где прописаны все импорты блоков плюс эти строчки: 
@import url(../vendor/normalize.css);
@import url(../fonts/fonts.css);
@import url(../variables/colors.css);
вы сами можете их изменить на что угодно.
