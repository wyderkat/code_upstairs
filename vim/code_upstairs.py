###
# Copyright 2013 Tomasz Wyderka <wyderkat@cofoh.com>
#  www.cofoh.com
# Licensed under GPL-2
##

import vim
from os import path
import code_upstairs_core
import one_line_tree

cu_STYLE = one_line_tree.css # default css

cu_START_FUNCTION = "main"

cu_CONNECTION = code_upstairs_core.init_connection()

cu_OLD_STATUSLINE = vim.eval("&statusline") 

cu_ROOT = code_upstairs_core.Create_tree( cu_CONNECTION, cu_START_FUNCTION)
cu_ROOT.find_strong_layers()
cu_ROOT.find_all_distances( end_name = cu_START_FUNCTION ) 
#cu_ROOT.print_tree(layers=True)

# functions locations in files
cu_LOCATIONS = code_upstairs_core.Location( cu_ROOT )
# function data cu_DB
cu_DB = None
# selection object
if cu_OLD_STATUSLINE == "":
  # we cannot use it now, because we are formatting everything with text
  #cu_USER_STATUSLINE = "%<%f\\ %h%m%r%=%-14.(%l,%c%V%)\\ %P" #default status line
  cu_USER_STATUSLINE = "%<%f %h%m%r%=%-14.(%l,%c%V%) %P" #default status line
else:
  cu_USER_STATUSLINE = cu_OLD_STATUSLINE 


def cursor_move_handler():
  global cu_DB
  (row,_) = vim.current.window.cursor
  filename = vim.current.buffer.name
  base_filename = path.basename( filename )
  function = cu_LOCATIONS.what( base_filename, int(row) )
  if function != cursor_move_handler._previous_function:
    cursor_move_handler._previous_function = function
    if function == None:
      cu_DB = None
    else:
      cu_DB = code_upstairs_core.FunctionDB( cu_ROOT.who(function) )
      cu_DB.prepend_text_layer( "-", cu_USER_STATUSLINE )
      cu_DB.select( layer = "childs" )
    refresh_statusline()

cursor_move_handler._previous_function = None


def refresh_statusline():
  if cu_DB:
    columns = int( vim.eval("&columns") )
    sl = one_line_tree.render_line(cu_DB, columns, cu_STYLE)
    sl = sl.replace(" ", "\\ ") # vim spaces
  else :
    sl = cu_OLD_STATUSLINE
  try:
    vim.command('set statusline=%s' % sl)
  except:
    print "DBG CMD>%s<" % sl

def select_next_layer( inc=1 ):
  cu_DB.select_next_layer( inc ) 
  refresh_statusline()

def select_next_fname( inc=1 ):
  cu_DB.select_next_fname( inc ) 
  refresh_statusline()

def jump_to_fname():
  (_, fname) = cu_DB.get_selected()
  if fname:
    where = cu_LOCATIONS.where( fname )
    print "jumping to %s" % str(where) 
    if where != None:
      vim.command("edit +%d %s" % (where[1], where[0]))

def heighlight_fname():
  (_, fname) = cu_DB.get_selected()
  if fname:
    vim.command("/%s" % fname)
   
