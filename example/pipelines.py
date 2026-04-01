from spiders.baidu import BaiduSpider
from spiders.douban import DoubanSpider


class BaiduPipeline(object):

    def process_item(self, item, spider):
        """处理item"""
        if isinstance(spider, BaiduSpider):
            print("百度爬虫的数据：", item.data)
        return item


class DoubanPipeline(object):

    # 这里有所不同的是，需要增加一个参数，也就是传入爬虫对象
    # 以此来判断当前item是属于那个爬虫对象的
    def process_item(self, item, spider):
        """处理item"""
        if isinstance(spider, DoubanSpider):
            print("豆瓣爬虫的数据：", item.data)
        return item
