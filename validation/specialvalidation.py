import operator
from ncsqa import qadatabasemssql
from ncsqa import qadatabase
from validation import comvalidation as com
from qaconfig import DataConstant as dc
from qaconfig import TestCases as tc
import os
import time
import jsonpath
from qalogger import log

logging = log()

mongodb = qadatabase.MongoDB()

db = qadatabasemssql.MSSQL()


def raise_error(error_msg):
    raise AssertionError(error_msg)


def special_validation(case_id, case_type, response, expected_response, validation_query, expected_validation_result):
    if case_type in ("response_valid",):
        validate_search(response, validation_query)
    elif case_type in ("response_invalid",):
        validate_errorapiresponse(response, expected_response)
    elif case_type in ('CreateItem', 'UpdateItem'):
        validate_create_record(eval(validation_query))
    elif case_type in ('serach_sch', 'serach_group'):
        validate_search_values(response, expected_response, validation_query)
    elif case_type in ('add_device', "delete_device", 'delete_sch', 'add_group', 'update_group', 'add_group_mapping',
                       'update_group_mapping', 'assgin_channel', 'save_sch'):
        validate_add_or_update_or_delete(response, expected_response, validation_query, expected_validation_result)
    elif case_type in ('search_paging', 'serach_errorStatus_group'):
        validate_psize(response, expected_response, expected_validation_result)
    elif case_type in ('download',):
        validate_file_download(case_id, response)
    elif case_type in ("common_validate",):
        validate_common_expected_response(response, expected_response)
    elif "search" in case_type:
        validate_search_key_filed(case_type, response, expected_response, validation_query)
    elif case_type in ("vms_device",):
        validate_vms_device(case_type, validation_query, expected_validation_result)


def validate_search(response, validation_query):

    # prepare the response content list as actual result:
    if "data" in response.responsejson:
        # if "content" in response.responsejson['data']:
        res_detail = response.responsejson["data"]
        act_detail = list(res_detail[0].values())
    else:
        raise_error("no content data field in response")
    # Prepare the query result from DB as expected result:
    exp_result = db.fetch_one(validation_query)
    exp_result_lst = list(exp_result)
    exp_result_lst[2] = str(exp_result[2])
    err_str = ''
    for i in range(len(act_detail)):
        if act_detail[i] != exp_result_lst[i]:
             err_str = "content not match on item No. %s" %i
             err_no = i
    if len(err_str) > 0:
        print("should be %s, but is %s" % (exp_result_lst[err_no], act_detail[err_no]))

        raise_error(err_str)


def validate_errorapiresponse(response,expected_response):
    # prepare the response content list as actual result:
    # compare the keys:
    act_key_list = list(response.responsejson.keys())
    exp_key_list = list(eval(expected_response).keys())
    for i in range(len(exp_key_list)):
        if exp_key_list[i] != act_key_list[i]:
            err_str = "content not match on item No. %s" % i
            err_no = i

    if len(err_str) > 0:
        print("item No.%s should be %s, but is %s" % (err_no, exp_key_list[err_no], act_key_list[err_no]))
        raise_error(err_str)


def validate_create_record(query):
    db.fetch_one(query)
    logging.info("*****DB record created successfully!********")


def validate_search_values(response, expected_response, validation_query):
    """Verify that the data field values returned by the interface are the same as those that exist in the database"""
    res_detail = response.responsejson
    actual_response_data = res_detail.pop("data")
    data_result_list_response = []
    for item in actual_response_data:
        update_item = {"createdDate": com.validate_time(item["createdDate"]),
                       "lastUpdatedDate": com.validate_time(item["lastUpdatedDate"])}
        item.update(update_item)
        feature = tuple(item.values())
        data_result_list_response.append(feature)

    if operator.ne(res_detail, eval(expected_response)):
        raise AssertionError(
            "validate_get_feature validation for message is fail, the expected result is %s, but the actual result is "
            "%s" % (expected_response, str(res_detail)))

    if validation_query:
        data_result_list_database = db.fetch_all(validation_query)
        print(data_result_list_database)
        if operator.ne(data_result_list_response, data_result_list_database):
            raise AssertionError("validate_get_feature validation for data is fail, the expected result is %s, but the "
                                 "actual result is %s" % (data_result_list_database, str(data_result_list_response)))


