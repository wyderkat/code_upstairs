"""
" Copyright 2013 Tomasz Wyderka <wyderkat@cofoh.com>
"  www.cofoh.com
" Licensed under GPL-2
""

python << PY_END
import sys
from os import path
sys.path.insert(0, "/home/tom/cu")
sys.path.insert(0, "/home/tom/cu/vim")
import code_upstairs 
PY_END

autocmd VimResized * python code_upstairs.refresh_statusline()
autocmd CursorMoved * python code_upstairs.cursor_move_handler()
map <silent> <c-r> :python code_upstairs.refresh_statusline()<cr>
map <silent> <space>. :python code_upstairs.select_next_layer()<cr>
map <silent> <space>, :python code_upstairs.select_next_layer(inc=-1)<cr>
map <silent> <space>m :python code_upstairs.select_next_function()<cr>
map <silent> <space>n :python code_upstairs.select_next_function(inc=-1)<cr>
map <silent> <space>b :python code_upstairs.jump_to_function()<cr>
map <silent> <space>/ :python code_upstairs.heighlight_function()<cr>
