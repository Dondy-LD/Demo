import os


class InterfaceConstant:

    RS_STATUS_CD = "statusCode"
    RS_MESSAGE = "message"
    base_url = "http://172.16.35.218:8807"


class DataConstant:

    FILE_TYPE_EXCEL = "excel"
    FILE_TYPE_YAML = "yaml"
    FILE_TYPE_XML = "xml"
    FILE_TYPE_DB = "db"

    case_id = "case_id"

    # db_host = '172.16.35.218'
    # db_port = 32885
    # db_name = "vap-audit"

    mssql_db_host = "172.16.35.218"
    mssql_db_user = "sa"
    mssql_db_password = "P@ssword999"
    mssql_db_dbname = "IVH_DB"
    mssql_db_charset = "utf8"

    # MongoDB data info
    mongo_db_host = "secure.vms.local"   # modify the hosts file as "172.16.36.11 secure.vms.local"
    mongo_db_port = 27017
    mongo_db_name = "vms-ds"
    mongo_db_user = "vmsdbuser"  # vmsdbrootuser
    mongo_db_password = "vmsdbpassword" # vmsdbrootpassword


class LogConstant:
    all_when = "midnight"
    all_backupCount = 7

    error_when = "midnight"
    error_backupCount = 7


class TestCases:

    PROJECT_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

    TESTDATA_COLS_EXCLUDE = [
        'executed'
    ]

    PRECON_COLS_EXCLUDE = [
        'executed',
        'tdrequest_method',
        'tdrequest_url',
        'indicator',
        'swapper',
        'tdpath_param',
        'tdrequest_param',
        'tdexecuted'
    ]

    TRARDOWN_COLS_EXCLUDE = [
        'request_method',
        'request_url',
        'path_param',
        'request_param',
        'field_value',
        'tdfield_value',
        'executed',
        'tdexecuted'
    ]
    Replace_URL=[
        "/vms/device/devices",
        "/vms/device/devices/{deviceId}",
        "/vms/schedules/save",
        "/vms/sms/streams/live"
    ]
    Dataset_type = [
        "pre_dataset",
        "test_dataset",
        "td_dataset"
    ]
    data_type = "excel"
    data_path = os.path.join(PROJECT_DIR, "data", "test_data.xls") + "&device_service"
    predata_path = os.path.join(PROJECT_DIR, "data", "test_data.xls") + "&precondition"

    ssl_ca_certs = os.path.join(PROJECT_DIR, "cert_file", "ca_certificate.pem")
    ssl_certfile = os.path.join(PROJECT_DIR, "cert_file", "client.pem")

    # Specific the cases' type need to be executed, if no cases type provided, default to execute all the test cases

    case_type_to_execute = []

