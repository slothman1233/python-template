from scrapy_redis.dupefilter import RFPDupeFilter



 
class SeleniumDupeFilter(RFPDupeFilter):
    
    def request_seen(self, request):
        """
        取消去重
        """
        return False