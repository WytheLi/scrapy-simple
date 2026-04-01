import time
from datetime import datetime

from scrapy_simple.middlewares.downloader_middleware import DownloaderMiddleware
from scrapy_simple.middlewares.spider_middleware import SpiderMiddleware
from scrapy_simple.http.request import Request
from scrapy_simple.utils.logger import logger, configure_logging

from .scheduler import Scheduler
from .downloader import Downloader
from .pipeline import Pipeline


class Engine(object):
    """
    a. 对外提供整个的程序的入口
    b. 依次调用其他组件对外提供的接口，实现整个框架的运作(驱动)
    """

    def __init__(self, spider):
        self.spider = spider    # 接收爬虫对象
        self.scheduler = Scheduler()    # 初始化调度器对象
        self.downloader = Downloader()    # 初始化下载器对象
        self.pipeline = Pipeline()    # 初始化管道对象
        self.spider_mid = SpiderMiddleware()    # 初始化爬虫中间件对象
        self.downloader_mid = DownloaderMiddleware()    # 初始化下载器中间件对象
        configure_logging()
        self.total_request_nums = 0
        self.total_response_nums = 0


    def start(self):
        """启动整个引擎"""
        start_time = datetime.now()
        self._start_engine()
        end_time = datetime.now()
        logger.info("爬虫耗时：%.2f" % (end_time - start_time).total_seconds())
        logger.info("总的请求数量:{}".format(self.total_request_nums))
        logger.info("总的响应数量:{}".format(self.total_response_nums))


    def _start_request(self):
        for start_request in self.spider.start_requests():
            #1. 对start_request进过爬虫中间件进行处理
            start_request = self.spider_mid.process_request(start_request)

            #2. 调用调度器的add_request方法，添加request对象到调度器中
            self.scheduler.add_request(start_request)
            #请求数+1
            self.total_request_nums += 1

    def _execute_request_response_item(self):
        #3. 调用调度器的get_request方法，获取request对象
        request = self.scheduler.get_request()
        if request is None: #如果没有获取到请求对象，直接返回
            return

        #request对象经过下载器中间件的process_request进行处理
        request = self.downloader_mid.process_request(request)

        #4. 调用下载器的get_response方法，获取响应
        response = self.downloader.get_response(request)
        #response对象经过下载器中间件的process_response进行处理
        response = self.downloader_mid.process_response(response)
        #response对象经过下爬虫中间件的process_response进行处理
        response = self.spider_mid.process_response(response)

        #5. 调用爬虫的parse方法，处理响应
        for result in self.spider.parse(response):
            #6.判断结果的类型，如果是request，重新调用调度器的add_request方法
            if isinstance(result,Request):
                #在解析函数得到request对象之后，使用process_request进行处理
                result = self.spider_mid.process_request(result)
                self.scheduler.add_request(result)
                self.total_request_nums += 1
            #7如果不是，调用pipeline的process_item方法处理结果
            else:
                self.pipeline.process_item(result)

        self.total_response_nums += 1

    def _start_engine(self):
        """
        具体的实现引擎的细节
        :return:
        """
        self._start_request()
        while True:
            time.sleep(0.001)
            self._execute_request_response_item()
            if self.total_response_nums>= self.total_request_nums:
                break
