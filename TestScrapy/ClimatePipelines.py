from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
import MySQLdb
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
            charset='utf-8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False
        )

    def process_item(self, item, spider):
        print(item)
        return item
