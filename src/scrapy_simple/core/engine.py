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

    def __init__(self, spiders):
        self.spiders = spiders
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
        # 1. 爬虫模块发出初始请求
        for spider_name, spider in self.spiders.items():
            for start_request in spider.start_requests():
                # 2. 把初始请求添加给调度器
                # 利用爬虫中间件预处理请求对象
                start_request = self.spider_mid.process_request(start_request)
                start_request.spider_name = spider_name    #为请求对象绑定它所属的爬虫的名称
                self.scheduler.add_request(start_request)
                #请求数+1
                self.total_request_nums += 1

    def _execute_request_response_item(self):
        #3. 调用调度器的get_request方法，获取request对象
        request = self.scheduler.get_request()
        if request is None: #如果没有获取到请求对象，直接返回
            return

            # request对象经过下载器中间件的process_request进行处理
        request = self.downloader_mid.process_request(request)

        # 4. 调用下载器的get_response方法，获取响应
        response = self.downloader.get_response(request)

        response.meta = request.meta

        # response对象经过下载器中间件的process_response进行处理
        response = self.downloader_mid.process_response(response)
        # response对象经过下爬虫中间件的process_response进行处理
        response = self.spider_mid.process_response(response)

        spider = self.spiders[request.spider_name]

        # 5. 利用爬虫的解析响应的方法，处理响应，得到结果
        parse = getattr(spider, request.parse)    # 获取对应的解析函数
        results = parse(response)    # parse函数的返回值是一个容器，如列表或者生成器对象
        for result in results:
            # 6. 判断结果对象
            # 6.1 如果是请求对象，那么就再交给调度器
            if isinstance(result, Request):
               # 利用爬虫中间件预处理请求对象
               result = self.spider_mid.process_request(result)
               result.spider_name = request.spider_name  # 为请求对象绑定它所属的爬虫的名称
               self.scheduler.add_request(result)
               self.total_request_nums += 1
            # 7如果不是，调用pipeline的process_item方法处理结果
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
