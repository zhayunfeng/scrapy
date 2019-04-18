# -*- coding: utf-8 -*-
import scrapy
import MaotumeishiSpider.items as msi
import re


class MeishiSpider(scrapy.Spider):
    name = 'meishi'
    allowed_domains = ['tripadvisor.cn']
    start_urls = ['https://www.tripadvisor.cn/Restaurants-g294211-China.html#LOCATION_LIST']
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
        }
    }

    def parse(self, response):
        for i in range(0, 212):  # 分页寻找
            url = "https://www.tripadvisor.cn/TourismChildrenAjax?geo=294211&offset={}&desktop=true".format(i)
            yield scrapy.Request(url, callback=self.parse_page_guide)
            print(url)

    def parse_page_guide(self, response):    # 进入具体城市向导页
        urls = response.xpath('//a/@href').extract()
        for url in urls:
            url = 'https://www.tripadvisor.cn'+url
            print(url)
            yield scrapy.Request(url, callback=self.parse_city_guide)

    def parse_city_guide(self,response):   # 城市向导页  并获取cityItem
        if response.xpath('//div[@class="navLinks"]/ul/li[3]/@class').extract()[0] == 'restaurants twoLines':
            string = response.xpath('//head/meta[@name="location"]/@content').extract()[0]
            strs = string.split(';')
            cityitem = msi.CityItem()
            cityitem['cityProvince'] = re.sub("[a-z\=]", "", strs[0])
            print(cityitem['cityProvince'])
            cityitem['cityName'] = re.sub("[a-z\=]", "", strs[1])
            print(cityitem['cityName'])
            cityitem['totalRestaurants'] = re.sub("[\(\)\,]", "",response.xpath('//span[@class="typeQty"]/text()').extract()[2])
            print(cityitem['totalRestaurants'])
            cityitem['totalComments'] = re.sub("\D", "",
                                               response.xpath('//span[@class="contentCount"]/text()').extract()[2])
            print(cityitem['totalComments'])
            yield cityitem
            url = 'https://www.tripadvisor.cn'+response.xpath('//li[@class="restaurants twoLines"]/a/@href').extract()[0]
            yield scrapy.Request(url, callback=self.parse_city)


    def parse_city(self, response):   # 爬取城市美食

        index = response.xpath('//div[@class="deckTools btm"]').extract()[0]
        if index == '<div class="deckTools btm">\n</div>':    #如果不分页，直接爬取
            urls = response.xpath('//div[@id="EATERY_SEARCH_RESULTS"]/div/div[2]/div[1]/div[1]/a/@href').extract()  # 获取城市中的餐厅列表
            for url in urls:
                url = 'https://www.tripadvisor.cn'+url
                yield scrapy.Request(url, callback=self.parse_restaurant) #具体餐厅

        else:     #如果分页，要分页爬取
            pages = int(response.xpath('//div[@class="pageNumbers"]/a/text()').extract()[-1].replace("\n", ""))
            print(pages)
            for i in range(pages):
                url = response.xpath('//div[@class="pageNumbers"]/a[1]/@href').extract()[0]
                urlspit = url.split("-")
                url = "https://www.tripadvisor.cn"+urlspit[0]+"-"+urlspit[1]+"-oa"+str(i*30)+"-"+urlspit[3]
                print(url)
                yield scrapy.Request(url, callback=self.parse_one_page)

    def parse_one_page(self, response):

        urls = response.xpath(
            '//div[@id="EATERY_SEARCH_RESULTS"]/div/div[2]/div[1]/div[1]/a/@href').extract()  # 获取城市中的餐厅列表
        for url in urls:
            url = 'https://www.tripadvisor.cn' + url
            yield scrapy.Request(url, callback=self.parse_restaurant)  # 具体餐厅

    def parse_restaurant(self, response):
        restaurantItem = msi.RestaurantItem()
        try:
            name =response.xpath('//h1[@class="ui_header h1"]/text()').extract()[0]
        except:
            restaurantItem['name'] = ''
        else:
            restaurantItem['name'] = name
            print(name)

        try:
            ranking = \
            response.xpath('//span[@class="header_popularity popIndexValidation"]/text()').extract()[0] + \
            response.xpath('//span[@class="header_popularity popIndexValidation"]/b/span/text()').extract()[0]
        except:
            restaurantItem['ranking'] = ''
        else:
            restaurantItem['ranking'] = ranking
            print(ranking)

        try:
            commands = response.xpath('//span[@class="reviewCount"]/text()').extract()[0]
        except:
            restaurantItem['commands'] = ''
        else:
            restaurantItem['commands'] = commands
            print(commands)

        try:
            score = response.xpath(
                '//span[@class="restaurants-detail-overview-cards-RatingsOverviewCard__overallRating--nohTl"]/text()').extract()[
                0]
        except:
            restaurantItem['score'] = 0.0
        else:
            restaurantItem['score'] = score
            print(score)

        try:
            address = response.xpath('//span[@class="detail "]')[0].xpath('string(.)').extract()[0]
        except:
            restaurantItem['address'] = ''
        else:
            restaurantItem['address'] = address
            print(address)

        try:
            phoneNumber = response.xpath('//span[@class="detail  is-hidden-mobile"]/text()').extract()[0]
        except:
            restaurantItem['phoneNumber'] = ''
        else:
            restaurantItem['phoneNumber'] = phoneNumber
            print(phoneNumber)

        try:
            pics = response.xpath('//span[@class="details"]/text()').extract()[0]
        except:
            restaurantItem['pics'] = 0
        else:
            restaurantItem['pics'] = pics
            print(pics)

        try:
            foodStyle = ','.join(response.xpath('//div[@class="header_links"]/a/text()').extract())
        except:

            restaurantItem['foodStyle'] = ''
        else:
            restaurantItem['foodStyle'] = foodStyle
            print(foodStyle)

        try:
            mealTime = response.xpath(
                '//div[@class="restaurants-detail-overview-cards-DetailsSectionOverviewCard__tagText--1OH6h"]/text()').extract()[
                2]
        except:

            restaurantItem['mealTime'] = ''
        else:
            restaurantItem['mealTime'] = mealTime
            print(mealTime)

        try:
            businessHours = response.xpath(
                '//span[@class="public-location-hours-LocationHours__hoursOpenerText--42y6t"]/span[2]/text()').extract()[
                0]
        except:
            restaurantItem['businessHours'] = ''
        else:
            restaurantItem['businessHours'] = businessHours
            print(businessHours)

        yield restaurantItem



