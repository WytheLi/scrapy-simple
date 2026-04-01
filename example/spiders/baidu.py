from scrapy_simple.core.spider import Spider


class BaiduSpider(Spider):
    name = 'baidu'
    start_urls = ['http://www.baidu.com']    # 设置初始请求url
