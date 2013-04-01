###
# Copyright 2013 Tomasz Wyderka <wyderkat@cofoh.com>
#  www.cofoh.com
# Licensed under GPL-2
##

from os import path
import code_upstairs_core
import one_line_tree
import vim

class CodeUpstairs:
  pass
# global storage 
cu = CodeUpstairs() 

def init( args ):
  if len(args) == 1:
    cu.DIR = args[0]
  else:
    cu.DIR = "."

  try:

    cu.CONNECTION = code_upstairs_core.init_connection( cu.DIR )

    cu.STYLE = one_line_tree.css # default css

    cu.START_FUNCTION = "main"

    cu.OLD_STATUSLINE = vim.eval("&statusline") 
    cu.OLD_STATUSLINE_VISIBILITY = vim.eval("&laststatus") 

    # without visited={} python uses old visited dictionary
    # reinitialization not possible
    # why ????
    cu.ROOT = code_upstairs_core.Create_tree( cu.CONNECTION, cu.START_FUNCTION, visited={})
    cu.ROOT.find_strong_layers()
    cu.ROOT.find_all_distances( end_name = cu.START_FUNCTION ) 
    #cu.ROOT.print_tree(layers=True)

    # functions locations in files
    cu.LOCATIONS = code_upstairs_core.Location( cu.ROOT )
    # function data cu.DB
    cu.DB = None
    if cu.OLD_STATUSLINE_VISIBILITY != "2":
      vim.command('set laststatus=%s' % "2")

    # selection object
    if cu.OLD_STATUSLINE == "":
      # we cannot use it now, because we are formatting everything with text
      #cu.USER_STATUSLINE = "%<%f\\ %h%m%r%=%-14.(%l,%c%V%)\\ %P" #default status line
      cu.USER_STATUSLINE = "%<%f %h%m%r%=%-14.(%l,%c%V%) %P" #default status line
    else:
      cu.USER_STATUSLINE = cu.OLD_STATUSLINE 

    # initial display - refresh
    cursor_move_handler()
  except code_upstairs_core.MissingSources:
    shutdown()
    return 1
  except code_upstairs_core.MissingScopeApp, e:
    if str(e)[:2] == "Py":
      return 3
    else:
      return 2
  return 0


def shutdown():
  global cu
  #
  code_upstairs_core.shutdown_connection( cu.CONNECTION )
  #
  sl = cu.OLD_STATUSLINE
  try:
    vim.command('set statusline=%s' % sl)
  except:
    print "DBG CMD>%s<" % sl

  vim.command('set laststatus=%s' % cu.OLD_STATUSLINE_VISIBILITY)
  #
  cu = CodeUpstairs() 



def cursor_move_handler():
  global cu # TEST
  (row,_) = vim.current.window.cursor
  filename = vim.current.buffer.name
  base_filename = path.basename( filename )
  function = cu.LOCATIONS.what( base_filename, int(row) )
  if function != cursor_move_handler._previous_function:
    cursor_move_handler._previous_function = function
    if function == None:
      cu.DB = None
    else:
      cu.DB = code_upstairs_core.FunctionDB( cu.ROOT.who(function) )
      cu.DB.prepend_text_layer( "-", cu.USER_STATUSLINE )
      cu.DB.select( layer = "childs" )
    refresh_statusline()

cursor_move_handler._previous_function = None


def refresh_statusline():
  if cu.DB:
    columns = int( vim.eval("&columns") )
    sl = one_line_tree.render_line(cu.DB, columns, cu.STYLE)
    sl = sl.replace(" ", "\\ ") # vim spaces
  else :
    sl = cu.OLD_STATUSLINE
  try:
    vim.command('set statusline=%s' % sl)
  except:
    print "DBG CMD>%s<" % sl

def select_next_layer( inc=1 ):
  cu.DB.select_next_layer( inc ) 
  refresh_statusline()

def select_next_fname( inc=1 ):
  cu.DB.select_next_fname( inc ) 
  refresh_statusline()

def jump_to_fname():
  (_, fname) = cu.DB.get_selected()
  if fname:
    where = cu.LOCATIONS.where( fname )
    print "jumping to %s" % str(where) 
    if where != None:
      vim.command("edit +%d %s" % (where[1], cu.DIR + "/" + where[0]))

def heighlight_fname():
  (_, fname) = cu.DB.get_selected()
  if fname:
    vim.command("/%s" % fname)
   
