# coding=utf-8
from scrapy.exceptions import DropItem
import MySQLdb


class ClimatePipeline(object):
    def __init__(self):
        # 初始化数据库对象
        self.connect = MySQLdb.connect('192.168.129.83', 'blm', 'boloomodb', 'jjsw_env', charset='utf8')
        # self.connect = MySQLdb.connect('192.168.129.187', 'root', '123456', 'climate', charset='utf8')
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        insert_climate_code = 'insert ignore into `codetable_climate_code`(`CLIMATE_CODE_ID`, `NAME`) values(%s, %s)'
        replace_station_forecast = 'replace into `t1101_meteorology`(`COUNTY_ID`, `TIME`, `TEMP`, `RAINFALL`, `CLIMATE_ID`, `WIND_SPEED`, `WIND_DIRECTION`, `AIR_PRESSURE`, `RELATIVE_HUM`, `CLOUDAGE`, `VISIBILITY`) values((select COUNTY_ID from `t1201_county` where `NAME` = %s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        params_climate_code = (item['climate_code'], item['day_climate'])
        params_station_forecast = (item['name'], item['time'], item['temp'], item['prep'], item['climate'], item['wind_speed'], item['wind_dire'], item['air_pres'], item['relative_hum'], item['cloud'], item['visibility'])
        self.cursor.execute(replace_station_forecast, params_station_forecast)
        self.cursor.execute(insert_climate_code, params_climate_code)
        self.connect.commit()

    def closed_spider(self, spider):
        self.cursor.close()
        self.connect.close()
