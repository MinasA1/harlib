#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# harlib
# Copyright (c) 2014-2017, Andrew Robbins, All rights reserved.
#
# This library ("it") is free software; it is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; you can redistribute it and/or
# modify it under the terms of LGPLv3 <https://www.gnu.org/licenses/lgpl.html>.
'''
harlib - HTTP Archive (HAR) format library
'''
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import json
from harlib.compat import OrderedDict


def by_name(har):
    return har['name']


def sorted_har_request_body(har):
    if 'params' in har:
        har['params'] = sorted(har['params'], key=by_name)
    return har


def sorted_har_request(har):
    har['headers'] = sorted(har['headers'], key=by_name)
    if 'cookies' in har:
        har['cookies'] = sorted(har['cookies'], key=by_name)
    if 'queryString' in har:
        har['queryString'] = sorted(har['queryString'], key=by_name)
    if 'postData' in har:
        har['postData'] = sorted_har_request_body(har['postData'])
    return har


def sorted_har_response(har):
    har['headers'] = sorted(har['headers'], key=by_name)
    if 'cookies' in har:
        har['cookies'] = sorted(har['cookies'], key=by_name)
    return har


def sorted_har_entry(har):
    har['request'] = sorted_har_request(har['request'])
    har['response'] = sorted_har_response(har['response'])
    return har


def sorted_har(har):
    for i, entry in enumerate(har['log']['entries']):
        har['log']['entries'][i] = sorted_har_entry(entry)
    return har


def har_sort(reader, writer):
    d = json.load(reader, object_pairs_hook=OrderedDict)
    d = sorted_har(d)
    print(json.dumps(d, indent=2, default=str,
                     separators=(',', ': ')), file=writer)


def har_sort_main():
    import sys
    filename = sys.argv[1]
    with open(filename, 'r') as reader:
        har_sort(reader, sys.stdout)


main = har_sort_main
if __name__ == '__main__':
    main()
