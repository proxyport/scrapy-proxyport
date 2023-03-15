[Proxy Port](https://github.com/proxyport/py-proxyport) integration for Scrapy.
## Prerequisites
To use this package you will need a free API key. Get your API key <a href="https://account.proxy-port.com/scraping" target="_blank">here</a>.
Detailed instructions <a href="https://proxy-port.com/en/scraping-proxy/getting-started" target="_blank">here</a>.

## Installation

```shell
$ pip install scrapyproxyport
```
## Getting Started
You need to assign an API key.
This can be done either through an environment variable
```shell
$ export PROXY_PORT_API_KEY=<API_KEY>
```
or inside settings.py.
```python
# inside <your_project>/settings.py

PROXY_PORT_API_KEY = '<API_KEY>'
DOWNLOADER_MIDDLEWARES = {
    # Add middleware with order number right before CookiesMiddleware
    'scrapyproxyport.middlewares.ProxyMiddleware': 898,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 899,
}
DOWNLOAD_TIMEOUT = 10
RETRY_TIMES = 20
DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'
```
