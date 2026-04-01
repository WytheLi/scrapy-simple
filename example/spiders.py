from scrapy_simple.core.spider import Spider
from scrapy_simple.http.request import Request
from scrapy_simple.item import Item


class BaiduSpider(Spider):

    start_urls = ['http://www.baidu.com']    # 设置初始请求url


class DoubanSpider(Spider):

    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/124.0.0.0 Safari/537.36'
        ),
        'Referer': 'https://movie.douban.com/top250',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    def start_requests(self):
        """重写start_requests方法，返回多个请求"""
        base_url = 'https://movie.douban.com/top250?start='
        for i in range(0, 250, 25):    # 逐个返回第1-10页的请求对象
            url = base_url + str(i)
            yield Request(url, headers=self.headers)

    def parse(self, response):
        """解析豆瓣电影top250列表页"""
        movie_list = []
        for li in response.xpath("//ol[@class='grid_view']/li"):
            title_nodes = li.xpath(".//div[@class='hd']//span[@class='title'][1]/text()")
            rating_nodes = li.xpath(".//span[@class='rating_num']/text()")
            quote_nodes = li.xpath(".//p[@class='quote']/span/text()")
            link_nodes = li.xpath(".//div[@class='hd']/a/@href")
            info_nodes = li.xpath(".//div[@class='bd']/p[1]//text()")

            info = ' '.join(
                text.replace('\xa0', ' ').strip()
                for text in info_nodes
                if text.strip()
            )

            movie_list.append({
                'title': title_nodes[0].strip() if title_nodes else '',
                'rating': rating_nodes[0].strip() if rating_nodes else '',
                'quote': quote_nodes[0].strip() if quote_nodes else '',
                'url': link_nodes[0].strip() if link_nodes else '',
                'info': info,
            })

        yield Item(movie_list)
