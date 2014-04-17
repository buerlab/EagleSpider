# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class EagleItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass


class TitleItem(Item):
	url = Field()
	title = Field()

#use the group to avoid frequently io when handle titleitem
class TitleGroup(Item):
	siteurl = Field()
	#titles: [{"title", "url"}]
	titles = Field()

