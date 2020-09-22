from flask import Flask
from flask import request
from WindPy import *
import json

app = Flask(__name__)
prompt = 'API_group'


def get_info_data_from_wind(test_resource):
    test_data = test_resource.Data
    test_codes = test_resource.Codes
    test_fields = test_resource.Fields
    test_row = 0
    if len(test_data) != 0:
        test_row = len(test_data[0])

    res_data = []

    for i in range(test_row):
        dict = {
            "code": test_codes[i]
        }

        for idx_field in range(len(test_fields)):
            field = test_fields[idx_field]
            dict[field] = test_data[idx_field][i]

        dict['first_tradedate'] = dict['first_tradedate'].strftime('%Y-%m-%d')
        dict['last_tradedate'] = dict['last_tradedate'].strftime('%Y-%m-%d')
        dict['curr_status'] = None
        res_data.append(dict)

    return res_data


def get_status_data_from_wind(test_resource):
    test_data = test_resource.Data
    test_codes = test_resource.Codes
    test_fields = test_resource.Fields
    test_dict = {}
    test_row = 0
    if len(test_data) != 0:
        test_row = len(test_data[0])
    test_column = 7

    res_data = {}

    for i in range(test_row):
        dict = {}

        for idx_field in range(len(test_fields)):
            field = test_fields[idx_field]
            dict[field] = test_data[idx_field][i]

        res_data[test_codes[i]] = dict

    return res_data


## 510050.SH
def get_info(date_str, us_code):
    info_res = w.wset("optionchain",
                      "date=" + date_str +
                      ";us_code=" + us_code +
                      ";option_var=全部;call_put=全部")

    if info_res.ErrorCode != 0:
        return None

    info_res = get_info_data_from_wind(info_res)
    query_list = []
    for r in info_res:
        query_list.append(r['option_code'])
    query_str = ','.join(query_list)
    return {
        'query_str': query_str,
        'query_info': info_res,
        'query_list': query_list
    }


def get_status(query_str):
    status_res = w.wsq(query_str, "rt_ask1,rt_ask2,rt_last_amt,rt_conv_price,rt_last,rt_ustock_price,rt_delta")
    if status_res.ErrorCode != 0:
        return None
    status_res = get_status_data_from_wind(status_res)
    return {
        'status_res': status_res
    }


def val_to_return(succeed, data):
    res = {
        'success': succeed,
        'data': data
    }
    return json.dumps(res, ensure_ascii=False)


@app.route('/')
def hello_Wind():
    return val_to_return(True, {
        "Welcome": "/"
    })


@app.route('/loginWind', methods=['GET'])
def login():
    w.start()
    return val_to_return(w.isconnected(), None)


@app.route('/logoutWind', methods=['GET'])
def logout():
    w.stop()
    return val_to_return(not w.isconnected(), None)


# 获取列表的。一天执行一次
# 格式 2019-01-20
## 510050.SH
@app.route('/getList/<string:us_code>/<string:date>', methods=['GET'])
def getList(date, us_code):
    w.start()
    print("getList")
    info_dict = get_info(date, us_code=us_code)  # 注意，不管什么问题，一定要返回，就算是返回None
    w.stop()
    if info_dict is None:
        return val_to_return(False, None)
    return val_to_return(True, info_dict)


@app.route('/getOptions/<string:query_str>', methods=['GET'])
def getOptions(query_str):
    w.start()
    status_dict = get_status(query_str)
    w.stop()
    if status_dict is None:
        return val_to_return(False, None)
    return val_to_return(True, status_dict)


# 没用的，仅作格式之用
@app.route('/doTrade', methods=['POST'])
def doTrade():
    param_dict = request.form
    # TODO 参数设定
    # TODO 使用Wind代码生成器，生成代码，进行交易

    return


# Author: zjy
# 登录接口
@app.route('/trade/tlogon', methods=['POST'])
def trade_logon():
    param_dict = json.loads(request.get_data(as_text=True))

    brokerId = param_dict.get('brokerId', None)
    departmentId = param_dict.get('departmentId', None)
    logonAccount = param_dict.get('logonAccount', None)
    password = param_dict.get('password', None)
    accountType = param_dict.get('accountType', {})

    if brokerId is None or departmentId is None or logonAccount is None or password is None:
        return val_to_return(False, prompt + ": info not valid")

    # 登录交易账号
    LogonID = w.tlogon(brokerId, departmentId, logonAccount, password, accountType)

    if LogonID.ErrorCode == 0:
        return val_to_return(True, LogonID.Data[0])
    else:
        return val_to_return(False, LogonID.Data)


