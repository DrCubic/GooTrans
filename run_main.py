#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: run_main.py
Author: mijianhong(mijianhong@baidu.com)
Date: 2016/07/27 20:16:15
"""
import logging
import argparse

import log
import goo_translate

if __name__ == '__main__':
    """
    主程序入口
    """
    log.init_log('./log/mini_spider')   
    logging.info('%-35s' % ' * Google-translate is starting ... ')
    parser = argparse.ArgumentParser(description = 'This is a google-translation programm!')
    parser.add_argument('-v', 
                        '--version',
                        action='version', 
                        version='%(prog)s 1.0.0')

    parser.add_argument('-f',
                        '--kw_file',
                        action='store',
                        dest='FILE_PATH',
                        default='word.dict',
                        help='please set file_path ... ')
    parser.add_argument('-n',
                        '--thread_num',
                        action='store',
                        dest='THREAD_NUM',
                        default=12,
                        help='please set thread_num ...')

    args = parser.parse_args()
    goo_t = goo_translate.GoogleTrans(args.FILE_PATH, int(args.THREAD_NUM))
    if goo_t.read_from_file():
        goo_t.run_threads()
    
    logging.info('%-35s' % ' * Google-translate is ended ... ')
