import requests
import urllib3
import stations
from threading import Thread, Lock
from PIL import Image
import time
from urllib import parse
import datetime
import re


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TrainCollection(object):
    headers = '车次 车站 时间 历时 商务座 一等座 二等座 高级软卧 软卧 动卧 硬卧 软座 硬座 无座 其他'.split()
    price_temp = (
        'https://kyfw.12306.cn/otn/leftTicket/'
        'queryTicketPrice?train_no={}&'
        'from_station_no={}&'
        'to_station_no={}&'
        'seat_types={}&'
        'train_date={}')

    def __init__(self, raw_trains, options, date):
        self.raw_trains = raw_trains
        self.options = options
        self.date = date
        self.prices = []
        self.train_num = 0

    def get_from_to_station_name(self, data_list):
        from_station_telecode = data_list[6]
        to_station_telecode = data_list[7]
        return "\n".join([stations.get_name(from_station_telecode), stations.get_name(to_station_telecode)])

    def get_start_arrive_time(self, data_list):
        return '\n'.join([data_list[8], data_list[9]])

    def parse_train_data(self, data_list):
        return {
            'sec':data_list[0],
            "station_train_code": data_list[3],
            "from_to_station_name": self.get_from_to_station_name(data_list),
            "start_arrive_time": self.get_start_arrive_time(data_list),
            "lishi": data_list[10],
            "business_class_seat": data_list[32] or '--',
            "first_class_seat": data_list[31] or '--',
            "second_class_seat": data_list[30] or '--',
            "super_soft_sleep": data_list[21] or '--',
            "soft_sleep": data_list[23] or '--',
            "dong_sleep": data_list[33] or '--',
            "hard_sleep": data_list[28] or '--',
            "soft_seat": data_list[24] or '--',
            "hard_seat": data_list[29] or '--',
            "no_seat": data_list[26] or '--',
            "other": data_list[22] or '--'
        }

    def need_print(self, data_list):
        station_train_code = data_list[3]
        initial = station_train_code[0].lower()
        return not self.options or initial in self.options

    @property
    def trains(self):
        # mutex = Lock()
        # def get_price():
        #     price_url = self.price_temp.format(data_list[2], data_list[16], data_list[17], data_list[-2], self.date)
        #     r_p = requests.get(price_url, verify=False)
        #     price = r_p.json()['data']
        #     with mutex:
        #         self.prices.append(price)

        for train in self.raw_trains:
            data_list = train.split('|')
            # print(data_list)
            if self.need_print(data_list):
                # t = Thread(target=get_price)
                # t.start()
                self.train_num += 1
                yield self.parse_train_data(data_list)



    def search_out(self):
        print(self.date)
        result = [self.headers]
        for train in self.trains:
            result.append([
                train['sec'],
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

        # while 1:
        #     if len(self.prices) == self.train_num:
        #         print('查询趟次:', len(self.prices))
        #         return result, self.prices
        print('查询趟次:', len(result)-1)
        # print(result)
        return result


class Search(object):
    url_template = (
        'https://kyfw.12306.cn/otn/leftTicket/query?'
        'leftTicketDTO.train_date={}&'
        'leftTicketDTO.from_station={}&'
        'leftTicketDTO.to_station={}&'
        'purpose_codes=ADULT')

    def __init__(self, from_station, to_station, date, options=None):
        if options is None:
            options = {}
        self.arguments = {'from_station': from_station, 'to_station': to_station}
        self.arguments.update(options)
        self.from_station = stations.get_telecode(self.arguments['from_station'])
        self.to_station = stations.get_telecode(self.arguments['to_station'])
        self.date = date
        self.check_arguments_validity()
        self.options = ''.join([key for key, value in self.arguments.items() if value == 1])

    @property
    def request_url(self):
        return self.url_template.format(self.date, self.from_station, self.to_station)

    def check_arguments_validity(self):
        try:
            if self.from_station is None or self.to_station is None:
                raise ValueError
        except:
            raise ValueError

    def run(self):
        r = requests.get(self.request_url, verify=False)
        trains = r.json()['data']['result']
        self.train = TrainCollection(trains, self.options, self.date)
        return self.train.search_out()



# ****************************************************登录模块******************************************************



class Login(object):

    locate = ['34,39', '107,43', '182,41', '250,40', '34,114', '100,123', '182,109', '251,116']
    header = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False

    def captcha(self):
        captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?' \
                      'login_site=E&module=login&rand=sjrand&0.7069395580950589'
        captcha_img = self.session.get(captcha_url)
        f = open('captcha_img.png', 'wb+')
        f.write(captcha_img.content)
        f.close()
        im = Image.open('captcha_img.png')
        im.show()

    def captcha_check(self, code, username, password):
        answer = ''
        if len(str(code)) == 1:
            answer = self.locate[int(code) - 1]
        else:
            code = code.split(' ')
            for i in code:
                answer += self.locate[int(i) - 1] + ','
            answer = answer[:-1]

        captcha_check_api = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
        payload = {
            'answer': answer,
            'login_site': 'E',
            'rand': 'sjrand'
        }

        check_res = self.session.post(captcha_check_api, payload)
        check_res = check_res.json()
        # print(check_res)
        if check_res['result_code'] != '4':
            print('验证码错误,请重新输入')
            return -1
        else:
            # 用户登录
            login_api = 'https://kyfw.12306.cn/passport/web/login'
            login_data = {
                'username': username,
                'password': password,
                'appid': 'otn',
            }
            print('正在登录中，请稍后...')
            login_res = self.session.post(login_api, headers=self.header, data=login_data)
            # print(login_res.text)
            login_res = login_res.json()
            if login_res['result_code'] != 0:
                print('用户名或密码错误，请重新登录')
                return 0

            else:
                self.verify()

    def verify(self):
        # 第一次验证
        uamtk_url = "https://kyfw.12306.cn/passport/web/auth/uamtk"
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": "https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin",
            "X-Requested-With": "XMLHttpRequest"
        }
        res = self.session.post(uamtk_url, headers=header, data={"appid": "otn"})
        # print(res.text)
        self.apptk = res.json()['newapptk']

        # 第二次验证
        uamauthclient_url = 'https://kyfw.12306.cn/otn/uamauthclient'
        self.session.post(uamauthclient_url, headers = header, data = {'tk': self.apptk})
        # print(res.text)
        print('登录成功')
        return 1

    # 检测当前账号有没有未完成的订单
    def submit(self,from_name, to_name, sec, date):
        # check
        check_url = "https://kyfw.12306.cn/otn/login/checkUser"
        res = self.session.post(check_url, data={"_json_att": ""})
        # print(res.text)
        if not res.json()['data']['flag']:
            print('登录超时，请重新登录')
            self.captcha()
        else:
            print('验证成功，提交预订信息')
            today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            order_url = "https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest"
            payload = {
                "back_train_date": today,
                "purpose_codes": "ADULT",
                "query_from_station_name": from_name,
                "query_to_station_name": to_name,
                "secretStr": sec,
                "tour_flag": "dc",
                "train_date": date,
                "undefined": ""
            }
            res = self.session.post(order_url, data=payload)
            # print('预订',res.text)
            if not res.json()['status']:
                print('预订失败，请完成已经预订的订单或重新预订')
            else:
                print('正在预订，获取订票信息中。。。')
                self.initDc(date)

    def initDc(self,date):
        # 请求订票信息
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        res = self.session.post(url, data={"_json_att": ""}).text
        tk = re.search(r'globalRepeatSubmitToken = \'(.+?)\'',res).group(1)
        leftTicketStr = re.search(r'\'leftTicketStr\':\'(.+?)\'',res).group(1)
        key_check_isChange = re.search(r'\'key_check_isChange\':\'(.+?)\'', res).group(1)

        ZE_num = re.search(r'\'ZE_num\':\'(.+?)\'', res).group(1)  # 二等座
        ZY_num = re.search(r'\'ZY_num\':\'(.+?)\'', res).group(1)  # 一等座
        YZ_num = re.search(r'\'YZ_num\':\'(.+?)\'', res).group(1)  # 硬座票数
        WZ_num = re.search(r'\'WZ_num\':\'(.+?)\'', res).group(1)  # 无座票数

        if not (int(YZ_num) != -1) or (int(ZE_num) != -1):   # 判断是否存在硬座
            print('没票了，10秒后自动刷新')
            self.initDc(date)

        else:
            station_train_code = re.search(r'\'station_train_code\':\'(.+?)\'', res).group(1)  # 车次号
            from_station = re.search(r'\'from_station\':\'(.+?)\'', res).group(1)  # 出发地
            to_station = re.search(r'\'to_station\':\'(.+?)\'', res).group(1)  # 目的地
            train_location = re.search(r'\'train_location\':\'(.+?)\'', res).group(1)
            train_no = re.search(r'\'train_no\':\'(.+?)\'', res).group(1)
            # name, sfz, phone = getPassenger(token, zw)
            users = self.getPassenger(tk)
            for user in users.items():
                print(user)

            self.checkOrderInfo('3', '巫家竞', '500109199203150431', '15702387382',tk)
            name = '巫家竞'
            sfz = '500109199203150431'
            phone = '15702387382'
            zw = '3'

            ticket_data = self.getQueueCount(leftTicketStr, station_train_code, from_station, to_station, train_location, train_no,
                          '3',date,tk)  # 确认订单

            print('余票信息',ticket_data)




            confirm = input('请确认购买')
            if confirm == '1':
                oldPassengerStr = name + ",1," + sfz + ",1_"  # 姓名,1,身份证,1_
                passengerTicketStr = zw + ",0,1," + name + ",1," + sfz + "," + phone + ",N"
                self.confirmSingleForQueue(key_check_isChange,leftTicketStr,oldPassengerStr,passengerTicketStr,train_location,tk)
            else:
                print('购票失败')
                return

    def confirmSingleForQueue(self, key_check_isChange, leftTicketStr, oldPassengerStr, passengerTicketStr, train_location, tk):
        url = "https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue"
        payload = {
            "_json_att": "",
            "choose_seats": "",
            "dwAll": "N",
            "key_check_isChange": key_check_isChange,
            "leftTicketStr": leftTicketStr,
            "oldPassengerStr": oldPassengerStr,
            "passengerTicketStr": passengerTicketStr,
            "purpose_codes": "00",
            "randCode": "",
            "REPEAT_SUBMIT_TOKEN": tk,
            "roomType": "00",
            "seatDetailType": "000",
            "train_location": train_location,
            "whatsSelect": "1"
        }

        msg = self.session.post(url, data=payload)

        if msg.json()['data']['submitStatus']:
            print("提交订单成功，请及时付款")
        else:
            print("提交订单失败，请重新提交")



    def getQueueCount(self, leftTicket, station_train_code, from_station, to_station, train_location, train_no, zw,
                  date,tk):
        url ='https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
        payload = {
            "_json_att": "",
            "fromStationTelecode": from_station,
            "toStationTelecode": to_station,
            "leftTicket": leftTicket,
            "purpose_codes": "00",
            "REPEAT_SUBMIT_TOKEN": tk,
            "seatType": zw,
            "stationTrainCode": station_train_code,
            "train_date": datetime.datetime.fromtimestamp(time.mktime(time.strptime(date, '%Y-%m-%d'))).strftime(
            '%a %b %d %Y %H:%M:%S GMT+0800'),
            "train_location": train_location,
            "train_no": train_no
        }

        res = self.session.post(url, data=payload)
        print(res.text)
        if res.json()['status']:
            return res.json()['data']
        else:
            print('车票信息获取失败')


    def getPassenger(self,tk):
        user_info = {}
        url = "https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs"
        res = self.session.post(url, data={"_json_att": "", "REPEAT_SUBMIT_TOKEN": tk})
        res = res.json()['data']['normal_passengers']
        for info in res:
            id = info['code']  # id
            name = info['passenger_name']  # 姓名
            sex = info['sex_name']  # 性别
            sfz = info['passenger_id_no']  # 身份证
            name_type = info['passenger_type_name']  # 人的类别
            phone = info['mobile_no']  # 电话号码
            user_info[id] = [name, sex, sfz, name_type, phone]

        return user_info

        #显示余票信息、乘客信息



    def checkOrderInfo(self, seat, name, sfz, phone,tk):
        oldPassengerStr = name + ",1," + sfz + ",1_"
        passengerTicketStr = seat + ",0,1," + name + ",1," + sfz + "," + phone + ",N"
        # print(passengerTicketStr)
        url = "https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo"
        payload = {
            "_json_att": "",
            "bed_level_order_num": "000000000000000000000000000000",
            "cancel_flag": 2,
            "oldPassengerStr": oldPassengerStr,
            "passengerTicketStr": passengerTicketStr,
            "randCode": "",
            "REPEAT_SUBMIT_TOKEN": tk,
            "tour_flag": "dc",
            "whatsSelect": "1"
        }
        # print(payload)
        res = self.session.post(url, data=payload)

        if res.json()['data']['submitStatus']:
            print("乘客添加成功，正在返回余票数量。。。")

        else:
            print('乘客信息错误,请重新预订')


def main():

    # login
    username = '@qq.com'
    password = 'user'
    user = Login()
    user.captcha()
    code = input('验证码')
    user.captcha_check(code,username,password)


    # search
    search = Search('重庆', '上海', '2018-07-02')
    result = search.run()
    print(result)
    # # 查询票价
    #
    # # order 选择车次、座位
    order_sec = parse.unquote(result[1][0])
    user.submit(search.arguments['from_station'], search.arguments['to_station'], order_sec, search.date)
    # # 座位类型 1是硬座，2是软座，3是硬卧，4是软卧,'9': '商务座, O是高铁二等座，M是高铁一等座，
    #

if __name__ == '__main__':
    main()

