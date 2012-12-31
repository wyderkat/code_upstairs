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

class Function(object):
  def __init__(me, name):
    me.calls = {} # Functions which are called from 'me' Function 
    me.used  = {} # Functions which are calling 'me' Function
                  # This is also list of parrents
    me.name = name # Function name, duplicated from parents.calls dictionary
  def add_new_call(me, name):
    f = Function( name ) 
    me.calls[ name ] = f # tree structure
    f.used[ me.name ] = me # backreference
    return f
  def add_existing_call(me, she):
    me.calls[ she.name ] = she # tree structure
    she.used[ me.name ] = me # backreference
    return she
  def print_tree(me, depth=0, parents={}):
    print "  " * depth, me.name
    if me.name in parents:
      print "  " * depth, ".. RECURSION (%s)" % me.name
      return
    else:
      if len(me.calls) == 0:
         #print "  " * depth, "-"
         return
      else:
        parents[ me.name ] = 1 # 1 is just flag
        for fname, f in me.calls.items():
           f.print_tree(depth+1)
        del( parents[ me.name ] )
          
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




def readln( ):
  pipes.stdout.read( str + "\n" )
  pipes.str.flush()

CSCOPE = 'cscope'
                    
pipes = Popen([CSCOPE,'-l','-k'],stdin=PIPE,stdout=PIPE,stderr=PIPE)  
                                        
#fname = "theater_init"
fname = "main"
if len(sys.argv) > 1:
  fname = sys.argv[1]


T = {} # tree of functions, keys are functions names, values are called functions or None

visited = {}

def create_tree ( f ) :
  visited[f.name] = f
  outs = writeln("2"+f.name)
  #print len(outs)
  for hit in outs:
    #print hit
    try:
      f1 = visited[ hit ]
      f.add_existing_call( f1 ) 
    except KeyError: # not visited 
      sub_f = f.add_new_call( hit ) 
      create_tree( sub_f )


T = Function(fname)
create_tree(T)

T.print_tree()
