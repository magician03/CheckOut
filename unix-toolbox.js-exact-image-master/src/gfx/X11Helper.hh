/*
 * --- GSMP-COPYRIGHT-NOTE-BEGIN ---
 * 
 * This copyright note is auto-generated by ./scripts/Create-CopyPatch.
 * Please add additional copyright information _after_ the line containing
 * the GSMP-COPYRIGHT-NOTE-END tag. Otherwise it might get removed by
 * the ./scripts/Create-CopyPatch script. Do not edit this copyright text!
 * 
 * GSMP: gfx/include/X11Helper.hh
 * General Sound Manipulation Program is Copyright (C) 2000 - 2004
 *   Valentin Ziegler and Ren� Rebe
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; version 2. A copy of the GNU General
 * Public License can be found in the file LICENSE.
 * 
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANT-
 * ABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
 * Public License for more details.
 * 
 * --- GSMP-COPYRIGHT-NOTE-END ---
 */

#ifndef __X11HELPER__
#define __X11HELPER__

#include <X11/Xlib.h>
#include <X11/Xutil.h>

#include "Evas.h"
#include "Evas_Engine_Software_X11.h"

// int types
#include <inttypes.h>

template <class T>
int first_bit_set (T v)
{
  unsigned int i;
  for (i = 0; i < sizeof (T) * 8; ++i) {
    if (v & (1L << i))
      break;
  }
  return i;
}

template <class T>
int bits_set (T v)
{
  unsigned int i, c = 0;
  
  for (i = 0; i < sizeof(T) * 8; ++i) {
    if (v & (1L << i))
      ++c;
  }
  return c;
}

Visual* find_argb_visual (Display* dpy, int scr);

// Based uppon xscreensavers grab-ximage.c
class X11Window
{
 public:
  
  static int Width (Display* dpy, Window window);
  static int Height (Display* dpy, Window window);

  static bool Move (Display* dpy, Window window, int x, int y);
  static bool Resize (Display* dpy, Window window, int w, int h);
  
  static int Depth (Display* dpy, Window window);
  static Visual* ColorVisual (Display* dpy, Window window);

  static Evas_Object* CaptureIntoEvasImage (Evas* evas,
					    Display* dpy,
					    Window window,
					    int x, int y, int w, int h);

  static void CaptureIntoEvasImage (Evas_Object* ob,
				    Display* dpy,
				    Window window,
				    int x, int y, int w, int h);
  
  static void StayOnTop (Display* dpy, Window win);
  
private:

  static int screen_number (Screen* screen);
  
  static int visual_class (Screen* screen, Visual* visual);
  static int visual_cells (Screen* screen, Visual* visual);
  
  // on top stuff
  static bool gnome_stay_on_top (Display* dpy, Window root, Window win);
  static bool netwm_stay_on_top(Display* dpy, Window root, Window win);
};

#endif // __X11HELPER__
