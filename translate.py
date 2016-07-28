#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: translate.py
Author: mijianhong(mijianhong@baidu.com)
Date: 2016/07/26 21:40:01
"""
import requests
import json
import re
import os
import argparse
import logging

import log

def get_req(key_wd):
    """
    cat a request url

    Args:
        key_wd : word used to be translated

    Returns:
        req_url : request-url
    """
    req_url = 'http://dict-co.iciba.com/api/dictionary.php?w=%s&type=json&key=56B84924D396C2DD15227A428D5B0297' % key_wd
    return req_url

def judge(str):
    """
    判断字符串是否是英文还是中文

    Args:
        str : 待翻译的字符串

    Returns:
        1  : str is english
        -1 : str is chinese
    """
    str_ = str.__repr__()
    pa = re.compile(r'\\x|\\u')
    finds = re.search(pa, str_)
    if finds is None:
        return 1
    else:
        return -1

def trans_kw(kw):
    """
    download and print message
    """
    #kw = u'success'
    jdge = judge(kw)
    url = get_req(kw)
    try:
        req = requests.get(url)
        text = req.text
    except Exception as e:
        logging.error(' * {Download Error} : %s' % e)
        return 
    #print text
    if jdge == 1:
        ress = parse_dict_entoch(text)
        if ress is None or len(ress[0]) == 0:
            logging.error(' * {No any result}')
            return
        print u'Means:'
        print '----'
        for res in ress[0]:
            print res
    else:
        ress = parse_dict_chtoen(text)
        if ress is None or len(ress) == 0:
            logging.error(' * {No any result }')
            return 
        print u'词义如下:'
        print '----'
        for res in ress:
            print res['word_mean']

def parse_dict_chtoen(content):
    """
    """
    ddict = json.loads(content)
    for k, v in ddict.iteritems():
        if k == 'symbols':
            try:
                means = v[0]['parts'][0]['means']
                return means 
            except ValueError as e:
                print 'translate failed!'
                logging.error(' * {Translate Failed} : %s' % e)
                return None
    return None

def parse_dict_entoch(content):
    """
    parse the json-content

    Args:
        content : json-content used to be parsed

    Returns:
        (means, ci_xing) : means and cixing of the word used to be translated
        None : parse failed
    """
    ddict = json.loads(content)
    for k, v in ddict.iteritems():
        if k == 'symbols':
            try: 
                ci_xing = v[0]['parts'][0]['part']
                means = v[0]['parts'][0]['means']
                return (means, ci_xing)
            except KeyError as e:
                print 'translate failed!'
                logging.error(' * {Translate Failed} : %s' % e)
                return None
    return None        

def read_from_file(path):
    if not os.path.isfile(path):
        logging.error(' * {ReadFile is not existing !!!}')
        return None
    
    res_list = []
    with open(path, 'rb') as f:
        lines = f.readlines()
    for line in lines:
        if line.strip() == '':
            continue
        res_list.append(line.strip())
    return res_list 

def main():
    """
    main function to call trans_kw
    """
    log.init_log("./log/my_program")
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--readfile', action='store', dest='FILEPATH', default='.', help='set file path')
    args = parser.parse_args()
    file_path = args.FILEPATH
    trans_list = read_from_file(file_path)
    if trans_list is None:
        return 
    for trans in trans_list:
        print 'word:', trans
        trans_kw(trans)
        print '========================='

if __name__ == '__main__':
    """
    main function to run
    """
    main()
