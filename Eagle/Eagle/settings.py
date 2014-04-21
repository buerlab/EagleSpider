# Scrapy settings for Eagle project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'Eagle'
DOWNLOAD_TIMEOUT = 60

SPIDER_MODULES = ['Eagle.spiders']
NEWSPIDER_MODULE = 'Eagle.spiders'

ITEM_PIPELINES = {
	# 'Eagle.pipelines.UrlFullFillPipeline':100,
	# 'Eagle.pipelines.DuplicatedPipeline':200
	# 'Eagle.pipelines.FilterPipeline':200,
	# 'Eagle.pipelines.SaveItemPipeline':300
}

EXTENSIONS = {
    'Eagle.extensions.CrawlTimeRecord':100,
    'Eagle.extensions.ErrorCatcher':100
}


LOG_ENABLED = True
LOG_STDOUT = False
LOG_LEVEL = 'INFO'

USER_AGENT = "Mozilla/5.0 (Linux; X11)"
# DUPEFILTER_CLASS = ''

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Eagle (+http://www.yourdomain.com)'
