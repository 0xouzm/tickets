
import requests
import urllib3
from datetime import datetime
import stations


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class TrainCollection(object):
    headers = '车次 车站 时间 历时 商务座 一等座 二等座 高级软卧 软卧 动卧 硬卧 软座 硬座 无座 其他'.split()

    def __init__(self, raw_trains, options):
        self.raw_trains = raw_trains
        self.options = options


    def get_from_to_station_name(self, data_list):
        from_station_telecode = data_list[6]
        to_station_telecode = data_list[7]
        return "\n".join([stations.get_name(from_station_telecode),stations.get_name(to_station_telecode)])

    def get_start_arrive_time(self, data_list):
        return '\n'.join([data_list[8], data_list[9]])


    def parse_train_data(self, data_list):
        return {
            "station_train_code": data_list[3],
            "from_to_station_name": self.get_from_to_station_name(data_list),
            "start_arrive_time": self.get_start_arrive_time(data_list),
            "lishi": data_list[10],
            "business_class_seat":data_list[32] or '--',
            "first_class_seat":data_list[31] or '--',
            "second_class_seat":data_list[30] or '--',
            "super_soft_sleep":data_list[21] or '--',
            "soft_sleep":data_list[23] or '--',
            "dong_sleep":data_list[33] or '--',
            "hard_sleep":data_list[28] or '--',
            "soft_seat":data_list[24] or '--',
            "hard_seat":data_list[29] or '--',
            "no_seat":data_list[26] or '--',
            "other":data_list[22] or '--'
        }

    def need_print(self, data_list):
        station_train_code = data_list[3]
        initial = station_train_code[0].lower()
        return (not self.options or initial in self.options)

    @property
    def trains(self):
        for train in self.raw_trains:
            data_list = train.split('|')
            if self.need_print(data_list):
                yield self.parse_train_data(data_list)

    def pretty_print(self):
        result = [self.headers]
        for train in self.trains:
            result.append([
                train["station_train_code"],
                train["from_to_station_name"],
                train["start_arrive_time"],
                train["lishi"],
                train["business_class_seat"],
                train["first_class_seat"],
                train["second_class_seat"],
                train["super_soft_sleep"],
                train["soft_sleep"],
                train["dong_sleep"],
                train["hard_sleep"],
                train["soft_seat"],
                train["hard_seat"],
                train["no_seat"],
                train["other"]
                ])
        return result

class Cli(object):
    url_template = (
        'https://kyfw.12306.cn/otn/leftTicket/query?'
        'leftTicketDTO.train_date={}&'
        'leftTicketDTO.from_station={}&'
        'leftTicketDTO.to_station={}&'
        'purpose_codes=ADULT')

    def __init__(self,from_station, to_station,date):
        self.arguments = {'from_station':from_station,'to_station':to_station}
        self.from_station = stations.get_telecode(self.arguments['from_station'])
        self.to_station = stations.get_telecode(self.arguments['to_station'])
        self.date = date
        self.check_arguments_validatity()
        self.options = ''.join([key for key, value in self.arguments.items() if value is True ])

    @property
    def request_url(self):
        return self.url_template.format(self.date, self.from_station, self.to_station)

    def check_arguments_validatity(self):
        print(datetime.strptime(self.date, '%Y-%m-%d'))
        try:
            if self.from_station is None or self.to_station is None:
                raise ValueError
            # if datetime.strptime(self.date, '%Y-%m-%d') < datetime.now():
            #     raise ValueError
        except:
            raise ValueError


    def run(self):
        r = requests.get(self.request_url, verify=False)
        trains = r.json()['data']['result']
        return TrainCollection(trains, self.options).pretty_print()