# 交易登出接口
@app.route('/trade/tlogout', methods=['POST'])
def trade_logout():
    param_dict = json.loads(request.get_data(as_text=True))
    logonId = param_dict.get('logonId', 0)
    Logout = w.tlogout(LogonID=logonId)
    if Logout.ErrorCode == 0:
        return val_to_return(True, prompt + ': logout succeed')
    else:
        return val_to_return(False, Logout.Data[2])


# 交易委托下单接口
@app.route('/trade/torder', methods=['POST'])
def trade_order():
    param_dict = json.loads(request.get_data(as_text=True))
    securityCode = param_dict.get('securityCode', None)
    tradeSide = param_dict.get('tradeSide', None)
    orderPrice = param_dict.get('orderPrice', None)
    orderVolume = param_dict.get('orderVolume', None)

    if not (securityCode and tradeSide and orderPrice and orderVolume):
        return val_to_return(False, prompt + ": info not valid")

    options = param_dict.get('options', {})
    options_list = []
    options_str = ''
    for option_key in options.keys():
        options_list.append(option_key + '=' + options.get(option_key))
    options_str = ';'.join(options_list)

    print(param_dict)
    if options == '':
        OrderStatus = w.torder(SecurityCode=securityCode, TradeSide=tradeSide,
                               OrderPrice=orderPrice, OrderVolume=orderVolume)
    else:
        OrderStatus = w.torder(SecurityCode=securityCode, TradeSide=tradeSide,
                               OrderPrice=orderPrice, OrderVolume=orderVolume, options=options_str)

    if OrderStatus.ErrorCode == 0:
        # return val_to_return(True, OrderStatus.Data)
        return val_to_return(True, param_dict)
    else:
        # return val_to_return(False, OrderStatus.Data[8])
        return val_to_return(False, param_dict)


# 交易撤销委托函数
@app.route('/trade/tcancel', methods=['POST'])
def tcancel():
    param_dict = json.loads(request.get_data(as_text=True))
    OrderNumber = param_dict.get('OrderNumber', None)
    MarketType = param_dict.get('MarketType', None)
    LogonID = param_dict.get('LogonID', None)

    if not (OrderNumber):
        return val_to_return(False, prompt + ": info not valid")

    options = param_dict.get('options', {})
    options_list = []
    options_str = ''
    for option_key in options.keys():
        options_list.append(option_key + '=' + options.get(option_key))
    options_str = ';'.join(options_list)

    if options == '':
        OrderStatus = w.tcancel(OrderNumber=OrderNumber, options=None)
    else:
        OrderStatus = w.tcancel(OrderNumber=OrderNumber, options=options_str)

    if OrderStatus.ErrorCode == 0:
        return val_to_return(True, OrderStatus.Data)
    else:
        return val_to_return(False, OrderStatus.Data[3])


# 交易情况查询函数
@app.route('/trade/tquery', methods=['POST'])
def tquery():
    param_dict = json.loads(request.get_data(as_text=True))
    queryType = param_dict.get('queryType', None)
    LogonID = param_dict.get('LogonID', None)
    RequestID = param_dict.get('LogonID', None)
    OrderNumber = param_dict.get('OrderNumber', None)
    MarketType = param_dict.get('MarketType', None)
    OrderType = param_dict.get('OrderType', None)
    WindCode = param_dict.get('WindCode', None)

    if not (queryType):
        return val_to_return(False, prompt + ": info not valid")

    options = param_dict.get('options', {})
    options_list = []
    options_str = ''
    for option_key in options.keys():
        options_list.append(option_key + '=' + options.get(option_key))
    options_str = ';'.join(options_list)

    if options == '':
        OrderStatus = w.tquery(qrycode=queryType, options=None)
    else:
        OrderStatus = w.tquery(qrycode=queryType, options=options_str)

    if OrderStatus.ErrorCode == 0:
        return val_to_return(True, OrderStatus.Data)
    else:
        return val_to_return(False, None)  # 没看到错误msg在哪里


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # w.start()
