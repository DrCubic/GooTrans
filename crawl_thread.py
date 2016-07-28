#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
########################################################################

"""
File: crawl_thread.py
Author: mijianhong(mijianhong@baidu.com)
Date: 2016/07/27 19:53:05
"""
import threading
import logging
import re
import traceback
import time
import urllib

from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

class TransThread(threading.Thread):
    """
    thread for translating

    Attributes:
        process_request : 线程请求翻译词回调函数
        process_response : 线程任务完成后的回调函数
    """
    def __init__(self, name, process_request, process_response, driver):
        super(TransThread, self).__init__(name=name)
        self.process_request = process_request
        self.process_response = process_response
        self.driver = driver
        self.base_url = 'http://translate.google.cn/#%s/%s/%s'

    def run(self):
        """
        每个线程具体完成的任务
        """
        while 1:
            kw_word = self.process_request()
            #print kw_word
            #print chardet.detect(kw_word)
            if self.judge_en_ch(kw_word):
                url = self.base_url % ('en', 'zh-CN', kw_word)
            else:
                kw_word_ = urllib.quote(kw_word)
                url = self.base_url % ('zh-CN', 'en', kw_word_)
            try:
                self.driver.get(url)
            except Exception as e:
                logging.error(' {Driver.get Eroor} : %s' % e)
                return
            time.sleep(2)

            try:
                element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "result_box")))
            except Exception as e:
                logging.warn(' {WebDriverWait Error}: %s' % e)
                return

            content = self.driver.page_source
            res =  self.parse_html(content).encode('utf-8')
            if res is None:
                return
            print kw_word + ': ' + res
            self.process_response()

    def judge_en_ch(self, kw):
        """
        判断待翻译词是中文 还是 英文

        Args:
            kw : 待翻译的词汇

        Returns:
            False / True : 若为中文则返回False,否则返回True
        """
        kw_ = kw.__repr__()
        pa = re.compile(r'\\x|\\u')
        finds = re.search(pa, kw_)
        if finds is None:
            return True
        return False

    def parse_html(self, content):
        """
        解析翻译页面，得到翻译结果并返回

        Args:
            content : 翻译页面内容

        Returns:
            res : 解析除的翻译词
            None : 当解析失败的时候返回
        """
        try:
            soup = BeautifulSoup(content, 'html5lib')
            res = soup.find_all('span', id='result_box')[0].get_text().strip()
        except Exception as e:
            logging.warn(' {Parse Error } : %s' % e)
            return None
        return res
