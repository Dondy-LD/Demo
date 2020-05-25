from ncsqa import qadatabasemssql
from qaconfig import TestCases as qtc
from qalogger import log
from ncsqa import qadatabase
import traceback
import jsonpath


# Replace the parameters of the testcase table
def update_testdata_for_data_preparation(datac, case_id, response, field_value, datapath):
    pendingupdate = []
    case_id_list = []
    if case_id.find("[") >= 0:
        case_id_list = eval(case_id)
    else:
        case_id_list.append(case_id)

    for key, value in field_value.items():
        for case_id in case_id_list:
            rowindex, colindex = datac.get_index_by_row_column_value(case_id, key)
            olddata = eval(datac.table.cell(rowindex, colindex).value)
            for k, v in value.items():
                if k in olddata.keys():
                    temp = "$.." + k[1:-1]
                    if jsonpath.jsonpath(response, temp):
                        olddata[k] = jsonpath.jsonpath(response, temp)[0]
                    else:
                        olddata[k] = ''
                elif k.split("->")[1] in olddata.keys():
                    for k1 in olddata.keys():   # 解决字段名字不一样的替换
                        if k.find(k1):
                            temp1 = k.split("->")[0]
                            temp = "$.." + temp1[1:-1]
                            if jsonpath.jsonpath(response, temp):
                                olddata[k1] = jsonpath.jsonpath(response, temp)[0]
                            else:
                                olddata[k1] = ''
                else:
                    continue
                newdata = (rowindex, colindex, olddata)
                pendingupdate.append(newdata)
    datac.update_value_to_excel(pendingupdate, datapath)


def update_testdata_for_data_teardown(datac, case_id, response, field_value, datapath):
    pendingupdate = []
    for key, value in field_value.items():
        rowindex, colindex = datac.get_index_by_row_column_value(case_id, key)
        olddata = eval(datac.table.cell(rowindex, colindex).value)
        for k, v in value.items():
            if k in olddata.keys():
                temp = "$.." + k[1:-1]
                if jsonpath.jsonpath(response, temp):
                    olddata[k] = jsonpath.jsonpath(response, temp)[0]
                else:
                    olddata[k] = ''
            else:
                continue
            newdata = (rowindex, colindex, olddata)
            pendingupdate.append(newdata)
    datac.update_value_to_excel(pendingupdate, datapath)


# def update_testdata_for_data_preparation(datac, case_id, response, field_value, datapath):
#     """Replace the parameters of the device_service table"""
#     pendingupdate = []
#     case_id_list = []
#     if case_id.find("[") >= 0:
#         case_id_list = eval(case_id)
#     else:
#         case_id_list.append(case_id)
#
#     for key, value in field_value.items():  # key: swapper , value : {"{channelId}": {"{channelId}":{"data":["channelId"]}[dict]
#         for case_id in case_id_list:
#             rowindex, colindex = datac.get_index_by_row_column_value(case_id, key)
#             olddata = eval(datac.table.cell(rowindex, colindex).value)
#             if isinstance(value.items(), str):
#                 new_value = response
#             for k, v in value.items():
#                 if isinstance(v, str):
#                     new_value = response[v]
#                 elif isinstance(v, dict):
#                     for k_l2, v_l2 in v.items():
#                         response_l2 = response[k_l2]
#                         if isinstance(v_l2, str):
#                             new_value = v[v_l2]
#                         elif isinstance(v_l2, list) and isinstance(response_l2, dict) :
#                             v_13 = v_l2[0]
#                             if isinstance(v_13, str):
#                                 new_value = response_l2[v_13]
#                         elif isinstance(v_l2, list) and isinstance(response_l2, list) :
#                             response_l3 = response_l2[0]
#                             v_13 = v_l2[0]
#                             if isinstance(v_13, str):
#                                 new_value = response_l3[v_13]
#                             elif isinstance(v_13, dict):
#                                 for k_l4, v_l4 in v_13.items():
#                                     if isinstance(v_l4,str):
#                                         new_value = response_l3[v_l4]
#                 olddata[k] = new_value
#             newdata = (rowindex, colindex, olddata)
#             pendingupdate.append(newdata)
#
#     print(pendingupdate)
#     datac.update_value_to_excel(pendingupdate, datapath)


