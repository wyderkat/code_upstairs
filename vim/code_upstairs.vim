python << PY_END
import vim
import sys
from os import path
sys.path.insert(0, "/home/tom/cu")
import cu
import one_line_tree

css = { 
       "sym" : {
         "left" : "(",
         "right" : ")",
         "middle" : ""
       },
       "col": {
       },
       "names": {
         "parents" : "P",
         "siblings" : "S",
         "childs" : "C",
       }
     }
fname = "main"

conn = cu.init_connection()

root = cu.Create_tree(conn, fname)
root.find_strong_layers()
root.find_all_distances( end_name = fname ) 
loc = cu.Location( root )
db = None

def cursor_moved():
  global db
  (r,c) = vim.current.window.cursor
  filename = vim.current.buffer.name
  base_filename = path.basename( filename )
  fun = loc.what( base_filename, int(r) )
  if fun == None:
    db = {} # TODO what when no function
  else:
    db = root.who(fun).what_is_upstairs()
  print_status()
  #vim.command('set statusline=%s\\ %s\\ %s' % (r, base_filename, fun) )


def print_status():
  cols = int( vim.eval("&columns") )
  sl = one_line_tree.render_line(db, ["childs","calc"], cols, css)
  sl = sl.replace(" ", "\\ ") # vim spaces
  vim.command('set statusline=%s' % sl)


PY_END

autocmd VimResized * python print_status()
autocmd CursorMoved * python cursor_moved()
noremap <silent> <c-r> :python print_status()<cr>
