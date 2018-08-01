from welcome import *
from query_tickets import *
from buy_info import *
from book_tickets import *


# 985061107@qq.com
# m674930977

def choice_1():
    YanZheng()
    user = login_ret()
    if user == 0:
        return
    sb_res = bookWindow(user)
    # order_sec = parse.unquote(datalist[0])
    # from_name = stations.get_name(datalist[6])
    # to_name = stations.get_name(datalist[7])
    # date = datalist[13]
    # timeArray = time.strptime(date, "%Y%m%d")
    # date = time.strftime("%Y-%m-%d", timeArray)
    # # 预订请求
    # sb_res = user.submit(from_name, to_name, order_sec, date)  # 这里datalist容易超时，要做异常判断,改到宋振页面申请
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
    t_file = [date, station_train_code, from_station_name, start_time, to_station_name, arrive_time, users.items(),
              ticket_num, prices]
    # 选票界面
    xieqi_res = confirm_snp(t_file)
    if xieqi_res == 0:
        return
    print(xieqi_res)
    seat = xieqi_res[0]
    name = xieqi_res[1]
    id_num = xieqi_res[3]
    phone = xieqi_res[5]

    user.checkOrderInfo(seat, name, id_num, phone, tk)

    confirm_data = user.getQueueCount(leftTicketStr, station_train_code, from_station, to_station, train_location,
                                      train_no, seat, date, tk)  # 确认订单
    print('余票信息', confirm_data)

    oldPassengerStr = name + ",1," + id_num + ",1_"
    passengerTicketStr = seat + ",0,1," + name + ",1," + id_num + "," + phone + ",N"
    comfirm_ret = user.confirmSingleForQueue(key_check_isChange, leftTicketStr, oldPassengerStr, passengerTicketStr,
                               train_location, tk)

    print(comfirm_ret)


def main():
    choice = DengLu()
    if choice == 1:
        choice_1()

    if choice == -1:
        ret = searchWindow(user=None)
        if ret == 0:
            return
        else:
            choice_1()


if __name__ == '__main__':
    main()