def validate_add_or_update_or_delete(response, expected_response, validation_query, expected_validation_result):
    """ verify that the interface return is consistent with the DB query after adding, modifying, or deleting,"""
    if not expected_response and response.responsejson:
        raise AssertionError("validate_add_or_update_or_delete validation for message is fail, the expected response "
                             "message is blank, but the actual response is %s" % response.responsejson)
    elif expected_response:
        if operator.ne(response.responsejson, eval(expected_response)):
            raise AssertionError("validate_add_or_update_or_delete validation for message is fail, the expected result "
                                 "is %s, but the actual result is %s" % (expected_response, str(response.responsejson)))

    if validation_query:
        time.sleep(4)  # 防止数据请求过后数据查询在同步之,
        data_result_database = db.fetch_all(validation_query)
        if len(data_result_database) != int(expected_validation_result):
            raise AssertionError("validate_add_or_update_or_delete validation for data is fail, the data saved in the "
                                 "database is not as per expected")


def validate_psize(response, expected_response, expected_validation_result):
    """Verify the number of data bars returned by the interface"""
    res_detail = response.responsejson
    data = res_detail.pop("data")
    if not expected_response and response.responsejson:
        raise AssertionError("validate_psize validation for message is fail, the expected response "
                             "message is blank, but the actual response is %s" % res_detail)
    elif expected_response:
        if operator.ne(res_detail, eval(expected_response)):
            raise AssertionError("validate_psize validation for message is fail, the expected result "
                                 "is %s, but the actual result is %s" % (expected_response, str(res_detail)))
            # if "content" in response.responsejson['data']:

    if len(data) != int(expected_validation_result):
        raise AssertionError("validate_psize validation for data is fail, the expected psize " 
                             "is %s, but the actual psize is %s" % (int(expected_validation_result), len(data)))


def validate_file_download(case_id, response):
    new_file = case_id + ".xlsx"
    download_file_path = os.path.join(tc.PROJECT_DIR, "data", "download")
    # 1. save the download file
    with open(os.path.join(download_file_path, new_file), "wb+") as act_file:
        act_file.write(response.responsecontent)
        act_file.close()


def validate_common_expected_response(response, expected_response):
    """Verify the number of data bars returned by the interface"""
    res_detail = response.responsejson
    if "data" in response.responsejson:
        res_detail.pop("data")
    if not expected_response and response.responsejson:
        raise AssertionError("validate_psize validation for message is fail, the expected response "
                             "message is blank, but the actual response is %s" % res_detail)
    elif expected_response:
        if operator.ne(res_detail, eval(expected_response)):
            raise AssertionError("validate_psize validation for message is fail, the expected result "
                                 "is %s, but the actual result is %s" % (expected_response, str(res_detail)))


def validate_search_key_filed(case_type, response, expected_response, validation_query):
    if case_type.find("search") >= 0:
        search_filed = case_type[case_type.find("["):]
        search_filed_combine = "$.." + search_filed
        res_detail = response.responsejson
        if jsonpath.jsonpath(res_detail, search_filed_combine):
            key_filed_value = jsonpath.jsonpath(res_detail, search_filed_combine)
        else:
            key_filed_value =[]
        validate_key_filed_value = []
        temp = search_filed_combine.count(",") + 1
        for index in range(int(len(key_filed_value) / temp)):
            hh = tuple(key_filed_value[index * temp:(index + 1) * temp])
            validate_key_filed_value.append(hh)
        res_detail.pop("data")
        if operator.ne(res_detail, eval(expected_response)):
            raise AssertionError(
                 "validate_get_feature validation for message is fail, the expected result is %s, but the actual result is "
                 "%s" % (expected_response, str(res_detail)))

        if validation_query:
            data_result_list_database = db.fetch_all(validation_query)
            if operator.ne(validate_key_filed_value, data_result_list_database):
                raise AssertionError("validate_get_feature validation for data is fail, the expected result is %s, but the actual result is "
                                     "%s" % (data_result_list_database, str(validate_key_filed_value)))


def validate_vms_device(case_type, validation_query, expected_validation_result):
    vms_device_data_num = mongodb.find_all_num("vms-ds", "Device", eval(validation_query))
    if vms_device_data_num != int(expected_validation_result):
        mongodb.delete("vms-ds", "Device", eval(validation_query))
        raise AssertionError("validate vms device for data is failed, the expected result "
                             "is %s, but the actual result is %s" % (int(expected_validation_result), vms_device_data_num))






