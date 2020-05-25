import pytest
import re
from qalogger import log
from qaconfig import TestCases as tc, DataConstant as dc
from ncsqa import qadatacentral as dtc
from ncsqa import qainterface
from ncsqa import qacommon as qc
from ncsqa import qadatabase
from validation import comvalidation, specialvalidation

mongodb_tc = qadatabase.MongoDB()

# ========fixture=============
def pytest_generate_tests(metafunc):
    # called once per each test function
    funcarglist = metafunc.cls.params[metafunc.function.__name__]
    # print(funcarglist)
    argnames = list(funcarglist[0]) if len(funcarglist) > 0 else funcarglist
    metafunc.parametrize(argnames, [[funcargs[name] for name in argnames] for funcargs in funcarglist], ids=[item[dc.case_id] for item in funcarglist])


class TestCases:

    # Step1: Get test data
    _predatac = dtc.get_data_central(tc.data_type, tc.predata_path)
    _predataset = _predatac.read_data()
    _pretestdata = _predatac.convert_to_parameter_test(_predataset, data_type=tc.Dataset_type[0], datacols=tc.PRECON_COLS_EXCLUDE)
    _tdtestdata = _predatac.convert_to_parameter_test(_predataset, data_type=tc.Dataset_type[2], datacols=tc.TRARDOWN_COLS_EXCLUDE)

    _datac = dtc.get_data_central(tc.data_type, tc.data_path)
    _dataset = _datac.read_data()
    _testdata = _datac.convert_to_parameter_test(_dataset, data_type=tc.Dataset_type[1])

    logging = log()

    params = {
        "test_precondition": _pretestdata,
        "test_cases": _testdata,
        "test_teardown": _tdtestdata
    }

    def test_precondition(self, case_id, request_method, request_url, request_param, field_value, tdfield_value):
        # noinspection PyBroadException
        try:
            # Step2: Send Request and Response
            response = qainterface.InterFace(request_method, request_url,
                                                 headers=eval(request_param).get("headers") if request_param else None,
                                                 param=eval(request_param).get("param") if request_param else None,
                                                 data=eval(request_param).get("form-data") if request_param else None,
                                                 json=eval(request_param).get("json-data") if request_param else None,
                                                 files=eval(request_param).get("files") if request_param else None)

            if response.httpstatuscd != response.status_ok:
                    raise Exception(response.responsetext)
            # Step3: Replace target field value
            if field_value:
                datac = dtc.get_data_central(tc.data_type, tc.data_path)
                qc.update_testdata_for_data_preparation(datac, case_id, response.responsejson,
                                                        eval(field_value), tc.data_path)
            if tdfield_value:
                    predatac = dtc.get_data_central(tc.data_type, tc.predata_path)
                    qc.update_testdata_for_data_teardown(predatac, case_id,
                                                            response.responsejson, eval(tdfield_value), tc.predata_path)

            self.logging.info("Precondition Pass ! test case %s passed" % case_id)

        except Exception as e:

            self.logging.info("Precondition Fail ! test case %s failed" % case_id)

            self.logging.error(e, exc_info=True)

            pytest.fail()

    def test_cases(self, case_id,  case_purpose, request_method, request_url, request_param,
                   expected_statuscd, expected_response, validation_query, expected_validation_result, case_type, swapper, indicator, pre_sql, pre_mongodb):
        # noinspection PyBroadException
        try:
            # Execute Sql to prepare the test data per test case. pre_sql can be a query as string or a list of queries.
            new_swapper = eval(swapper) if swapper else None  # read data form database to replace the request data
            if pre_sql:
                sql = eval(pre_sql)
                if isinstance(sql, str):
                    if re.search('select', sql, re.IGNORECASE):
                        datac = dtc.get_data_central(tc.data_type, tc.data_path)
                        new_swapper = qc.excute_sql_and_replace("mssql", sql, datac, case_id, eval(swapper), tc.data_path)
                    else:
                        qc.exec_SQL_script("mssql", sql)
                elif isinstance(sql, list):
                    for items in sql:
                        qc.exec_SQL_script("mssql", items)
                self.logging.info("Precondition SQL executed for this test case.")
            if pre_mongodb:
                mongodb_data = eval(pre_mongodb)
                if isinstance(mongodb_data, dict):
                    method = mongodb_data.get("method")
                    if method =="delete":
                        mongodb_tc.delete(mongodb_data.get("database_name"), mongodb_data.get("collection_name"),
                                       mongodb_data.get("key_field"))

            # Step2:  Send request and get response
            response = qainterface.InterFace(request_method, request_url,
                                             headers=eval(request_param).get("headers") if request_param else None,
                                             param=eval(request_param).get("param") if request_param else None,
                                             data=eval(request_param).get("form-data") if request_param else None,
                                             files=eval(request_param).get("files") if request_param else None,
                                             json=eval(request_param).get("json-data") if request_param else None,
                                             swapper=new_swapper if new_swapper else None,
                                             indicator=indicator if indicator else None)
            self.logging.debug("the response for case %s is %s" % (case_id, response.responsetext))

            # Step3: Get response to do common validation

            comvalidation.common_validation(response, expected_statuscd, expected_response)

            # Step4: Special validation base on caseType
            if case_type:
                specialvalidation.special_validation(case_id, case_type, response, expected_response, validation_query, expected_validation_result)
                self.logging.info("Cases Pass ! %s:%s passed" % (case_id, case_purpose))

        except AssertionError as error:

            self.logging.info("Cases Fail ! %s:%s failed, the actual result is different with expected result" % (case_id, case_purpose))

            self.logging.error(error)

            pytest.fail()

        except Exception as e:

            self.logging.info("Cases Fail ! %s:%s failed,  some error hit in test scripts, please contact QA team for more help!" % (case_id, case_purpose))

            self.logging.error(e, exc_info=True)

            pytest.fail()

    def test_teardown(self, case_id, tdrequest_method, tdrequest_url, tdrequest_param, indicator, swapper):
        # Step2: Send Request and Response
        try:
            response = qainterface.InterFace(tdrequest_method, tdrequest_url,
                                             headers=eval(tdrequest_param).get("headers") if tdrequest_param else None,
                                             param=eval(tdrequest_param).get("param") if tdrequest_param else None,
                                             data=eval(tdrequest_param).get("form-data") if tdrequest_param else None,
                                             json=eval(tdrequest_param).get("json-data") if tdrequest_param else None,
                                             swapper=eval(swapper) if swapper else None, indicator=indicator if indicator else None)

            if response.httpstatuscd != response.status_ok:
                raise Exception(response.responsetext)

            self.logging.info("Teardown Pass ! test case %s passed" % case_id)

        except Exception as e:

            self.logging.info("Teardown Fail ! test case %s failed" % case_id)

            self.logging.error(e, exc_info=True)

            pytest.fail()
