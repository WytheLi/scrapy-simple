class TestDownloaderMiddleware1(object):

    def process_request(self, request):
        """处理请求头，添加默认的user-agent"""
        print("TestDownloaderMiddleware1: process_request")
        return request

    def process_response(self, item):
        """处理数据对象"""
        print("TestDownloaderMiddleware1: process_response")
        return item


class TestDownloaderMiddleware2(object):

    def process_request(self, request):
        """处理请求头，添加默认的user-agent"""
        print("TestDownloaderMiddleware2: process_request")
        return request

    def process_response(self, item):
        """处理数据对象"""
        print("TestDownloaderMiddleware2: process_response")
        return item
