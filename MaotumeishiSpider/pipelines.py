# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from MaotumeishiSpider.items import CityItem,RestaurantItem
import pymysql


class CityItemPipeline(object):
    def __init__(self):
        self.client = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='123456',
            db='zyf',
            charset='utf8'
        )
        self.cur = self.client.cursor()

    def process_item(self, item, spider):
        if isinstance(item, CityItem):
            sql = 'insert into cityItem(province,cityname,rests,comments) values(%s,%s,%s,%s)'
            lis = (item['cityProvince'], item['cityName'], item['totalRestaurants'], item['totalComments'])
            self.cur.execute(sql, lis)
            self.client.commit()
            return item
        if isinstance(item, RestaurantItem):
            sql = 'insert into restaurant(name,rank,commands,score,address,phone,pics,foodstyle,meattime,businesshour) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            lis = (item['name'], item['ranking'], item['commands'], item['score'], item['address'], item['phoneNumber'], item['pics'], item['foodStyle'], item['mealTime'], item['businessHours'])
            self.cur.execute(sql, lis)
            self.client.commit()
            return item

# class RestaurantItemPipeline(object):
#     def __init__(self):
#         self.client = pymysql.connect(
#             host='127.0.0.1',
#             port=3306,
#             user='root',
#             password='123456',
#             db='zyf',
#             charset='utf8'
#         )
#         self.cur = self.client.cursor()
#
#     def process_item(self, item, spider):
#         if isinstance(item, RestaurantItem):
#             sql = 'insert into restaurant(name,rank,commands,score,address,phone,pics,foodstyle,meattime,businesshour) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
#             lis = (item['name'], item['ranking'], item['commands'], item['score'], item['address'], item['phoneNumber'], item['pics'], item['foodStyle'], item['mealTime'], item['businessHours'])
#             self.cur.execute(sql, lis)
#             self.client.commit()
#             return item
