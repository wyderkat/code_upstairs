#!/usr/bin/env python
###
# Copyright 2013 Tomasz Wyderka <wyderkat@cofoh.com>
#  www.cofoh.com
# Licensed under GPL-2
##
from collections import OrderedDict as OD
from code_upstairs_core import Function, FunctionDB


css = { 
        "sym" : {
          "left" : "(",
          "right" : ")",
          "middle" : "",
          "sel_l" : "*",
          "sel_r" : "*",
        },
        "col": {
        },
        "names": {
          "parents" : "P",
          "siblings" : "S",
          "childs" : "C",
          "status" : "-",
        }
      }

def main( current_sel, width ):
  if not len( current_sel ):
    current_sel = ["childs", "acc"]
  stub = Function("stub")
  stub.find_strong_layers()
  db = FunctionDB( stub )
  db.D = OD ([ ("parents",  OD([ ("main",0) ]) ) , 
               ("siblings", OD([ ("init",0), ("update",0) ]) ) , 
               ("childs",   OD([ ("calc",0), ("precalc",0), ("acc",0) ]) ),
               ("3",        OD([ ("ola",0), ("ma",0) ]) ), 
               ("4",        OD([ ("kota",0) ]) ),
               (">4",       OD([ ("fx",0), ("xx123456789"*6,0) ]) )
               ])
  db.prepend_text_layer("-", "Ola i kot sa w domu")
  db.select( current_sel[0], current_sel[1] )

  return render_line( db, width, css )

def render_line( db, width, css ):
  rendered_elements = OD( )
  current_selected = db.get_selected()[0]
  for l in db.get_all_layers():
    if l == current_selected:
      # skip now, just placeholder
      render = ""
    else:
      render = render_layer( db, l, 0, css )

    rendered_elements[ l ] = render

  totalwidth = 0
  for s in rendered_elements.values():
    totalwidth += len( s )

  if totalwidth >= width:
      print "not enough space to render"
      return "-" * width
  # missing selected element
  rendered_elements[ current_selected ] = \
        render_layer( db, current_selected, width - totalwidth , css )

  #put it back together
  return "".join( rendered_elements.values() )

  
def render_layer( db, layer, width, css ):

  out = css["sym"]["left"]
  try:
    out += css["names"][layer]
  except KeyError:
    out += layer

  if db.is_selected( layer=layer ): 
    rendered_subelements = OD( )
    # TODO
    if db.is_text_layer( layer ):
      # in case of flat text element, just print it
      rendered_subelements[ layer ] = db.get_text_layer( layer )
    else:
      for f in db.get_fnames_in_layer( layer ):
        render = render_fname( db, layer, f, 0, css )
        rendered_subelements[ f ] = render

    totalwidth = 0
    for s in rendered_subelements.values():
      totalwidth += len( s )

    #put it back together
    out += " " +  " ".join( rendered_subelements.values() ) + " "
    right = css["sym"]["right"] 
    space = width - len(out) - len(right)
    if space >= 0:
      out += " " * space + right
    else:
      print "width %d space %d" % ( width, space )
      out = out[ : width-len(right) ] + right
  else:
    # not selected layer
    out += css["sym"]["right"]

  return out

def render_fname( db, layer, fname, width, css ):
  if db.is_selected( layer=layer, fname=fname ): 
    return css["sym"]["sel_l"] + fname + css["sym"]["sel_r"] 
  else:
    return fname

if __name__ == "__main__": 
  import sys
  print main( sys.argv[1:], 80 )

