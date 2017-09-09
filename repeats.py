#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2016, Jianfeng Chen <jchen37@ncsu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.


from __future__ import division
from os.path import isfile, join
import os
import pdb


def request_new_file(folder, model_name):
    if folder[-1] == '/':
        folder = folder[:-1]

    files = [f for f in os.listdir(folder) if isfile(join(folder, f))]
    existed = [f for f in files if '_'+model_name+'_' in f]
    if len(existed) == 0:
        return folder+'/_'+model_name+'_1.txt'
    else:
        i = [int(e.split('_')[2].split('.')[0]) for e in existed]
        i = max(i) + 1
        return folder+'/_'+model_name+'_' + str(i) + '.txt'


def fetch_all_files(folder, model_name):
    if folder[-1] == '/':
        folder = folder[:-1]

    files = [join(folder, f) for f in os.listdir(folder) if isfile(join(folder, f)) and '_'+model_name+'_' in f]
    return files


if __name__ == '__main__':
    print(request_new_file('./tse_rs/paper_material', 'osp'))
    print(fetch_all_files('./tse_rs/paper_material', 'osp'))
