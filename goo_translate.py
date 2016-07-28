#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
########################################################################

"""
File: goo_translate.py
Author: mijianhong(mijianhong@baidu.com)
Date: 2016/07/27 19:10:44
"""
import logging
import Queue
import os

import termcolor
from selenium import webdriver

import crawl_thread

class GoogleTrans(object):
    """
    谷歌翻译的主调用类-主要作用是调用翻译线程

    Attributes:
        kw_queue : 存放待翻译词的队列
        file_path : 待翻译词的存放文本路径
        thread_count : 启动线程数，默认为12
    """
    def __init__(self, file_path, thread_cnt):
        self.kw_queue= Queue.Queue(0)
        self.file_path = file_path
        self.thread_count = thread_cnt

    def read_from_file(self):
        """
        读取待翻译词存放的文件，并放入kw_queue

        Returns:
            False / True : 读取失败返回False ，否则返回True
        """
        if not os.path.isfile(self.file_path):
            logging.error(' * not existing !!!}')
            return False
        with open(self.file_path, 'rb') as f:
            lines = f.readlines()
        for line in lines:
            if line.strip() == '':
                continue
            self.kw_queue.put(line.strip())
        return True

    def run_threads(self):
        """
        建立线程池，并启动所有线程
        """
        thread_list = []
        for index in xrange(self.thread_count):
            driver = webdriver.PhantomJS()
            driver.implicitly_wait(10)
            thread_name = 'thread - %d' % index
            thread = crawl_thread.TransThread(thread_name, self.process_request, self.process_response, driver)
            thread.setDaemon(True)
            thread_list.append(thread)
            print termcolor.colored(("第%s个线程开始工作") % index, 'yellow')
        for thread in thread_list:
            thread.start()
        self.kw_queue.join()
        # kill all phantomjs - processes
        os.system("kill -9 $(ps -ef|grep phantomjs |awk '$0 !~/grep/ {print $2}' |tr -s '\n' ' ')")
        print 'program ending...'

    def process_request(self):
        """
        线程每次的开始的回调函数
        """
        key_wd = self.kw_queue.get()
        return key_wd

    def process_response(self):
        """
        线程队列任务完成后的回调函数
        """
        self.kw_queue.task_done()
        pass
