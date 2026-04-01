from example.middlewares.downloader import TestDownloaderMiddleware1, TestDownloaderMiddleware2
from example.middlewares.spider import TestSpiderMiddleware2, TestSpiderMiddleware1
from example.pipelines import BaiduPipeline, DoubanPipeline
from example.spiders.baidu import BaiduSpider
from example.spiders.douban import DoubanSpider
from scrapy_simple.core.engine import Engine


if __name__ == '__main__':
    baidu_spider = BaiduSpider()
    douban_spider = DoubanSpider()
    spiders = {BaiduSpider.name: baidu_spider, DoubanSpider.name: douban_spider}
    pipelines = [BaiduPipeline(), DoubanPipeline()]
    spider_mids = [TestSpiderMiddleware1(), TestSpiderMiddleware2()]
    downloader_mids = [TestDownloaderMiddleware1(), TestDownloaderMiddleware2()]

    engine = Engine(spiders, pipelines=pipelines, spider_mids=spider_mids, downloader_mids=downloader_mids)
    engine.start()
