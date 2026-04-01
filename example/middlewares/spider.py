class TestSpiderMiddleware1(object):

    def process_request(self, request):
        print("TestSpiderMiddleware1: process_request")
        return request

    def process_item(self, item):
        print("TestSpiderMiddleware1: process_item")
        return item


class TestSpiderMiddleware2(object):

    def process_request(self, request):
        print("TestSpiderMiddleware2: process_request")
        return request

    def process_item(self, item):
        print("TestSpiderMiddleware2: process_item")
        return item