# def update_predata_for_data_preparation(datac, request_url, response, field_value, datapath):
#     """Replace the parameters of the precondition table"""
#     pendingupdate = []
#     # case_id_list = []
#     # if case_id.find("[") >= 0:
#     #     case_id_list = eval(case_id)
#     # else:
#     #     case_id_list.append(case_id)
#     request_url_list =qtc.Replace_URL
#     if field_value:
#         for key, value in field_value.items():  # key: swapper , value : {"{channelId}": {"{channelId}":{"data":["channelId"]}[dict]
#             # rowindex, colindex = datac.get_index_by_row_column_value(case_id, key)
#             colval, colindex =datac.get_calval_by_col_value(key)
#             rowindex = datac.get_index_by_row_value(request_url)
#             for i  in range(1, len(request_url_list)-request_url_list.index(request_url)):
#                 olddata = eval(datac.table.cell(rowindex+i, colindex).value)
#                 if isinstance(value.items(), str):
#                     new_value = response
#                 for k, v in value.items():
#                     if isinstance(v, str):
#                         new_value = response[v]
#                     elif isinstance(v, dict):
#                         for k_l2, v_l2 in v.items():
#                             response_l2 = response[k_l2]
#                             if isinstance(v_l2, str):
#                                 new_value = v[v_l2]
#                             elif isinstance(v_l2, list) and isinstance(response_l2, dict) :
#                                 v_13 = v_l2[0]
#                                 if isinstance(v_13, str):
#                                     new_value = response_l2[v_13]
#                             elif isinstance(v_l2, list) and isinstance(response_l2, list) :
#                                 response_l3 = response_l2[0]
#                                 v_13 = v_l2[0]
#                                 if isinstance(v_13, str):
#                                     new_value = response_l3[v_13]
#                                 elif isinstance(v_13, dict):
#                                     for k_l4, v_l4 in v_13.items():
#                                         if isinstance(v_l4,str):
#                                             new_value = response_l3[v_l4]
#                     olddata[k] = new_value
#                 newdata = (rowindex+i, colindex, olddata)
#                 pendingupdate.append(newdata)
#
#         print(pendingupdate)
#         datac.update_value_to_excel(pendingupdate, datapath)
#
#     log().logging.info(" The request_url %s |field_value is empty" % request_url)


def exec_SQL_script(db_type, query):
    # config DB connection
    if db_type == 'mssql':
        try:
            db = qadatabasemssql.MSSQL()
            db.execute_query(query)
        except:
            traceback.print_exc()
            raise
        finally:
            db.conn.close()

    elif db_type == 'MongoDB':
        pass
        # try:
        #     mongodb = qadatabase.MongoDB()  # db = qadatabase.MongoDB(dc.db_host, dc.db_port, dc.db_name)
        #     mongodb.e
        # except:
        #     traceback.print_exc()
        # finally:
        #     mongodb.client.close()


def excute_sql_and_replace(db_type, query, datac, case_id, swapper, datapath):
    # config DB connection
    if db_type == 'mssql':
        try:
            pendingupdate = []
            db = qadatabasemssql.MSSQL()
            db_result = db.fetch_one(query)
            m = 0
            for k in swapper.keys():
                swapper[k] = db_result[m]
                m += 1
                if m == len(db_result):
                    break
            rowindex, colindex = datac.get_index_by_row_column_value(case_id, "swapper")
            new_swapper = (rowindex, colindex, swapper)
            pendingupdate.append(new_swapper)
            datac.update_value_to_excel(pendingupdate, datapath)
            return swapper
        except:
            traceback.print_exc()
            raise
        finally:
            db.conn.close()