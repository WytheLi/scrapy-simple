from six.moves.queue import Queue


class Scheduler(object):
    """
    1. 缓存请求对象(Request)，并为下载器提供请求对象，实现请求的调度
    2. 对请求对象进行去重判断
    """
    def __init__(self):
        self.queue = Queue()
        # 记录总共的请求数
        self.total_request_number = 0

    def add_request(self, request):
        """添加请求对象"""
        self.queue.put(request)
        self.total_request_number += 1    # 统计请求总数

    def get_request(self):
        """获取一个请求对象并返回"""
        try:
            request = self.queue.get(False)
        except:
            return None
        else:
            return request

    def _filter_request(self):
        """请求去重"""
        pass
