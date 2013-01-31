###
# Copyright 2013 Tomasz Wyderka <wyderkat@cofoh.com>
#  www.cofoh.com
# Licensed under GPL-2
##

import vim
from os import path
import cu
import one_line_tree

STYLE = { 
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
start_function = "main"

CONNECTION = cu.init_connection()
OLD_STATUSLINE = vim.eval("&statusline") 

ROOT = cu.Create_tree( CONNECTION, start_function)
ROOT.find_strong_layers()
ROOT.find_all_distances( end_name = start_function ) 

# functions locations in files
LOC = cu.Location( ROOT )
# function data DB
DB = None
# selection object
SEL = None


def cursor_move_handler():
  global DB
  global SEL
  (row,_) = vim.current.window.cursor
  filename = vim.current.buffer.name
  base_filename = path.basename( filename )
  function = LOC.what( base_filename, int(row) )
  if function != cursor_move_handler._previous_function:
    cursor_move_handler._previous_function = function
    if function == None:
      DB = None
    else:
      DB = ROOT.who(function).what_is_upstairs()
      SEL = [ DB.keys()[0] ]
    refresh_statusline()

cursor_move_handler._previous_function = None


def refresh_statusline():
  if DB:
    columns = int( vim.eval("&columns") )
    sl = one_line_tree.render_line(DB, SEL, columns, STYLE)
    sl = sl.replace(" ", "\\ ") # vim spaces
  else :
    sl = OLD_STATUSLINE
  vim.command('set statusline=%s' % sl)

def select_next_layer(inc=1):
  global SEL
  options = DB.keys()
  current = SEL[0]
  try :
    idx = options.index( current )
  except ValueError:
    idx = 0
  
  idx = (idx+inc) %len(options)
  SEL[0] = options[ idx ] 

  refresh_statusline()

   
