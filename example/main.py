from example.spiders.baidu import BaiduSpider
from example.spiders.douban import DoubanSpider
from scrapy_simple.core.engine import Engine


if __name__ == '__main__':
    baidu_spider = BaiduSpider()
    douban_spider = DoubanSpider()
    spiders = {BaiduSpider.name: baidu_spider, DoubanSpider.name: douban_spider}
    engine = Engine(spiders)
    engine.start()
