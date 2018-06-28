from welcome import *
from query_tickets import *
from tickets import *

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

        sb_res = searchWindow(user)
        #
        # order_sec = parse.unquote(datalist[0])
        # from_name = stations.get_name(datalist[6])
        # to_name = stations.get_name(datalist[7])
        # date = datalist[13]
        # timeArray = time.strptime(date, "%Y%m%d")
        # date = time.strftime("%Y-%m-%d", timeArray)
        # # 预订请求
        # sb_res = user.submit(from_name, to_name, order_sec, date)  # 这里datalist容易超时，要做异常判断,改到宋振页面申请
        print(sb_res)
        date = sb_res[-1]
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
        t_file = [date, station_train_code, from_station_name, start_time,
                  to_station_name, arrive_time,
                  users.items(), ticket_num, prices]
        #
        # # # 选票界面
        xieqi_res = confirm_snp(t_file)
        # print(xieqi_res)

        seat = xieqi_res[0]
        name = xieqi_res[1]
        id_num = xieqi_res[3]
        phone = xieqi_res[5]

        user.checkOrderInfo(seat, name, id_num, phone, tk)

        confirm_data = user.getQueueCount(leftTicketStr, station_train_code, from_station, to_station,
                                          train_location, train_no, seat, date, tk)  # 确认订单
        print('余票信息', confirm_data)

        confirm = input('请确认购买')
        if confirm == '1':
            oldPassengerStr = name + ",1," + id_num + ",1_"  # 姓名,1,身份证,1_
            passengerTicketStr = seat + ",0,1," + name + ",1," + id_num + "," + phone + ",N"
            user.confirmSingleForQueue(key_check_isChange, leftTicketStr, oldPassengerStr, passengerTicketStr,
                                       train_location, tk)
        else:
            print('购票失败')
            return

    if choice == -1:
        searchWindow(user=None)


if __name__ == '__main__':
    main()