# def validate_add_or_update_or_delete(response, expected_response, validation_query, expected_validation_result):
#
#     if not expected_response and response.responsejson:
#         raise AssertionError("validate_add_or_update_or_delete validation for message is fail, the expected response message is blank, but the actual response is %s" % (response.responsejson))
#     elif expected_response:
#         if operator.ne(response.responsejson, eval(expected_response)):
#             raise AssertionError("validate_add_or_update_or_delete validation for message is fail, the expected result is %s, but the actual result is %s" % (expected_response, str(response.responsejson)))
#
#     if validation_query:
#         data_result_database = db.fetch_all(validation_query)
#
#         if len(data_result_database) != int(expected_validation_result):
#             raise AssertionError("validate_add_or_update_or_delete validation for data is fail, the data saved in the database is not as per expected")
#
#
# # To test the login api function
# def special_validation_login(case_type, response, expected_response, request_param,validation_query):
#     time.sleep(0.1)
#     if case_type in ("system_login", "ladp_login"):
#         validate_login_function_normal(case_type, response, expected_response, request_param, validation_query)
#     elif case_type in ("system_login_miss", "system_login_wronginfo", "ladp_login_miss", "ladp_login_wronginfo"):
#         validate_login_function_abnormal(case_type, response, expected_response, request_param)
#     elif case_type in ("system_logout", "system_logout_miss", "system_logout_incorrect"):
#         validate_logout_function_normal(response, expected_response)
#
#
# # Login API user info test
# def validate_login_function_normal(case_type, response, expected_response, request_param, validation_query):
#     api_response_result = json.loads(response.responsetext)
#     new_request_param = eval(request_param).get("json-data") if request_param else None
#     new_expected_response = eval(expected_response) if expected_response else None
#     token = api_response_result["data"]["access_token"]   # Now token is a dic
#     api_user_info = api_response_result["data"]["user_info"]
#     api_code = api_response_result["data"]["code"]
#     username = api_response_result["data"]["user_info"]["userName"]
#     db_find_result = db.exec_query_num(validation_query)
#
#     if token is None:
#         raise AssertionError(
#             "Special validation[validate_%s] case is fail !! The token %s is empty. " % (case_type, token))
#
#     if username != new_request_param['username']:
#         raise AssertionError(
#             "Special validation[validate_%s] case is fail !! The username %s is not match request username %s. " %
#             (case_type, username, new_request_param['username']))
#
#     if db_find_result == 0:
#         raise AssertionError(
#             "Special validation[validate_%s] case is fail !! The result in Database is empty. " % case_type)
#     else:
#         print("The search results num in database is: ", db_find_result)
#
#     if operator.ne(api_code, new_expected_response['code']):
#         raise AssertionError("Special validation fot get code info is fail !!" +
#                              "The expected response is %s, but actual response is %s" %
#                              (new_expected_response['code'], api_code))
#     else:
#         print("API Code info: ", api_code)
#
#     if operator.ne(api_user_info, new_expected_response['user_info']):
#         raise AssertionError("Special validation fot get user info is fail !!" +
#                              "The expected response is %s, but actual response is %s" %
#                              (new_expected_response['user_info'], api_user_info))
#     else:
#         print("API user Login info: ", api_user_info)
#
#
# # Enter data miss testing
# def validate_login_function_abnormal(case_type, response, expected_response, request_param):
#     api_response_result = json.loads(response.responsetext)
#     new_request_param = eval(request_param).get("json-data") if request_param else None
#     new_expected_response = eval(expected_response) if expected_response else None
#     for value in new_request_param:
#         if new_request_param[value] == '':
#             print("The case %s request param value %s is miss." % (case_type, new_request_param[value]))
#
#     if operator.ne(api_response_result, new_expected_response):
#         raise AssertionError("Special validation fot user login is fail !!" +
#                              "The expected response is %s, but actual response is %s" %
#                              (new_expected_response, api_response_result))
#
#
# # User logout test
# def validate_logout_function_normal(response, expected_response):
#     api_response_result = json.loads(response.responsetext)
#     new_expected_response = eval(expected_response) if expected_response else None
#     if operator.ne(api_response_result, new_expected_response):
#         raise AssertionError("Special validation fot user logout is fail !!" +
#                              "The expected response is %s, but actual response is %s" %
#                              (new_expected_response, api_response_result))
#
#
#
