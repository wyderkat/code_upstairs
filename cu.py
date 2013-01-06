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
from copy import deepcopy

CSCOPE = 'cscope'

visited = {}
def create_tree( f ) :
  """
  recursive tree made of Function nodes
  """
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
  """
  write command line to cscope -l 
  and read output
  """
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

def first_the_same_element_in_lists( l1, l2 ):
  """
  find the first common element in two lists
  Return (that element, index in l1, index in l2)
  """
  i1 = 0
  for e1 in l1:
    try:
      i2 = l2.index(e1)
      return (e1, i1, i2)
    except ValueError:
      pass
    i1 += 1
  return (None, None, None)


class Function(object):
  all = {} # non recurisve list of all Functions
  def __init__(me, name):
    me.calls = {} # Functions which are called from 'me' Function 
    me.used  = {} # Functions which are calling 'me' Function
                  # This is also list of parrents
    me.name = name # Function name, duplicated from parents.calls dictionary
    Function.all[ name ] = me
  def add_new_call(me, name):
    """
    add new Function element as a child to this element
    """
    f = Function( name ) 
    me.calls[ name ] = f # tree structure
    f.used[ me.name ] = me # backreference
    return f
  def add_existing_call(me, she):
    """
    add existing function elment under another (this) parent function
    """
    me.calls[ she.name ] = she # tree structure
    she.used[ me.name ] = me # backreference
    return she
  def print_tree(me, layers = False, graph=False, depth=0, parents={}):
    indentation = "    " * depth
    head = ""
    tail = " "
    #if len(me.used) > 1:
    #  tail += str(len(me.used))
    if len(me.distances) == 1 and me.distances[0] == -1:
      pass
    else:
      try:
        tail += str(me.max_distance())
      except ValueError:
        print "ERR %s" % me.name
    if graph:
      tail += str(me.used.keys())
    if layers:
      try:
        tail += "             - %s -" % me.strong_layer
      except AttributeError:
        pass
    print head + indentation + me.name + tail
    if me.name in parents:
      print indentation + "... RECURSION (%s)" % me.name
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
    """
    find layer of functions which have just one and common parent
    """
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

  def distances_to_myself ( me, end_name ):
    """ 
    calculate distances to other calls of this function
    """
    me.distances = []
    if me.name in me.used.keys(): # shallow recurence
      me.distances.append( 1 )  # 1 is distance for shallow recurence

    if len(me.used) <= 1:
      me.distances.append( -1 )
    else:
      paths = me.find_all_paths( end_name )
      # every path with each other
      for i in xrange( len( paths ) ):
        for j in xrange( i+1, len( paths ) ):
          (_,d1,d2) = first_the_same_element_in_lists( paths[i][1:], paths[j][1:] )
          me.distances.append( d1 + d2 + 2 )

  def find_all_distances( me, end_name ):
    """
    calculate self distances for every function
    """
    for f in Function.all.values():
      f.distances_to_myself( end_name )

  def max_distance( me ):
    """
    max distance from self-distances
    """
    return max(me.distances)

  def find_all_paths(me,  end_name, path=[]):
    """
    all path from function up to end_name
    end_name usally will be "main"
    """
    path = path + [me.name]
    if me.name == end_name:
        return [path]
    paths = []
    for up_f in me.used.values():
        if up_f.name not in path:
            newpaths = up_f.find_all_paths(end_name, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths
  def get_all_functions_count( me ):
    return len(Function.all)




if __name__ == "__main__":

  fname = "main"

  if len(sys.argv) > 1:
    fname = sys.argv[1]

  pipes = Popen( [CSCOPE,'-l','-k','-R'],
                stdin=PIPE,
                stdout=PIPE,
                stderr=PIPE)  

  root = Function(fname)
  create_tree(root)
  root.find_strong_layers()
  root.find_all_distances( end_name = fname ) 
  
  root.print_tree(layers=True)
  print "====="
  root.print_strong_layers()
  print "Functions in source %d " % root.get_all_functions_count()
