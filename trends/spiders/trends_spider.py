import scrapy
import ujson
from trends.items import TrendsItem, TrendsRankingItem
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import log
import datetime

now = datetime.datetime.now()
today = now.strftime('%Y-%m-%d')

class TrendsSpider(scrapy.Spider):
    name = "trends"
    allowed_domains = ["baidu.com"]
    start_urls = ["http://top.baidu.com/population?fr=toppopulation"]
    api_url = "http://top.baidu.com/population/toplist"

    def parse(self, response):
        flag = True
        ages_info = []
        for ages in response.css("div[id='ageSel'] select[class='select-style']"):
            if flag:
                flag = False
                for age in ages.xpath('option'):
                    ages_info.append({'id': age.xpath('@value')[0].extract(),
                                      'name': age.xpath('text()')[0].extract()})
            else:
                break

        for base_info in response.css("div[id='ageSel'] li[realid]"):
            item = TrendsItem()
            item['category'] = realid = base_info.xpath('@realid').extract()[0]
            item['name'] = base_info.xpath('text()').extract()[0]

            total = 7
            step = 3
            template = '&divids[]={}'
            for index in range(0, 2):
                if total > step:
                    extended = template * step
                    extended = extended.format(ages_info[index*step]['id'],
                                               ages_info[index*step+1]['id'],
                                               ages_info[index*step+2]['id'])
                else:
                    extended = template.format(ages_info[index*step]['id'])
                total -= step

                yield Request(
                    self.api_url,
                    method='POST',
                    body='boardid={}'.format(realid) + extended,
                    callback=self.parse_data,
                    errback=self.parse_error,
                )

            yield item

    def parse_data(self, response):
        selector = Selector(response)
        data = selector.xpath('//p/text()').extract()[0]
        data = ujson.loads(data)

        for row in data['topWords']:
            rank = 1
            for detail in data['topWords'][row]:
                item = TrendsRankingItem()
                item['category'] = data['boardid']
                item['date'] = today
                item['ageRange'] = row
                item['rank'] = rank
                item['keyword'] = detail['keyword']
                item['searches'] = detail['searches']
                item['changeRate'] = detail['changeRate']
                item['isNew'] = detail['isNew']
                item['trend'] = detail['trend']
                item['percentage'] = detail['percentage']
                rank += 1
                yield item

    def parse_error(self, response):
        log.msg('Crawl failed: {}'.format(response.url), log.WARNING)