from welcome import *
from query_tickets import *
from tickets import *
from urllib import parse
from buy_info import *


# "yz_num": "1",  # 硬座
# "rz_num": "2",  # 软座
# "yw_num": "3",  # 硬卧
# "rw_num": "4",  # 软卧
# "gr_num": "6",  # 高级软卧
# "tz_num": "P",  # 特等座
# "wz_num": "WZ",  # 无座
# "ze_num": "O",  # 二等座
# "zy_num": "M",  # 一等座
# "swz_num": "9",  # 商务座
#  gg_num;
#  yb_num;
#  qt_num;


def main():
    choice = DengLu()

    if choice == 1:
        user = YanZheng()

        # datalist = songzhen_window()
        datalist = [
            'qWahoOiH9Lqi%2FpPiqn160sVPrt78HtGdPtpC9ROeXfFm22k%2F3rVuVz90cWom1lfQoRRUOoUxIj5Z%0AFCcLmNKaSb96KgJcDj2Go0v8W7WynB06ESnJPtWC3hMpNrDjTYNp7IH5IDjU0HbQ%2F5NHeiwRpe5n%0Aaxhlt%2BedmbAN72%2BFFgSFs6yvcvzsrPqgBF%2FCiA9aeONgi5vzZ1S4783ypmIhiVnbliLYHh7y4GQH%0Ap%2FZtA9f2JrG7XSW16nkRSkXgah2R',
            '预订', '77000G852208', 'G8522', 'CUW', 'ICW', 'CUW', 'ICW', '21:59', '23:34', '01:35', 'Y',
            'lX89Fb0cCZF9Hn59kvBAzILmnrecjTD8t0XwJydsTrXNACFk', '20180702', '3', 'W1', '01', '03', '0', '0', '', '', '',
            '', '', '', '', '', '', '', '有', '有', '15', '', 'O0M090', 'OM9', '0']
        order_sec = parse.unquote(datalist[0])
        from_name = stations.get_name(datalist[6])
        to_name = stations.get_name(datalist[7])
        date = datalist[13]
        timeArray = time.strptime(date, "%Y%m%d")
        date = time.strftime("%Y-%m-%d", timeArray)
        # 预订请求
        sb_res = user.submit(from_name, to_name, order_sec, date)  # 这里datalist容易超时，要做异常判断,改到宋振页面申请
        print(sb_res)

        station_train_code = sb_res[0]
        from_station_name = sb_res[1]
        start_time = sb_res[2]
        to_station_name = sb_res[3]
        arrive_time = sb_res[4]
        ticket_num = sb_res[5]
        prices = sb_res[6]
        users = sb_res[7]
        tk = sb_res[8]
        leftTicketStr = sb_res[9]
        from_station = sb_res[10]
        to_station = sb_res[11]
        train_location = sb_res[12]
        train_no = sb_res[13]
        key_check_isChange = sb_res[14]
        #
        xieqi_file = [date, station_train_code, from_station_name, start_time,
                      to_station_name, arrive_time,
                      users.items(), ticket_num, prices]
        print('xieqi:', xieqi_file)
        # # 选票界面
        # # xieqi_res = confirm_snp(xieqi_file)
        #
        seat = 'M'
        name = ''
        id_num = ''
        phone = ''
        #
        user.checkOrderInfo(seat, name, id_num, phone, tk)

        confirm_data = user.getQueueCount(leftTicketStr, station_train_code, from_station, to_station,
                                          train_location, train_no, seat, date, tk)  # 确认订单
        print('余票信息', confirm_data)
        #
        # confirm = input('请确认购买')
        # if confirm == '1':
        #     oldPassengerStr = name + ",1," + id_num + ",1_"  # 姓名,1,身份证,1_
        #     passengerTicketStr = seat + ",0,1," + name + ",1," + id_num + "," + phone + ",N"
        #     user.confirmSingleForQueue(key_check_isChange, leftTicketStr, oldPassengerStr, passengerTicketStr,
        #                                train_location, tk)
        # else:
        #     print('购票失败')
        #     return

    if choice == -1:
        sw_res = searchWindow()


if __name__ == '__main__':
    main()
