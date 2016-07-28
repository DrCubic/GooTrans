## GooTrans
____
####Func:
* Translate word using google-trans by crawler

####Py_files:
* run_main.py　　:  运行主函数
* goo_translate.py:  google 翻译的主程序
* crawl_thread.py :  爬取的线程Python程序
* log.py 　　　　 :  用于日志的文件
* translate.py　　:  单独运行的 金山iciba 翻译

####How to run:
* run goo-translate

	```
	python run_main.py -f {词表路径} -n {线程数量}   注：线程数量默认12
	```
* run iciba 

	```
	python translate.py -f {词表路径}
	```

####Environment 
* phantomjs
* python
* python-selenium
* Linux or Mac