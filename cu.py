#!/usr/bin/env python
###
# Copyright 2013 Tomasz Wyderka <wyderkat@cofoh.com>
#  www.cofoh.com
# Licensed under GPL-2
##
from subprocess import Popen,PIPE  
from time import sleep
from pdb import set_trace as trace
import sys

CSCOPE = 'cscope'

visited = {}
def create_tree( f ) :
  visited[f.name] = f
  outs = writeln("2"+f.name)
  for hit in outs:
    try:
      f1 = visited[ hit ]
      f.add_existing_call( f1 ) 
    except KeyError: # not visited 
      definition = writeln("1"+hit)
      if len(definition) > 0: # it's function in our project
        sub_f = f.add_new_call( hit ) 
        create_tree( sub_f )

def writeln( str ):
  pipes.stdin.write( str + "\n" )
  pipes.stdin.flush()
  line = pipes.stdout.readline()
  try:
    no_of_lines = int( line.split()[2] ) 
  except IndexError:
    print "IndexError: " + line
    print "STR: " + str
  #print "NO %d" %no_of_lines
  result = []
  for i in range(no_of_lines):
    line = pipes.stdout.readline()
    elements = line.split()
    #print elements[1]
    result.append(elements[1])
  return result

class Function(object):
  all = {} # non recurisve list of all Functions
  def __init__(me, name):
    me.calls = {} # Functions which are called from 'me' Function 
    me.used  = {} # Functions which are calling 'me' Function
                  # This is also list of parrents
    me.name = name # Function name, duplicated from parents.calls dictionary
    Function.all[ name ] = me
  def add_new_call(me, name):
    f = Function( name ) 
    me.calls[ name ] = f # tree structure
    f.used[ me.name ] = me # backreference
    return f
  def add_existing_call(me, she):
    me.calls[ she.name ] = she # tree structure
    she.used[ me.name ] = me # backreference
    return she
  def print_tree(me, layers = False, graph=False, depth=0, parents={}):
    indentation = "    " * depth
    head = ""
    tail = ""
    if len(me.used) > 1:
      tail += str(len(me.used))
    if graph:
      tail += str(me.used.keys())
    if layers:
      try:
        tail += "             [[ %s ]]" % me.strong_layer
      except AttributeError:
        pass
    print head, indentation , me.name, tail
    if me.name in parents:
      print indentation, ".. RECURSION (%s)" % me.name
      return
    else:
      if len(me.calls) == 0:
         #print indentation, "-"
         return
      else:
        parents[ me.name ] = 1 # 1 is just flag
        for fname, f in me.calls.items():
           f.print_tree(layers, graph, depth+1, parents)
        del( parents[ me.name ] )
  def find_strong_layers( me ):
    me.strong_layers = {}
    for f in Function.all.values():
      if len(f.used) == 1:
        #print "name %s used %s" % (f.name, f.used.keys()[0] )
        f.strong_layer = f.used.keys()[0]
        try: 
          me.strong_layers[ f.used.keys()[0] ].append( f )
        except KeyError:
          me.strong_layers[ f.used.keys()[0] ] = [ ( f ) ]
  def print_strong_layers( me ):
    counter = 0
    for k,v in me.strong_layers.items():
      for f in v:
        print "%s " % f.name ,
        counter += 1
      print "=> %s" % k 
    print "STRONG RATIO %g" % (float(counter)/len(Function.all))

          


if __name__ == "__main__":

  #fname = "theater_init"
  fname = "main"
  if len(sys.argv) > 1:
    fname = sys.argv[1]

  pipes = Popen([CSCOPE,'-l','-k','-R'],stdin=PIPE,stdout=PIPE,stderr=PIPE)  

  T = Function(fname)
  create_tree(T)
  T.find_strong_layers()
  T.print_tree(layers=True)
  print "====="
  T.print_strong_layers()
