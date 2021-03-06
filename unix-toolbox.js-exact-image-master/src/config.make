prefix = /usr/local
exec_prefix = $(prefix)
PACKAGE = exact-image
VERSION = 0.8.8
VERSION_MAJOR = 0
VERSION_MINOR = 8
VERSION_MICRO = 8
DATE = Mo, 01 Apr 2013
bindir = $(exec_prefix)/bin
sbindir = $(exec_prefix)/sbin
libexecdir = $(exec_prefix)/lib
datadir = $(prefix)/share
sysconfdir = $(prefix)/etc
sharedstatedir = $(prefix)/com
localstatedirdir = $(prefix)/var
libdir = $(exec_prefix)/lib
includedir = $(prefix)/include
infodir = $(prefix)/info
mandir = $(prefix)/man
WITHEVAS = 0
WITHLIBJPEG = 1
WITHLIBTIFF = 1
WITHLIBPNG = 0
WITHBARDECODE = 0
EVASGL = 0
TGA = 1
PCX = 1
STATIC =
X11INCS = -I/usr/X11/include
X11LIBS = -L/usr/X11/lib64 -L/usr/X11/lib -L/usr/X11R6/lib -lX11
LIBJPEGINCS =
LIBJPEGLIBS =
LIBTIFFINCS =
LIBTIFFLIBS =
JASPERINCS =
JASPERLIBS =
EXPATINCS =
EXPATLIBS = -lexpat
SWIGINCS =
SWIGLIBS =
PERLINCS = -D_REENTRANT -D_GNU_SOURCE -DDEBIAN -fstack-protector -fno-strict-aliasing -pipe -I/usr/local/include -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -I/usr/lib/perl/5.14/CORE
PERLLIBS =
PYTHONINCS = -I/usr/include/python2.7 -I/usr/include/python2.7
PYTHONLIBS =
RUBYINCS = -I/usr/lib64/ruby/1.8/x86_64-linux
RUBYLIBS =
