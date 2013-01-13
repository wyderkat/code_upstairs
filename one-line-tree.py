#!/usr/bin/env python
###
# Copyright 2013 Tomasz Wyderka <wyderkat@cofoh.com>
#  www.cofoh.com
# Licensed under GPL-2
##
from collections import OrderedDict as OD


def main( current_sel ):
  if not len( current_sel ):
    current_sel = ["childs", "acc"]
  fname = "kick"
  tree = OD ([ ("parents",  OD([ ("main",0) ]) ) , 
               ("siblings", OD([ ("init",0), ("update",0) ]) ) , 
               ("childs",   OD([ ("calc",0), ("precalc",0), ("acc",0) ]) ),
               ("3",        OD([ ("ola",0), ("ma",0) ]) ), 
               ("4",        OD([ ("kota",0) ]) ),
               (">4",       OD([ ("fx",0), ("xx123456789"*6,0) ]) )
               ])
  width = 80

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


  print render_line( tree, current_sel, width, css )

def render_line( tree, current_sel, width, css ):
  rendered_elements = OD( )
  e_sel = current_sel[0]
  for e,sub_e in tree.items():
    if e == e_sel:
      # skip now, just placeholder
      render = ""
    else:
      render = render_element( e, tree, None, 0, css )

    rendered_elements[ e ] = render

  totalwidth = 0
  for s in rendered_elements.values():
    totalwidth += len( s )

  if totalwidth >= width:
      print "not enough space to render"
      return " " * width
  # missing selected element
  rendered_elements[ e_sel ] = \
        render_element( e_sel, tree, current_sel[1:], width - totalwidth , css )

  #put it back together
  return "".join( rendered_elements.values() )

  
def render_element( e_curr, tree, current_sel, width, css ):

  out = css["sym"]["left"]
  try:
    out += css["names"][e_curr]
  except KeyError:
    out += e_curr

  if current_sel == None: 
    # not selected element
    out += css["sym"]["right"]
  else:
    # selected element
    rendered_subelements = OD( )
    for sub_e,subsub_e in tree[e_curr].items():
      # width here is much too much
      render = render_subelement( sub_e, tree, current_sel[1:], 0, css )
      rendered_subelements[ sub_e ] = render

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


  return out

def render_subelement( e_curr, tree, current_sel, width, css ):
  return e_curr

if __name__ == "__main__": 
  import sys
  main( sys.argv[1:] )

