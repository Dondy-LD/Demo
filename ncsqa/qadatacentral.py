import xlrd, xlwt
from xlutils.copy import copy
from qaconfig import DataConstant, TestCases

"""
It is simple factory pattern.
From client side, they only need provide the filetype and filepath. 

The supported filetype is:
    (1)excel
    (2)yaml 
    (3)xml
    (4)db
"""


def get_data_central(filetype, path):
    if filetype == DataConstant.FILE_TYPE_EXCEL:
        dtc = Excel(path)
    elif filetype == DataConstant.FILE_TYPE_YAML:
        dtc = Yaml(path)
    elif filetype == DataConstant.FILE_TYPE_XML:
        dtc = Xml(path)
    elif filetype == DataConstant.FILE_TYPE_DB:
        dtc = DB(path)
    # TODO -- exception handle if no filetype match
    return dtc


"""
It is father class, will put the common method for data central process.
And these methods can be used by child
"""


class DataCentral:

    """
    For pytest cases execution, the parameter need to be a list.
    So this method is to provide the function to convert the data to the cases execution format.
    :param dataset -- the data set to filter the data
    :return
    """

    # def convert_to_parameter(self, dataset, datacols=None):
    #     testdataset = []
    #     casetypes = TestCases.case_type_to_execute
    #     if datacols is None:
    #         datacols = TestCases.TESTDATA_COLS_EXCLUDE
    #
    #     for item in dataset:
    #         if item.get("executed") == "Y" or item.get("tdexecuted") == "Y":
    #             if casetypes and item.get("case_type") and item.get("case_type") not in casetypes:
    #                 continue
    #             else:
    #                 subitem = {key: value for key, value in item.items() if key not in datacols}
    #                 testdataset.append(subitem)
    #     return testdataset

    def convert_to_parameter_test(self, dataset, data_type, datacols=None):
        testdataset = []
        casetypes = TestCases.case_type_to_execute
        if datacols is None:
            datacols = TestCases.TESTDATA_COLS_EXCLUDE

        if data_type in("pre_dataset", "test_dataset"):
            for item in dataset:
                if item.get("executed") == "Y":
                    if casetypes and item.get("case_type") and item.get("case_type") not in casetypes:
                        continue
                    else:
                        subitem = {key: value for key, value in item.items() if key not in datacols}
                        testdataset.append(subitem)
        if data_type == "td_dataset":
            for item in dataset:
                if item.get("tdexecuted") == "Y":
                    if casetypes and item.get("case_type") and item.get("case_type") not in casetypes:
                        continue
                    else:
                        subitem = {key: value for key, value in item.items() if key not in datacols}
                        testdataset.append(subitem)
        return testdataset


class Excel(DataCentral):

    """
    if need to specify the sheetname,  append the sheetname to the filepath with "&"
    For example:
        the excel path of the file is "D:\test\testdata.xls"
        the sheetname is "testdata"
        the path should be "D:\test\testdata.xls&testdata"

    if no need to specify the sheetname, just pass the excel path, will get the 1st sheet by default
    """

    _PATH_SEPARATOR = "&"
    _DEFAULT_SHEET_INDEX = 0

    def __init__(self, path):

        if self._PATH_SEPARATOR in path:

            excel_path_sheetname = path.split(self._PATH_SEPARATOR)
            self.excel_path = excel_path_sheetname[0]
            self.excel_sheetname = excel_path_sheetname[1]

            self.data = xlrd.open_workbook(self.excel_path, formatting_info=True)
            self.table = self.data.sheet_by_name(self.excel_sheetname)
        else:
            self.excel_path = path
            self.data = xlrd.open_workbook( self.excel_path, formatting_info=True)
            self.table = self.data.sheet_by_index(self._DEFAULT_SHEET_INDEX)

        # retrieve the 1st line to make it as keys
        self.keys = self.table.row_values(0)

        # retrieve the total row number
        self.rowNum = self.table.nrows

        # retrieve the total col number
        self.colNum = self.table.ncols

    def read_data(self):
        """Convert the excel data to a list which is combined by the dictionaries.
        For example:
            excel is like below
                name    age
                 dog     16
                 cat     18
            the returned list will be: [{"name":"dog", "age":"16"}, {"name":"cat", "age":"18"}]
        """
        if self.rowNum <= 1:
            print("the total rownum is less than 1")
        else:
            data_list = []
            j = 1
            for i in range(self.rowNum - 1):
                t = {}
                # get the value from 2nd line
                values = self.table.row_values(j)
                for x in range(self.colNum):
                    t[self.keys[x]] = values[x]

                data_list.append(t)
                j += 1

            return data_list

    def get_index_by_row_column_value(self, row_value, col_value):
        """Returns its index based on row and column values"""
        rowval = self.table.row_values(0)
        colval = self.table.col_values(0)

        len(rowval)
        colindex = rowval.index(col_value)
        rowindex = colval.index(row_value)

        return rowindex, colindex

    def get_index_by_row_value(self, row_value):
        """Returns the index of the request_url column based on row_value"""
        colval = self.table.col_values(2)

        rowindex = colval.index(row_value)

        return rowindex

    def get_calval_by_col_value(self, col_value):
        """Returns the index of the column to which a value belongs"""
        rowval = self.table.row_values(0)
        colindex = rowval.index(col_value)
        colval = self.table.col_values(colindex)
        return colval,colindex

    def update_value_to_excel(self, udatalist, datapath):
        if self._PATH_SEPARATOR in datapath:
            excel_path_sheetname = datapath.split(self._PATH_SEPARATOR)
            excel_path = excel_path_sheetname[0]
            excel_sheetname = excel_path_sheetname[1]
        else:
            excel_path = datapath

        old_excel = xlrd.open_workbook(excel_path, formatting_info=True)
        new_excel = copy(old_excel)

        if excel_sheetname:
            ws = new_excel.get_sheet(excel_sheetname)
        else:
            ws = new_excel.get_sheet(self._DEFAULT_SHEET_INDEX)

        # Set the table cell format
        style = xlwt.XFStyle()
        a1 = xlwt.Alignment()  # Set the table cell as vertical center
        a1.vert = 0x01
        a1.wrap = 0x01
        b1 = xlwt.Borders()  # Set the table cell as thin
        b1.bottom = 0x01
        b1.right = 0x01

        style.alignment = a1
        style.borders = b1

        for data in udatalist:
            ws.write(data[0], data[1], str(data[2]))

        new_excel.save(excel_path)

    def __str__(self):
        return "Excel.."


class Yaml(DataCentral):

    def __init__(self, path):
        print("hello, this is init method for yaml")

    def read_data(self):
        print("hello, this is read_data for yaml")

    def __str__(self):
        print("hello, this is drcription for yaml")


class DB(DataCentral):

    def __init__(self, path):
        print("hello, this is init method for DB")

    def read_data(self):
        print("hello, this is read_data for DB")

    def __str__(self):
        print("hello, this is drcription for DB")


class Xml(DataCentral):
    def __init__(self, path):
        print("hello, this is init method for XML")

    def read_data(self):
        print("hello, this is read_data for XML")

    def __str__(self):
        print("hello, this is drcription for XML")
