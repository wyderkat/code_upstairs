###
# Copyright 2013 Tomasz Wyderka <wyderkat@cofoh.com>
#  www.cofoh.com
# Licensed under GPL-2
##

import vim
from os import path
import cu
import one_line_tree


STYLE = one_line_tree.css # default css

start_function = "main"

CONNECTION = cu.init_connection()

OLD_STATUSLINE = vim.eval("&statusline") 

ROOT = cu.Create_tree( CONNECTION, start_function)
ROOT.find_strong_layers()
ROOT.find_all_distances( end_name = start_function ) 
#ROOT.print_tree(layers=True)

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
      try:
        layer = DB.keys()[2]
      except IndexError:
        layer = None
      try:
        function = DB[layer].keys()[0]
      except IndexError:
        function = None
      SEL = [ layer, function ]
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
  try:
    SEL[1] = DB[ SEL[0] ].keys()[0]
  except IndexError:
    SEL[1] = None

  refresh_statusline()

def select_next_function(inc=1):
  global SEL
  current_layer = SEL[0]
  options = DB[current_layer].keys()
  current = SEL[1]
  try :
    idx = options.index( current )
  except ValueError:
    idx = 0
  
  idx = (idx+inc) %len(options)
  SEL[1] = options[ idx ] 

  refresh_statusline()

def jump_to_function():
  function = SEL[1]
  if function:
    where = LOC.where( function )
    print "jumping to %s" % str(where) 
    if where != None:
      vim.command("edit +%d %s" % (where[1], where[0]))

def heighlight_function():
  function = SEL[1]
  if function:
    vim.command("/%s" % function)
   
