# coding=utf-8
from scrapy.exceptions import DropItem
import MySQLdb


class ClimatePipeline(object):
    def __init__(self):
        # 初始化数据库对象
        self.connect = MySQLdb.connect('192.168.129.193', 'blm', 'boloomodb', 'jjsw', charset='utf8')
        # self.connect = MySQLdb.connect('192.168.129.187', 'root', '123456', 'climate', charset='utf8')
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        insert_climate_code = 'insert ignore into `climate_code`(`code`, `climate`) values(%s, %s)'
        replace_station_forecast = 'replace into `station_forecast`(`station_id`, `time`, `temp`, `prep`, `climate`, `wind_speed`, `wind_dire`, `air_pres`, `relative_hum`, `cloud`, `visibility`) values((select station_id from `station_location` where `station_name` = %s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        params_climate_code = (item['climate_code'], item['day_climate'])
        params_station_forecast = (item['name'], item['time'], item['temp'], item['prep'], item['climate'], item['wind_speed'], item['wind_dire'], item['air_pres'], item['relative_hum'], item['cloud'], item['visibility'])
        self.cursor.execute(replace_station_forecast, params_station_forecast)
        self.cursor.execute(insert_climate_code, params_climate_code)
        self.connect.commit()

    def closed_spider(self, spider):
        self.cursor.close()
        self.connect.close()
