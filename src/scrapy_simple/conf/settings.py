from .default_settings import *

# 启用的爬虫类
SPIDER_CLASSES = [
    'spiders.baidu.BaiduSpider',
    'spiders.douban.DoubanSpider'
]

# 启用的管道类
PIPELINE_CLASSES = [
    'pipelines.BaiduPipeline',
    'pipelines.DoubanPipeline'
]

# 启用的爬虫中间件类
SPIDER_MIDDLEWARES = []

# 启用的下载器中间件类
DOWNLOADER_MIDDLEWARES = []
