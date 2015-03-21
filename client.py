#!/usr/bin/env python
# encoding: utf-8


import xmlrpclib

proxy = xmlrpclib.ServerProxy('http://localhost:9000', allow_none=True)
print proxy.get_count()
