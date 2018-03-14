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
        insert_location = 'insert into `station_location`(`station_name`, `lat`, `lng`) values(%s, %s, %s) on duplicate key update station_id = station_id'
        update_climate = 'insert into `station_climate`(`station_id`, `time`, `temp`, `prep`) values((select station_id from `station_location` where `station_name` = %s), %s, %s, %s) on duplicate key update `temp` = %s, `prep` = %s'
        params_station_location = (item['name'], item['lat'], item['lng'])
        params_station_climate = (item['name'], item['time'], item['temp'],  item['prep'], item['temp'], item['prep'])
        tx.execute(insert_location, params_station_location)
        tx.execute(update_climate, params_station_climate)

    @staticmethod
    def _handle_error(failure, item, spider):
        print("+++++++++++++++++++++++++++1111111")
        print '--------------database operation exception!!-----------------'
        print '-------------------------------------------------------------'
        print failure
