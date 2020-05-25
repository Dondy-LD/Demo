import datetime


def common_validation(response, expectedstatuscd, expected_response):
    if response.httpstatuscd != int(expectedstatuscd):
        raise AssertionError("Common validation is fail, the expected result g is %s, but the actual result g is %s" % (
        (int(expectedstatuscd)), response.httpstatuscd))
    elif len(expected_response) != 0:
        post_status = response.responsejson.get("status")
        expected_response_status = int(eval(expected_response).get("status"))
        if post_status != expected_response_status:
            raise AssertionError("Common validation is fail, the expected status is %s, but the actual status is %s"
                                 % (expected_response_status, post_status))


def validate_time(utc_base):
    """将响应中的数据转化为UTC时间后返回其时间戳"""
    temp = utc_base.replace('T', ' ')
    sql_time = temp[0:temp.rfind('+', 1)]
    sql_timestamp = datetime.datetime.strptime(sql_time, "%Y-%m-%d %H:%M:%S.%f")
    now_stamp = sql_timestamp.timestamp()
    local_time = datetime.datetime.fromtimestamp(now_stamp).timestamp()
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp).timestamp()
    offset = local_time - utc_time

    new_timestamp = int((now_stamp + offset))

    return new_timestamp