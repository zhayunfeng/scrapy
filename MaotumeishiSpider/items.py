# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CityItem(scrapy.Item):
    # define the fields for your item here like:
    cityName = scrapy.Field()
    cityProvince = scrapy.Field()
    totalRestaurants = scrapy.Field()
    totalComments = scrapy.Field()


class RestaurantItem(scrapy.Item):
    name = scrapy.Field()
    ranking = scrapy.Field()
    commands = scrapy.Field()
    score = scrapy.Field()
    address = scrapy.Field()
    phoneNumber = scrapy.Field()
    pics = scrapy.Field()
    foodStyle = scrapy.Field()
    mealTime = scrapy.Field()
    businessHours = scrapy.Field()


class CommandItem(scrapy.Item):
    commandId = scrapy.Field()
    restaurantId = scrapy.Field()
    dinnerDate = scrapy.Field()
    commandDate = scrapy.Field()
    commanderId = scrapy.Field()
    score = scrapy.Field()
    praise = scrapy.Field()
    commandContentNumber = scrapy.Field()
    commandTitle = scrapy.Field()
    commandContent = scrapy.Field()
    response = scrapy.Field()
    responseContent = scrapy.Field()


class CommanderItem(scrapy.Item):
    commanderId = scrapy.Field()
    commander = scrapy.Field()
    commanderLevel = scrapy.Field()
    joinTime = scrapy.Field()
    fromVIP = scrapy.Field()
    fromCity = scrapy.Field()
    commandCommendNumbers = scrapy.Field()
    commandShareNumbers = scrapy.Field()
    beenCitys = scrapy.Field()
    pics = scrapy.Field()
    veryGood = scrapy.Field()
    good = scrapy.Field()
    average = scrapy.Field()
    notGood = scrapy.Field()
    bad = scrapy.Field()


class AroundHotelItem(scrapy.Item):
    hotelId = scrapy.Field()
    hotelName = scrapy.Field()
    distance = scrapy.Field()


class AroundRestaurantItem(scrapy.Item):
    RestaurantId = scrapy.Field()
    RestaurantName = scrapy.Field()
    distance = scrapy.Field()


class AroundSceneryItem(scrapy.Item):
    SceneryId = scrapy.Field()
    SceneryName = scrapy.Field()
    distance = scrapy.Field()
