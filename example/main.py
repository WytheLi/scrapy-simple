from scrapy_simple.core.engine import Engine

from spiders import BaiduSpider, DoubanSpider

if __name__ == '__main__':
    spider = BaiduSpider()  # 实例化爬虫对象
    engine = Engine(spider)  # 传入爬虫对象
    engine.start()  # 启动引擎

    douban_spider = DoubanSpider()
    douban_engine = Engine(douban_spider)
    douban_engine.start()