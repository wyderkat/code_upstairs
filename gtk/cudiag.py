#!/usr/bin/python
from gi.repository import Gtk
import cairo
from math import sin,cos,pi
import code_upstairs_core as cu


class CUDiag(Gtk.ScrolledWindow):

  def __init__(me, root):
    Gtk.ScrolledWindow.__init__(me)
    me.da = Gtk.DrawingArea()
    me.vp = Gtk.Viewport()
    me.vp.add( me.da )
    me.add( me.vp )
    me.root = root
         
    me.da.set_size_request (2000, 2000)
    me.set_size_request( 700, 700 )

    me.da.connect('draw', me.draw_callback)

  def draw_callback(me, w, cr):
    width = w.get_allocation().width
    height = w.get_allocation().height
    cr.scale( width, height) 
    cr.set_line_width(max(cr.device_to_user_distance(2,2)))
    cr.set_font_size(max(cr.device_to_user_distance(15,15)))
    cr.select_font_face("tahoma")
  
    cr.set_source_rgb(0.0, 0.0, 0.0)
    me.draw_tree ( cr, me.root )
    return False
         
  def draw_tree( me , cr, fun, 
                deg=0.0, dlen=2.0*pi, 
                xcen=0.5, ycen=0.5, arm=0.0, 
                xpre=0.5, ypre=0.5,
                scale=0.0 ):
    elipsis_ratio = 2.5
    e = cr.text_extents( fun.name ) 
    x = xcen + elipsis_ratio*sin(deg + dlen/2)*arm
    y = ycen - cos(deg + dlen/2)*arm
    cr.move_to( xpre, ypre )
    cr.line_to( x, y ) 
    cr.stroke()
    cr.move_to(x - e[2]/2 - e[0], 
               y - e[3]/2 - e[1]) 
    cr.text_path( fun.name )
    cr.fill()
    if scale == 0.0: #not set, first function
      scale = e[3]*1.8 # TODO tmp solution
    r = ( e[2]+e[3]*0.8, scale )
    me.round_rectangle( cr, x - r[0]/2, y - r[1]/2, r[0], r[1], 1.0, r[1]/3)
    print  x - r[0]/2, y - r[1]/2, r[0], r[1], 1.0, r[1]/3
    #
    childs = fun.what_strong_layer_childs_fun()
    if childs:
      n_childs = len(childs)
      sub_dlen = dlen / n_childs
      # wzor na ramie
      # dlen*new_arm (OBWOD) = n_childs*min_size
      min_size = 2*scale
      new_arm = (n_childs * min_size) / dlen
      if n_childs == 1:
        new_arm = arm + min_size

      i_deg = deg
      for c in childs:
        print "%s - new_arm=%g for hight=%g and childsno=%d" %\
        (c.name, new_arm, r[1], n_childs)
        x1 = x+elipsis_ratio*sin(i_deg + sub_dlen/2)*arm
        y1 = y-cos(i_deg + sub_dlen/2)*arm
        #print "%s at x1=%g, y1=%g, deg=%g " % (c.name, x1, y1, i_deg)
        me.draw_tree( cr, c, i_deg, sub_dlen, xcen, ycen, new_arm, x, y, scale )
        i_deg += sub_dlen

  def draw_tree_OLD( me , cr, fun, deg, dlen, x, y, scale=0.0 ):
    elipsis_ratio = 2.5
    e = cr.text_extents( fun.name ) 
    cr.move_to(x - e[2]/2 - e[0], y - e[3]/2 - e[1])
    cr.text_path( fun.name )
    cr.fill()
    if scale == 0.0: #not set, first function
      scale = e[3]*1.8 # TODO tmp solution
    r = ( e[2]+e[3]*0.8, scale )
    me.round_rectangle( cr, x - r[0]/2, y - r[1]/2, r[0], r[1], 1.0, r[1]/3)
    childs = fun.what_strong_layer_childs_fun()
    if childs:
      sub_dlen = dlen / len(childs)
      arm = (8*scale  )/ dlen #+ 0.4*scale * len(childs) ) / \
         # ( dlen) # how much of rounde space we have
      i_deg = deg
      for c in childs:
        print "%s - arm=%g for hight=%g and childsno=%d" %\
        (c.name, arm, r[1], len(childs))
        x1 = x+elipsis_ratio*sin(i_deg + sub_dlen/2)*arm
        y1 = y-cos(i_deg + sub_dlen/2)*arm
        #print "%s at x1=%g, y1=%g, deg=%g " % (c.name, x1, y1, i_deg)
        me.draw_tree( cr, c, i_deg, sub_dlen, x1, y1, scale )
        i_deg += sub_dlen

  def round_rectangle( me, cr, x, y, w, h, aspect, corner_radius ):
    radius = corner_radius / aspect;
    degrees = pi / 180.0;

    cr.new_sub_path ();
    cr.arc ( x + w - radius, y + radius, radius, -90 * degrees, 0 * degrees);
    cr.arc ( x + w - radius, y + h - radius, radius, 0 * degrees, 90 * degrees);
    cr.arc ( x + radius, y + h - radius, radius, 90 * degrees, 180 * degrees);
    cr.arc ( x + radius, y + radius, radius, 180 * degrees, 270 * degrees);
    cr.close_path ();

    #cr.set_source_rgb (0.5, 0.5, 1);
    #cr.fill_preserve ();
    cr.set_source_rgba (0.5, 0, 0, 0.5);
    #cairo_set_line_width (cr, 10.0);
    cr.stroke ();

       

if __name__ == "__main__":
  import sys
  fname = "main"

  if len(sys.argv) > 1:
    fname = sys.argv[1]

  conn = cu.init_connection()

  root = cu.Create_tree(conn, fname)
  loc = cu.Location( root )
  root.find_strong_layers()
  root.find_all_distances( end_name = fname ) 
  
  #root.print_tree(layers=True)
  #print "====="
  #root.print_strong_layers()
  #print "Functions in source %d " % root.get_all_functions_count()
  #print "Strong layer for init: %s" % \
  #    str( root.who("init").what_strong_layer_childs() )
  #print "Strong layer siblings for init: %s" % \
  #    str( root.who("init").what_strong_layer_siblings() )
  #print loc.what( "linenoise.c", 200 )
  window = Gtk.Window()
  window.set_title ("Code Upstairs Diag")
  cudiag = CUDiag( root )
  window.add(cudiag)
       
  window.connect_after('destroy', Gtk.main_quit)
  window.show_all()
  hadj = cudiag.get_hadjustment()
  # TODO make it in onshow(...) signal
  hadj.set_value( (hadj.get_upper() 
                   - hadj.get_page_size() 
                   - hadj.get_lower() ) /2 )
  vadj = cudiag.get_vadjustment()
  vadj.set_value( (vadj.get_upper() 
                   - vadj.get_page_size() 
                   - vadj.get_lower() ) /2 )
  Gtk.main()
       
