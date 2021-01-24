from datetime import datetime, timedelta
import logging

from proxyport import get_random_proxy

from scrapy.exceptions import IgnoreRequest


logger = logging.getLogger(__name__)


class ProxyMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.max_retry_times = settings.get('RETRY_TIMES', 20)
        self.max_times_use = settings.get('MAX_TIMES_USE_PROXY', 50)
        self.bad_proxies = dict()
        self.cookie_map = dict()
        self.increase_proxy()

    def increase_proxy(self):
        if not self.cookie_map:
            i = 0
        else:
            i = self.get_last_cookiejar() + 1
        self.cookie_map[i] = dict(proxy=self.get_proxy(), times_used=0)
        return i

    def get_last_cookiejar(self):
        return sorted(self.cookie_map.keys())[-1]

    def process_request(self, request, spider):
        cookiejar = request.meta.get('cookiejar')
        if not cookiejar:
            cookiejar = self.get_last_cookiejar()
        proxy_obj = self.cookie_map[cookiejar]
        renew = request.meta.pop('renew_proxy', None)
        max_times_used_reached = proxy_obj['times_used'] > self.max_times_use
        if renew or max_times_used_reached:
            if max_times_used_reached:
                logger.debug('Proxy max times use reached, renew proxy.')
            cookiejar = self.increase_proxy()
            proxy_obj = self.cookie_map[cookiejar]
        request.meta.update(proxy=proxy_obj['proxy'], cookiejar=cookiejar)
        proxy_obj['times_used'] += 1
        logger.debug(
            'proxy="{}", cookie_id="{}", retry_times="{}", url="{}"'.format(
                proxy_obj['proxy'], cookiejar,
                request.meta.get('retry_times'), request.url))

    def process_response(self, request, response, spider):
        if response.status >= 400:
            logger.debug('response status="{}", proxy="{}"'.format(
                response.status, request.meta.get('proxy')))
            return self.renew_proxy(request)
        return response

    def process_exception(self, request, exception, spider):
        self.bad_proxies[request.meta.get('proxy')] = datetime.now()
        logger.debug('process_exception {}'.format(exception))
        return self.renew_proxy(request)

    def renew_proxy(self, request):
        retry_times = request.meta.get('retry_times', 0)
        if retry_times >= self.max_retry_times:
            logger.warning('to_many_retries url="{}", retries={}'.format(
                request.url, retry_times))
            raise IgnoreRequest()
        request.meta.update(renew_proxy=True, retry_times=retry_times + 1)
        return request

    def get_proxy(self):
        self.bad_proxies_gc()
        proxy = get_random_proxy()
        tries = 0
        while self.bad_proxies.get(proxy) and tries < 10:
            tries += 1
            proxy = get_random_proxy()
        return proxy

    def bad_proxies_gc(self):
        now = datetime.now()
        for address, added in list(self.bad_proxies.items()):
            if now - added > timedelta(minutes=5):
                del self.bad_proxies[address]
