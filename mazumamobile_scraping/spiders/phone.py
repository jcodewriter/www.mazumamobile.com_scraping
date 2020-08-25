import scrapy
from mazumamobile_scraping.items import MazumamobileScrapingItem


class PhoneSpider(scrapy.Spider):
    name = 'phone'
    allowed_domains = ['mazumamobile.com']
    domain_name = 'https://www.mazumamobile.com'
    start_urls = [
        'https://www.mazumamobile.com/sell-my-mobile/apple/phones',
        # 'https://www.mazumamobile.com/sell-my-mobile/samsung/phones',
        # 'https://www.mazumamobile.com/sell-my-mobile/huawei/phones',
        # 'https://www.mazumamobile.com/sell-my-mobile/google/phones',
        # 'https://www.mazumamobile.com/sell-my-mobile/motorola/phones',
        # 'https://www.mazumamobile.com/sell-my-mobile/sony/phones',
        # 'https://www.mazumamobile.com/sell-my-mobile/oneplus/phones',
        # 'https://www.mazumamobile.com/sell-my-mobile/htc/phones',
        # 'https://www.mazumamobile.com/sell-my-mobile/blackberry/phones',
        # 'https://www.mazumamobile.com/sell-my-mobile/lg/phones',
        # 'https://www.mazumamobile.com/sell-my-mobile/nokia/phones',
        # 'https://www.mazumamobile.com/sell-my-mobile/honor/phones',
        # 'https://www.mazumamobile.com/sell-my-mobile/apple/tablets',
        # 'https://www.mazumamobile.com/sell-my-mobile/samsung/tablets',
        # 'https://www.mazumamobile.com/sell-my-mobile/apple/watches',
        # 'https://www.mazumamobile.com/sell-my-mobile/samsung/watches',
        # 'https://www.mazumamobile.com/sell-my-mobile/huawei/watches',
        # 'https://www.mazumamobile.com/sell-my-mac/sell-macbook-pro',
        # 'https://www.mazumamobile.com/sell-my-mac/sell-macbook-air',
        # 'https://www.mazumamobile.com/sell-my-mac/sell-macbook',
        # 'https://www.mazumamobile.com/sell-my-mac/sell-mac-pro',
        # 'https://www.mazumamobile.com/sell-my-mac/sell-mac-mini',
        # 'https://www.mazumamobile.com/sell-my-mac/sell-imac',
    ]
    # start_urls = ['https://m.mazumamobile.com/pro-sitemaps-4138557.php']

    def parse(self, response):
        items = response.xpath('//div[@class="model"]')
        for item in items:
            url = item.xpath('//div[@class="tdmain"]/a/@href').extract_first()
            if (url.find('iphone') == -1) and (url.find('ipad') == -1) and (url.find('playstation') == -1) and (url.find('inch') == -1):
                print("url---------------------------->", url)
        yield scrapy.Request(relative_url, callback=self.parse_page)
        items = response.xpath(
            '//div[@class="one-third " or @class="one-third last"]')
        

    def parse_page(self, response):
        scrapyItem = MazumamobileScrapingItem()

        scrapyItem['phoneID'] = response.xpath(
            '//input[@name="phoneID"]/@value').extract_first()
        scrapyItem['phoneType'] = response.xpath(
            '//input[@name="phoneType"]/@value').extract_first()
        title = response.xpath(
            '//div[@class="page-title"]/h1/span[@class="brand"]/text()').extract_first()
        items = response.xpath('//ul[@class="networks"]/li')
        if items == []:
            aaa = response.xpath('//div[@id="guaranteed-value"]')
            scrapyItem['phoneModel'] = response.xpath(
                '//div[@class="page-title"]/h1/span[@class="model"]/text()').extract_first()
            scrapyItem['phoneName'] = title+" "+scrapyItem['phoneModel']
            scrapyItem['excellentPrice'] = response.xpath(
                '//div[@id="guaranteed-value"]/@data-excellent').extract_first()
            scrapyItem['goodPrice'] = response.xpath(
                '//div[@id="guaranteed-value"]/@data-good').extract_first()
            scrapyItem['poorPrice'] = response.xpath(
                '//div[@id="guaranteed-value"]/@data-poor').extract_first()
            scrapyItem['faultyPrice'] = response.xpath(
                '//div[@id="guaranteed-value"]/@data-faulty').extract_first()
            scrapyItem['deadPrice'] = response.xpath(
                '//div[@id="guaranteed-value"]/@data-dead').extract_first()
            scrapyItem['image_name'] = scrapyItem['phoneName']
        else:
            for item in items:
                scrapyItem['phoneModel'] = item.xpath(
                    'a/@data-fon-model').extract_first()
                scrapyItem['phoneName'] = title+" "+scrapyItem['phoneModel']
                # scrapyItem['dataOptionName'] = item.xpath(
                #     'a/@data-option-name').extract_first()
                scrapyItem['excellentPrice'] = item.xpath(
                    'a/@data-excellent').extract_first()
                scrapyItem['goodPrice'] = item.xpath(
                    'a/@data-good').extract_first()
                scrapyItem['poorPrice'] = item.xpath(
                    'a/@data-poor').extract_first()
                scrapyItem['faultyPrice'] = item.xpath(
                    'a/@data-faulty').extract_first()
                scrapyItem['deadPrice'] = item.xpath(
                    'a/@data-dead').extract_first()
                scrapyItem['image_name'] = scrapyItem['phoneName']

        # scrapyItem['image_name'] =
        imagePath = response.xpath(
            '//div[@class="phone-details"]/img/@src').extract_first()
        scrapyItem['image_urls'] = self.url_join(imagePath, response)
        # scrapyItem['image_paths'] = response.xpath(
        # '//div[@class="phone-details"]/img/@src').extract_first()
        return scrapyItem

    def url_join(self, url, response):
        joined_urls = []
        joined_urls.append(response.urljoin(url))
        return joined_urls
