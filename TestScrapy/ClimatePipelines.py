from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
import MySQLdb.cursors
import codecs
import json
from logging import log
import json


class ClimatePipeline(object):
    @classmethod
    def from_settings(cls, settings):
        db_params = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **db_params)
        return cls(dbpool)

    def __init__(self, dbpool):
        self.dbpool = dbpool

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_update, item)
        query.addErrback(self._handle_error, item, spider)
        return item

    @staticmethod
    def _conditional_update(tx, item):
        insert_climate_code = 'insert ignore into `climate_code`(`code`, `climate`) values(%s, %s)'
        insert_station_forecast = 'replace into `station_forecast`(`station_id`, `time`, `temp`, `prep`, `climate`, `wind_speed`, `wind_dire`, `air_pres`, `relative_hum`, `cloud`, `visibility`) values((select station_id from `station_location` where `station_name` = %s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        # insert_station_forecast = 'insert into `station_forecast`(`station_id`, `time`, `temp`, `prep`, `climate`, `wind_speed`, `wind_dire`, `air_pres`, `relative_hum`, `cloud`, `visibility`) values((select station_id from `station_location` where `station_name` = %s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        params_climate_code = (item['climate_code'], item['day_climate'])
        params_station_forecast = (item['name'], item['time'], item['temp'],  item['prep'], item['climate'], item['wind_speed'], item['wind_dire'], item['air_pres'], item['relative_hum'], item['cloud'], item['visibility'])
        tx.execute(insert_climate_code, params_climate_code)
        tx.execute(insert_station_forecast, params_station_forecast)

    @staticmethod
    def _handle_error(failure, item, spider):
        print("+++++++++++++++++++++++++++1111111")
        print '--------------database operation exception!!-----------------'
        print '-------------------------------------------------------------'
        print failure
