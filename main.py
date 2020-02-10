from scrapy.cmdline import execute

execute(["scrapy", "crawl", "mzitu", "-s", "LOG_FILE=all.log"])
