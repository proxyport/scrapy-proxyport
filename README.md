[Proxy Port](https://github.com/proxyport/py-proxyport) integration with Scrapy framework.

## Installation

```shell
$ pip install scrapyproxyport
```
## Getting Started

```python
# inside <your_project>/settings.py

DOWNLOADER_MIDDLEWARES = {
    # Add middleware with order number right before CookiesMiddleware
    'scrapyproxyport.middlewares.ProxyMiddleware': 898,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 899,
}
DOWNLOAD_TIMEOUT = 10
RETRY_TIMES = 20
DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'
```
