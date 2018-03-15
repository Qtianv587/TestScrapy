# coding=utf-8
import scrapy
import time
import re
from TestScrapy.ClimateItems import ClimateItem


class ClimateSpider(scrapy.Spider):
    name = "ClimateSpider"
    allowed_domains = ["nmc.gov.cn"]
    stations = ["chengdu", "longquanyi", "xindu", "wenjiang", "jintang", "shuangliu", "pixian", "dayi", "pujiang",
                "xinjin", "dujiangyan", "pengxian", "qionglai", "chongqing"]
    start_urls = []
    for station in stations:
        start_urls.append("http://www.nmc.gov.cn/publish/forecast/ASC/" + station + ".html")

    def parse(self, response):
        time_now = time.time()
        date_day0 = time.strftime('%Y-%m-%d', time.localtime(time_now))
        date_day1 = time.strftime('%Y-%m-%d', time.localtime(time_now + 24 * 3600))
        date_day2 = time.strftime('%Y-%m-%d', time.localtime(time_now + 24 * 3600 * 2))
        date_day3 = time.strftime('%Y-%m-%d', time.localtime(time_now + 24 * 3600 * 3))
        date_day4 = time.strftime('%Y-%m-%d', time.localtime(time_now + 24 * 3600 * 4))
        date_day5 = time.strftime('%Y-%m-%d', time.localtime(time_now + 24 * 3600 * 5))
        date_day6 = time.strftime('%Y-%m-%d', time.localtime(time_now + 24 * 3600 * 6))
        date_day7 = time.strftime('%Y-%m-%d', time.localtime(time_now + 24 * 3600 * 7))

        item = ClimateItem()
        for box in response.xpath('//*[@id="hour3"]'):
            station_name = box.xpath('/html/head/title/text()').extract()[0].split("-")[0]

            for table0 in box.xpath('//*[@id="day0"]'):  # 表示today的数据
                climate_url = response.xpath('//*[@id="forecast"]/div[1]/div[1]/table/tbody/tr[2]/td[1]/img/@src').extract()[0]
                climate_code = re.findall(r"/([0-9]*)\.png", climate_url)[0]
                day_climate = response.xpath('//*[@id="forecast"]/div[1]/div[1]/table/tbody/tr[3]/td[1]/text()').extract()[0]

                date = date_day0
                time_list = []
                temp_list = []
                prep_list = []
                climate_list = []
                ws_list = []
                wd_list = []
                air_pres_list = []
                relative_hum_list = []
                cloud_list = []
                visi_list = []
                # 时间
                for times in table0.xpath('./div[1]//div'):
                    time_str = times.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '日' in time_str:
                        date = date_day1
                        time_str = time_str.split('日')[1]  # 遇见'日'字表示到了第二天的时间

                    if '精细' in time_str:
                        continue
                    time_list.append(date + " " + time_str + ":00")

                #  天气现象
                for climates in table0.xpath('./div[2]//div'):
                    if '现象' in climates.xpath('./text()').extract()[0].strip().encode('utf-8'):
                        continue
                    climate = climates.xpath('./img/@src').extract()[0]
                    print("========regregreg======")
                    # print(climate)
                    res = re.findall(r"/([0-9]*)\.png", climate)[0]
                    climate_list.append(res)

                #  温度
                for temps in table0.xpath('./div[3]//div'):
                    temp_str = temps.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '气温' in temp_str:
                        continue
                    temp_list.append(temp_str.strip('℃'))

                #  降雨量
                for preps in table0.xpath('./div[4]//div'):
                    prep_str = preps.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '降水' == prep_str:
                        continue
                    if '无降水' == prep_str:
                        prep_list.append('0')
                        continue
                    prep_list.append(prep_str.strip('毫米'))

                #  风速
                for w_speeds in table0.xpath('./div[5]//div'):
                    ws_str = w_speeds.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '风速' in ws_str:
                        continue
                    ws_list.append(ws_str.strip('米/秒'))

                #  风向
                for w_dires in table0.xpath('./div[6]//div'):
                    wd_str = w_dires.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if wd_str == '东风':
                        continue
                    if '风向' in wd_str:
                        wd_list.append('E')
                    elif wd_str == '西风':
                        wd_list.append('W')
                    elif wd_str == '南风':
                        wd_list.append('S')
                    elif wd_str == '北风':
                        wd_list.append('N')
                    elif wd_str == '西北风':
                        wd_list.append('NW')
                    elif wd_str == '东北风':
                        wd_list.append('NE')
                    elif wd_str == '西南风':
                        wd_list.append('SW')
                    elif wd_str == '东南风':
                        wd_list.append('SE')

                #  气压
                for air_pres in table0.xpath('./div[7]//div'):
                    air_pre_str = air_pres.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '气压' in air_pre_str:
                        continue
                    air_pres_list.append(air_pre_str)

                #  相对温度
                for relative_hums in table0.xpath('./div[8]//div'):
                    relative_hum_str = relative_hums.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '相对湿度' in relative_hum_str:
                        continue
                    relative_hum_list.append(relative_hum_str.strip('%'))

                #  云量
                for clouds in table0.xpath('./div[9]//div'):
                    cloud_str = clouds.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '云量' in cloud_str:
                        continue
                    cloud_list.append(cloud_str.strip('%'))

                #  能见度
                for visis in table0.xpath('./div[10]//div'):
                    visi_str = visis.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '能见度' in visi_str:
                        continue
                    visi_list.append(visi_str.strip('公里').strip('≥'))

                for i in range(0, len(time_list)):
                    item['name'] = station_name
                    item['climate_code'] = climate_code
                    item['day_climate'] = day_climate
                    item['time'] = time_list[i]
                    item['climate'] = climate_list[i]
                    item['temp'] = temp_list[i]
                    item['prep'] = prep_list[i]
                    item['wind_speed'] = ws_list[i]
                    item['wind_dire'] = wd_list[i]
                    item['air_pres'] = air_pres_list[i]
                    item['relative_hum'] = relative_hum_list[i]
                    item['cloud'] = cloud_list[i]
                    item['visibility'] = visi_list[i]
                    yield item
            for table1 in box.xpath('//*[@id="day1"]'):  # 表示today的数据
                climate_url = \
                response.xpath('//*[@id="forecast"]/div[2]/div[1]/table/tbody/tr[2]/td[1]/img/@src').extract()[0]
                climate_code = re.findall(r"/([0-9]*)\.png", climate_url)[0]
                day_climate = \
                response.xpath('//*[@id="forecast"]/div[2]/div[1]/table/tbody/tr[3]/td[1]/text()').extract()[0].encode(
                    'utf-8')
                date = date_day1
                time_list = []
                temp_list = []
                prep_list = []
                climate_list = []
                ws_list = []
                wd_list = []
                air_pres_list = []
                relative_hum_list = []
                cloud_list = []
                visi_list = []
                # 时间
                for times in table1.xpath('./div[1]//div'):
                    time_str = times.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '日' in time_str:
                        date = date_day2
                        time_str = time_str.split('日')[1]  # 遇见'日'字表示到了第二天的时间

                    if '精细' in time_str:
                        continue
                    time_list.append(date + " " + time_str + ":00")

                #  天气现象
                for climates in table1.xpath('./div[2]//div'):
                    if '现象' in climates.xpath('./text()').extract()[0].strip().encode('utf-8'):
                        continue
                    climate = climates.xpath('./img/@src').extract()[0]
                    print("========regregreg======")
                    # print(climate)
                    res = re.findall(r"/([0-9]*)\.png", climate)[0]
                    climate_list.append(res)


                #  温度
                for temps in table1.xpath('./div[3]//div'):
                    temp_str = temps.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '气温' in temp_str:
                        continue
                    temp_list.append(temp_str.strip('℃'))

                #  降雨量
                for preps in table1.xpath('./div[4]//div'):
                    prep_str = preps.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '降水' == prep_str:
                        continue
                    if '无降水' == prep_str:
                        prep_list.append('0')
                        continue
                    prep_list.append(prep_str.strip('毫米'))

                #  风速
                for w_speeds in table1.xpath('./div[5]//div'):
                    ws_str = w_speeds.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '风速' in ws_str:
                        continue
                    ws_list.append(ws_str.strip('米/秒'))

                #  风向
                for w_dires in table1.xpath('./div[6]//div'):
                    wd_str = w_dires.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if wd_str == '东风':
                        continue
                    if '风向' in wd_str:
                        wd_list.append('E')
                    elif wd_str == '西风':
                        wd_list.append('W')
                    elif wd_str == '南风':
                        wd_list.append('S')
                    elif wd_str == '北风':
                        wd_list.append('N')
                    elif wd_str == '西北风':
                        wd_list.append('NW')
                    elif wd_str == '东北风':
                        wd_list.append('NE')
                    elif wd_str == '西南风':
                        wd_list.append('SW')
                    elif wd_str == '东南风':
                        wd_list.append('SE')

                #  气压
                for air_pres in table1.xpath('./div[7]//div'):
                    air_pre_str = air_pres.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '气压' in air_pre_str:
                        continue
                    air_pres_list.append(air_pre_str)

                #  相对温度
                for relative_hums in table1.xpath('./div[8]//div'):
                    relative_hum_str = relative_hums.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '相对湿度' in relative_hum_str:
                        continue
                    relative_hum_list.append(relative_hum_str.strip('%'))

                #  云量
                for clouds in table1.xpath('./div[9]//div'):
                    cloud_str = clouds.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '云量' in cloud_str:
                        continue
                    cloud_list.append(cloud_str.strip('%'))

                #  能见度
                for visis in table1.xpath('./div[10]//div'):
                    visi_str = visis.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '能见度' in visi_str:
                        continue
                    visi_list.append(visi_str.strip('公里').strip('≥'))

                for i in range(0, len(time_list)):
                    item['name'] = station_name
                    item['time'] = time_list[i]
                    item['temp'] = temp_list[i]
                    item['prep'] = prep_list[i]
                    item['wind_speed'] = ws_list[i]
                    item['wind_dire'] = wd_list[i]
                    item['air_pres'] = air_pres_list[i]
                    item['relative_hum'] = relative_hum_list[i]
                    item['cloud'] = cloud_list[i]
                    item['visibility'] = visi_list[i]
                    yield item
            for table2 in box.xpath('//*[@id="day1"]'):  # 表示today的数据
                climate_url = \
                response.xpath('//*[@id="forecast"]/div[3]/div[1]/table/tbody/tr[2]/td[1]/img/@src').extract()[0]
                climate_code = re.findall(r"/([0-9]*)\.png", climate_url)[0]
                day_climate = \
                response.xpath('//*[@id="forecast"]/div[3]/div[1]/table/tbody/tr[3]/td[1]/text()').extract()[0].encode(
                    'utf-8')

                date = date_day2
                time_list = []
                temp_list = []
                prep_list = []
                climate_list = []
                ws_list = []
                wd_list = []
                air_pres_list = []
                relative_hum_list = []
                cloud_list = []
                visi_list = []
                # 时间
                for times in table2.xpath('./div[1]//div'):
                    time_str = times.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '日' in time_str:
                        date = date_day3
                        time_str = time_str.split('日')[1]  # 遇见'日'字表示到了第二天的时间

                    if '精细' in time_str:
                        continue
                    time_list.append(date + " " + time_str + ":00")

                #  天气现象
                for climates in table2.xpath('./div[2]//div'):
                    if '现象' in climates.xpath('./text()').extract()[0].strip().encode('utf-8'):
                        continue
                    climate = climates.xpath('./img/@src').extract()[0]
                    print("========regregreg======")
                    # print(climate)
                    res = re.findall(r"/([0-9]*)\.png", climate)[0]
                    climate_list.append(res)


                #  温度
                for temps in table2.xpath('./div[3]//div'):
                    temp_str = temps.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '气温' in temp_str:
                        continue
                    temp_list.append(temp_str.strip('℃'))

                #  降雨量
                for preps in table2.xpath('./div[4]//div'):
                    prep_str = preps.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '降水' == prep_str:
                        continue
                    if '无降水' == prep_str:
                        prep_list.append('0')
                        continue
                    prep_list.append(prep_str.strip('毫米'))

                #  风速
                for w_speeds in table2.xpath('./div[5]//div'):
                    ws_str = w_speeds.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '风速' in ws_str:
                        continue
                    ws_list.append(ws_str.strip('米/秒'))

                #  风向
                for w_dires in table2.xpath('./div[6]//div'):
                    wd_str = w_dires.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if wd_str == '东风':
                        continue
                    if '风向' in wd_str:
                        wd_list.append('E')
                    elif wd_str == '西风':
                        wd_list.append('W')
                    elif wd_str == '南风':
                        wd_list.append('S')
                    elif wd_str == '北风':
                        wd_list.append('N')
                    elif wd_str == '西北风':
                        wd_list.append('NW')
                    elif wd_str == '东北风':
                        wd_list.append('NE')
                    elif wd_str == '西南风':
                        wd_list.append('SW')
                    elif wd_str == '东南风':
                        wd_list.append('SE')

                #  气压
                for air_pres in table2.xpath('./div[7]//div'):
                    air_pre_str = air_pres.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '气压' in air_pre_str:
                        continue
                    air_pres_list.append(air_pre_str)

                #  相对温度
                for relative_hums in table2.xpath('./div[8]//div'):
                    relative_hum_str = relative_hums.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '相对湿度' in relative_hum_str:
                        continue
                    relative_hum_list.append(relative_hum_str.strip('%'))

                #  云量
                for clouds in table2.xpath('./div[9]//div'):
                    cloud_str = clouds.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '云量' in cloud_str:
                        continue
                    cloud_list.append(cloud_str.strip('%'))

                #  能见度
                for visis in table2.xpath('./div[10]//div'):
                    visi_str = visis.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '能见度' in visi_str:
                        continue
                    visi_list.append(visi_str.strip('公里').strip('≥'))

                for i in range(0, len(time_list)):
                    item['name'] = station_name
                    item['time'] = time_list[i]
                    item['temp'] = temp_list[i]
                    item['prep'] = prep_list[i]
                    item['wind_speed'] = ws_list[i]
                    item['wind_dire'] = wd_list[i]
                    item['air_pres'] = air_pres_list[i]
                    item['relative_hum'] = relative_hum_list[i]
                    item['cloud'] = cloud_list[i]
                    item['visibility'] = visi_list[i]
                    yield item
            for table3 in box.xpath('//*[@id="day1"]'):  # 表示today的数据
                climate_url = \
                response.xpath('//*[@id="forecast"]/div[4]/div[1]/table/tbody/tr[2]/td[1]/img/@src').extract()[0]
                climate_code = re.findall(r"/([0-9]*)\.png", climate_url)[0]
                day_climate = \
                response.xpath('//*[@id="forecast"]/div[4]/div[1]/table/tbody/tr[3]/td[1]/text()').extract()[0].encode(
                    'utf-8')

                date = date_day3
                time_list = []
                temp_list = []
                prep_list = []
                climate_list = []
                ws_list = []
                wd_list = []
                air_pres_list = []
                relative_hum_list = []
                cloud_list = []
                visi_list = []
                # 时间
                for times in table3.xpath('./div[1]//div'):
                    time_str = times.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '日' in time_str:
                        date = date_day4
                        time_str = time_str.split('日')[1]  # 遇见'日'字表示到了第二天的时间

                    if '精细' in time_str:
                        continue
                    time_list.append(date + " " + time_str + ":00")

                #  天气现象
                for climates in table3.xpath('./div[2]//div'):
                    if '现象' in climates.xpath('./text()').extract()[0].strip().encode('utf-8'):
                        continue
                    climate = climates.xpath('./img/@src').extract()[0]
                    print("========regregreg======")
                    # print(climate)
                    res = re.findall(r"/([0-9]*)\.png", climate)[0]
                    climate_list.append(res)


                #  温度
                for temps in table3.xpath('./div[3]//div'):
                    temp_str = temps.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '气温' in temp_str:
                        continue
                    temp_list.append(temp_str.strip('℃'))

                #  降雨量
                for preps in table3.xpath('./div[4]//div'):
                    prep_str = preps.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '降水' == prep_str:
                        continue
                    if '无降水' == prep_str:
                        prep_list.append('0')
                        continue
                    prep_list.append(prep_str.strip('毫米'))

                #  风速
                for w_speeds in table3.xpath('./div[5]//div'):
                    ws_str = w_speeds.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '风速' in ws_str:
                        continue
                    ws_list.append(ws_str.strip('米/秒'))

                #  风向
                for w_dires in table3.xpath('./div[6]//div'):
                    wd_str = w_dires.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if wd_str == '东风':
                        continue
                    if '风向' in wd_str:
                        wd_list.append('E')
                    elif wd_str == '西风':
                        wd_list.append('W')
                    elif wd_str == '南风':
                        wd_list.append('S')
                    elif wd_str == '北风':
                        wd_list.append('N')
                    elif wd_str == '西北风':
                        wd_list.append('NW')
                    elif wd_str == '东北风':
                        wd_list.append('NE')
                    elif wd_str == '西南风':
                        wd_list.append('SW')
                    elif wd_str == '东南风':
                        wd_list.append('SE')

                #  气压
                for air_pres in table3.xpath('./div[7]//div'):
                    air_pre_str = air_pres.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '气压' in air_pre_str:
                        continue
                    air_pres_list.append(air_pre_str)

                #  相对温度
                for relative_hums in table3.xpath('./div[8]//div'):
                    relative_hum_str = relative_hums.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '相对湿度' in relative_hum_str:
                        continue
                    relative_hum_list.append(relative_hum_str.strip('%'))

                #  云量
                for clouds in table3.xpath('./div[9]//div'):
                    cloud_str = clouds.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '云量' in cloud_str:
                        continue
                    cloud_list.append(cloud_str.strip('%'))

                #  能见度
                for visis in table3.xpath('./div[10]//div'):
                    visi_str = visis.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '能见度' in visi_str:
                        continue
                    visi_list.append(visi_str.strip('公里').strip('≥'))

                for i in range(0, len(time_list)):
                    item['name'] = station_name
                    item['time'] = time_list[i]
                    item['temp'] = temp_list[i]
                    item['prep'] = prep_list[i]
                    item['wind_speed'] = ws_list[i]
                    item['wind_dire'] = wd_list[i]
                    item['air_pres'] = air_pres_list[i]
                    item['relative_hum'] = relative_hum_list[i]
                    item['cloud'] = cloud_list[i]
                    item['visibility'] = visi_list[i]
                    yield item
            for table4 in box.xpath('//*[@id="day1"]'):  # 表示today的数据
                climate_url = \
                response.xpath('//*[@id="forecast"]/div[5]/div[1]/table/tbody/tr[2]/td[1]/img/@src').extract()[0]
                climate_code = re.findall(r"/([0-9]*)\.png", climate_url)[0]
                day_climate = \
                response.xpath('//*[@id="forecast"]/div[5]/div[1]/table/tbody/tr[3]/td[1]/text()').extract()[0].encode(
                    'utf-8')

                date = date_day4
                time_list = []
                temp_list = []
                prep_list = []
                climate_list = []
                ws_list = []
                wd_list = []
                air_pres_list = []
                relative_hum_list = []
                cloud_list = []
                visi_list = []
                # 时间
                for times in table4.xpath('./div[1]//div'):
                    time_str = times.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '日' in time_str:
                        date = date_day5
                        time_str = time_str.split('日')[1]  # 遇见'日'字表示到了第二天的时间

                    if '精细' in time_str:
                        continue
                    time_list.append(date + " " + time_str + ":00")

                #  天气现象
                for climates in table4.xpath('./div[2]//div'):
                    if '现象' in climates.xpath('./text()').extract()[0].strip().encode('utf-8'):
                        continue
                    climate = climates.xpath('./img/@src').extract()[0]
                    print("========regregreg======")
                    # print(climate)
                    res = re.findall(r"/([0-9]*)\.png", climate)[0]
                    climate_list.append(res)


                #  温度
                for temps in table4.xpath('./div[3]//div'):
                    temp_str = temps.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '气温' in temp_str:
                        continue
                    temp_list.append(temp_str.strip('℃'))

                #  降雨量
                for preps in table4.xpath('./div[4]//div'):
                    prep_str = preps.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '降水' == prep_str:
                        continue
                    if '无降水' == prep_str:
                        prep_list.append('0')
                        continue
                    prep_list.append(prep_str.strip('毫米'))

                #  风速
                for w_speeds in table4.xpath('./div[5]//div'):
                    ws_str = w_speeds.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '风速' in ws_str:
                        continue
                    ws_list.append(ws_str.strip('米/秒'))

                #  风向
                for w_dires in table4.xpath('./div[6]//div'):
                    wd_str = w_dires.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if wd_str == '东风':
                        continue
                    if '风向' in wd_str:
                        wd_list.append('E')
                    elif wd_str == '西风':
                        wd_list.append('W')
                    elif wd_str == '南风':
                        wd_list.append('S')
                    elif wd_str == '北风':
                        wd_list.append('N')
                    elif wd_str == '西北风':
                        wd_list.append('NW')
                    elif wd_str == '东北风':
                        wd_list.append('NE')
                    elif wd_str == '西南风':
                        wd_list.append('SW')
                    elif wd_str == '东南风':
                        wd_list.append('SE')

                #  气压
                for air_pres in table4.xpath('./div[7]//div'):
                    air_pre_str = air_pres.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '气压' in air_pre_str:
                        continue
                    air_pres_list.append(air_pre_str)

                #  相对温度
                for relative_hums in table4.xpath('./div[8]//div'):
                    relative_hum_str = relative_hums.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '相对湿度' in relative_hum_str:
                        continue
                    relative_hum_list.append(relative_hum_str.strip('%'))

                #  云量
                for clouds in table4.xpath('./div[9]//div'):
                    cloud_str = clouds.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '云量' in cloud_str:
                        continue
                    cloud_list.append(cloud_str.strip('%'))

                #  能见度
                for visis in table4.xpath('./div[10]//div'):
                    visi_str = visis.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '能见度' in visi_str:
                        continue
                    visi_list.append(visi_str.strip('公里').strip('≥'))

                for i in range(0, len(time_list)):
                    item['name'] = station_name
                    item['time'] = time_list[i]
                    item['temp'] = temp_list[i]
                    item['prep'] = prep_list[i]
                    item['wind_speed'] = ws_list[i]
                    item['wind_dire'] = wd_list[i]
                    item['air_pres'] = air_pres_list[i]
                    item['relative_hum'] = relative_hum_list[i]
                    item['cloud'] = cloud_list[i]
                    item['visibility'] = visi_list[i]
                    yield item
            for table5 in box.xpath('//*[@id="day1"]'):  # 表示today的数据
                climate_url = \
                response.xpath('//*[@id="forecast"]/div[6]/div[1]/table/tbody/tr[2]/td[1]/img/@src').extract()[0]
                climate_code = re.findall(r"/([0-9]*)\.png", climate_url)[0]
                day_climate = \
                response.xpath('//*[@id="forecast"]/div[6]/div[1]/table/tbody/tr[3]/td[1]/text()').extract()[0].encode(
                    'utf-8')

                date = date_day5
                time_list = []
                temp_list = []
                prep_list = []
                climate_list = []
                ws_list = []
                wd_list = []
                air_pres_list = []
                relative_hum_list = []
                cloud_list = []
                visi_list = []
                # 时间
                for times in table5.xpath('./div[1]//div'):
                    time_str = times.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '日' in time_str:
                        date = date_day6
                        time_str = time_str.split('日')[1]  # 遇见'日'字表示到了第二天的时间

                    if '精细' in time_str:
                        continue
                    time_list.append(date + " " + time_str + ":00")

                #  天气现象
                for climates in table5.xpath('./div[2]//div'):
                    if '现象' in climates.xpath('./text()').extract()[0].strip().encode('utf-8'):
                        continue
                    climate = climates.xpath('./img/@src').extract()[0]
                    print("========regregreg======")
                    # print(climate)
                    res = re.findall(r"/([0-9]*)\.png", climate)[0]
                    climate_list.append(res)


                #  温度
                for temps in table5.xpath('./div[3]//div'):
                    temp_str = temps.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '气温' in temp_str:
                        continue
                    temp_list.append(temp_str.strip('℃'))

                #  降雨量
                for preps in table5.xpath('./div[4]//div'):
                    prep_str = preps.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '降水' == prep_str:
                        continue
                    if '无降水' == prep_str:
                        prep_list.append('0')
                        continue
                    prep_list.append(prep_str.strip('毫米'))

                #  风速
                for w_speeds in table5.xpath('./div[5]//div'):
                    ws_str = w_speeds.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '风速' in ws_str:
                        continue
                    ws_list.append(ws_str.strip('米/秒'))

                #  风向
                for w_dires in table5.xpath('./div[6]//div'):
                    wd_str = w_dires.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if wd_str == '东风':
                        continue
                    if '风向' in wd_str:
                        wd_list.append('E')
                    elif wd_str == '西风':
                        wd_list.append('W')
                    elif wd_str == '南风':
                        wd_list.append('S')
                    elif wd_str == '北风':
                        wd_list.append('N')
                    elif wd_str == '西北风':
                        wd_list.append('NW')
                    elif wd_str == '东北风':
                        wd_list.append('NE')
                    elif wd_str == '西南风':
                        wd_list.append('SW')
                    elif wd_str == '东南风':
                        wd_list.append('SE')

                #  气压
                for air_pres in table5.xpath('./div[7]//div'):
                    air_pre_str = air_pres.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '气压' in air_pre_str:
                        continue
                    air_pres_list.append(air_pre_str)

                #  相对温度
                for relative_hums in table5.xpath('./div[8]//div'):
                    relative_hum_str = relative_hums.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '相对湿度' in relative_hum_str:
                        continue
                    relative_hum_list.append(relative_hum_str.strip('%'))

                #  云量
                for clouds in table5.xpath('./div[9]//div'):
                    cloud_str = clouds.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '云量' in cloud_str:
                        continue
                    cloud_list.append(cloud_str.strip('%'))

                #  能见度
                for visis in table5.xpath('./div[10]//div'):
                    visi_str = visis.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '能见度' in visi_str:
                        continue
                    visi_list.append(visi_str.strip('公里').strip('≥'))

                for i in range(0, len(time_list)):
                    item['name'] = station_name
                    item['time'] = time_list[i]
                    item['temp'] = temp_list[i]
                    item['prep'] = prep_list[i]
                    item['wind_speed'] = ws_list[i]
                    item['wind_dire'] = wd_list[i]
                    item['air_pres'] = air_pres_list[i]
                    item['relative_hum'] = relative_hum_list[i]
                    item['cloud'] = cloud_list[i]
                    item['visibility'] = visi_list[i]
                    yield item
            for table6 in box.xpath('//*[@id="day1"]'):  # 表示today的数据
                climate_url = \
                response.xpath('//*[@id="forecast"]/div[7]/div[1]/table/tbody/tr[2]/td[1]/img/@src').extract()[0]
                climate_code = re.findall(r"/([0-9]*)\.png", climate_url)[0]
                day_climate = \
                response.xpath('//*[@id="forecast"]/div[7]/div[1]/table/tbody/tr[3]/td[1]/text()').extract()[0].encode(
                    'utf-8')

                date = date_day6
                time_list = []
                temp_list = []
                prep_list = []
                climate_list = []
                ws_list = []
                wd_list = []
                air_pres_list = []
                relative_hum_list = []
                cloud_list = []
                visi_list = []
                # 时间
                for times in table6.xpath('./div[1]//div'):
                    time_str = times.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '日' in time_str:
                        date = date_day7
                        time_str = time_str.split('日')[1]  # 遇见'日'字表示到了第二天的时间

                    if '精细' in time_str:
                        continue
                    time_list.append(date + " " + time_str + ":00")

                #  天气现象
                for climates in table6.xpath('./div[2]//div'):
                    if '现象' in climates.xpath('./text()').extract()[0].strip().encode('utf-8'):
                        continue
                    climate = climates.xpath('./img/@src').extract()[0]
                    print("========regregreg======")
                    # print(climate)
                    res = re.findall(r"/([0-9]*)\.png", climate)[0]
                    climate_list.append(res)


                #  温度
                for temps in table6.xpath('./div[3]//div'):
                    temp_str = temps.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '气温' in temp_str:
                        continue
                    temp_list.append(temp_str.strip('℃'))

                #  降雨量
                for preps in table6.xpath('./div[4]//div'):
                    prep_str = preps.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '降水' == prep_str:
                        continue
                    if '无降水' == prep_str:
                        prep_list.append('0')
                        continue
                    prep_list.append(prep_str.strip('毫米'))

                #  风速
                for w_speeds in table6.xpath('./div[5]//div'):
                    ws_str = w_speeds.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '风速' in ws_str:
                        continue
                    ws_list.append(ws_str.strip('米/秒'))

                #  风向
                for w_dires in table6.xpath('./div[6]//div'):
                    wd_str = w_dires.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if wd_str == '东风':
                        continue
                    if '风向' in wd_str:
                        wd_list.append('E')
                    elif wd_str == '西风':
                        wd_list.append('W')
                    elif wd_str == '南风':
                        wd_list.append('S')
                    elif wd_str == '北风':
                        wd_list.append('N')
                    elif wd_str == '西北风':
                        wd_list.append('NW')
                    elif wd_str == '东北风':
                        wd_list.append('NE')
                    elif wd_str == '西南风':
                        wd_list.append('SW')
                    elif wd_str == '东南风':
                        wd_list.append('SE')

                #  气压
                for air_pres in table6.xpath('./div[7]//div'):
                    air_pre_str = air_pres.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '气压' in air_pre_str:
                        continue
                    air_pres_list.append(air_pre_str)

                #  相对温度
                for relative_hums in table6.xpath('./div[8]//div'):
                    relative_hum_str = relative_hums.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '相对湿度' in relative_hum_str:
                        continue
                    relative_hum_list.append(relative_hum_str.strip('%'))

                #  云量
                for clouds in table6.xpath('./div[9]//div'):
                    cloud_str = clouds.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '云量' in cloud_str:
                        continue
                    cloud_list.append(cloud_str.strip('%'))

                #  能见度
                for visis in table6.xpath('./div[10]//div'):
                    visi_str = visis.xpath('./text()').extract()[0].strip().encode('utf-8')
                    if '能见度' in visi_str:
                        continue
                    visi_list.append(visi_str.strip('公里').strip('≥'))

                for i in range(0, len(time_list)):
                    item['name'] = station_name
                    item['time'] = time_list[i]
                    item['temp'] = temp_list[i]
                    item['prep'] = prep_list[i]
                    item['wind_speed'] = ws_list[i]
                    item['wind_dire'] = wd_list[i]
                    item['air_pres'] = air_pres_list[i]
                    item['relative_hum'] = relative_hum_list[i]
                    item['cloud'] = cloud_list[i]
                    item['visibility'] = visi_list[i]
                    yield item
