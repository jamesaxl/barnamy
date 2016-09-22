# barnamy
barnamy is an application for chat, and for control robots as device(BeagleBone, Raspberry Pi oder board that support python) on the network even over internet.

# Install

SERVER SIDE
===========
It is better to create a virtual env for python2 and use pip to install this requires modules

1.  bcrypt
2.  mongoengine (if you want mongodb)
3.  msgpack-python
4.  MySQL-python (if you want mariadb)
5.  psycopg2cffi (if you want postgresql with pypy)
6.  pymongo (if you want mongodb)
7.  pyOpenSSL
8.  schema
9.  service-identity
10. SQLAlchemy
11. structlog
12. Twisted

It contains two executed files barnamyd the server and barnamy_samrt, it will help you to manage your server.

CLIENT SIDE
===========

For Gnu/Linux operating system you should install these modules for pyhton version 2, do not install by hand if you do not know how your system works, It better to install them from your distribution package manager.

1.  bcrypt
2.  msgpack-python
3.  pyOpenSSL
5.  service-identity
6.  Twisted
7.  Gtk3
8.  python-gstreamer (version 1)

It contains two files barnamyc the client and bsft (Barnamy Settings First Time) it helps you to configure barnamy when you first time run it or for changing settings without connecting to the server.
