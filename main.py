import os
import sys
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute("scrapy crawl userinfo".split())
# execute("scrapy crawl douban".split())
# execute("scrapy crawl taobao".split())
