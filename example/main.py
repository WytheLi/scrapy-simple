from example.pipelines import BaiduPipeline, DoubanPipeline
from example.spiders.baidu import BaiduSpider
from example.spiders.douban import DoubanSpider
from scrapy_simple.core.engine import Engine


if __name__ == '__main__':
    baidu_spider = BaiduSpider()
    douban_spider = DoubanSpider()
    spiders = {BaiduSpider.name: baidu_spider, DoubanSpider.name: douban_spider}
    pipelines = [BaiduPipeline(), DoubanPipeline()]
    engine = Engine(spiders, pipelines=pipelines)
    engine.start()
