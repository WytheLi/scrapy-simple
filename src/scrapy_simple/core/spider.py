from scrapy_simple.item import Item
from scrapy_simple.http.request import Request


class Spider(object):
    """
    1. 构建请求信息(初始的)，也就是生成请求对象(Request)
    2. 解析响应对象，返回数据对象(Item)或者新的请求对象(Request)
    """

    start_urls = []    # 默认初始请求地址

    # def start_requests(self):
    #     '''构建初始请求对象并返回'''
    #     request_list = []
    #     for url in self.start_urls:
    #         request_list.append(Request(url))
    #     return request_list

    # 利用生成器方式实现，提高程序的资源消耗
    def start_requests(self):
        """构建初始请求对象并返回"""
        for url in self.start_urls:
            yield Request(url)

    def parse(self, response):
        """
        解析请求
        并返回新的请求对象、或者数据对象
        返回值应当是一个容器，如start_requests返回值方法一样，改为生成器即可
        :param response:
        :return:
        """
        yield Item(response.body)   # 返回item对象 改为生成器即可
