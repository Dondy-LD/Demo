from pymongo import MongoClient
from qaconfig import DataConstant as dc
from qaconfig import TestCases as tc


class MongoDB:
    def __init__(self, host="localhost", port=27017, dbname=None, username=None, password=None):
        """Initial mongoDB instance:
                :parameter
                --host: MongoDB URI, if not provided, the default value is "localhost"
                --port: MongoDB Port, if not provided, the default value is 27017
                --dbname: Database name, if not provide, will use the default DB name which is implemented in client.get_database()
                --username / password: Database connect username and password, if provided, will do the authentication

                (1) Init an MongoDB client with host and port
                (2) Get a database with dbname
                (3) Validate username and password if provided

                Normally the MongoDB will close and release the resource automatically, but if hit the exception, will manually close the mongoDB client.

                The use is like:

                from ncsqa import KqaDataBase
                mongoDB = KqaDataBase.MongoDB(host="192.168.200.215", dbname="core_engine", username="core_engine", password="core_engine")
        """
        self.host = dc.mongo_db_host
        self.port = dc.mongo_db_port
        self.dbname = dc.mongo_db_name
        self.username = dc.mongo_db_user
        self.password = dc.mongo_db_password
        # SSL verify
        try:
            self.client = MongoClient(self.host, self.port, ssl=True,
                                      ssl_ca_certs=tc.ssl_ca_certs, ssl_certfile=tc.ssl_certfile)
            self.db = self.client.get_database(self.dbname)
            if self.username and self.password:
                self.db.authenticate(self.username, self.password)
        except Exception as err:
            print("initial the database failed, the error is: " + str(err))
            if self.client:
                self.client.close()

    def insert(self, databasename, collectionname, data):
        """
        To insert the data to the specific collection.

        :param databasename:  The name of database, it is a string
        :param collectionname:  The name of collection, it is a string
        :param data: the Data need to be added.
                            If only insert one record, just pass one document in json format, like:
                            data = {
                                 "_id":1,
                                "className" : "com.kaisquare.db.model.Device",
                                "name" : "NUCi5_200",
                                " device_key" : "b8:ae:ed:7f:0d:6f",
                            }
                            if insert many records one time, need pass the array of documents in json format, like:
                            data = [
                            {
                                 "_id":1,
                                "className" : "com.kaisquare.db.model.Device",
                                "name" : "NUCi5_200",
                                " device_key" : "b8:ae:ed:7f:0d:6f",
                            }, {
                                 "_id":2,
                                "className" : "com.kaisquare.db.model.Device.Test",
                                "name" : "NUCi5_200_Test",
                                " device_key" : "b8:ae:ed:7f:0d:6fTest",
                            }
                            ]
        """
        mydatabase = self.client[databasename]
        mydatabase.get_collection(collectionname).insert(data)

    def save(self, databasename, collectionname, data):
        """
        :param databasename:
        :param collectionname:
        :param data:
        :return:
        """
        mydatabase = self.client[databasename]
        return mydatabase.get_collection(collectionname).save(data)

    def find_one(self, databasename, collectionname, query=None, returncol=None):
        """
        Base on the query condition to search out the first record of all matched records, and return the specific columns which are included in returncol.

        :param databasename: The name of the database - it is a string
        :param collectionname: The name of the collection - it is a string
        :param query: The conditions that the results must match
        :param returnedcol: The fields need to be included in the results. If it is not provided, default to return all the columns
                            And the "_id" default to be returned, if not required, just add {"_id": 0}
        :return: The first record of the record list which is matched with query condition returned, and include the returnedcol

        The use is like:
            from ncsqa import qadatabase
            mongoDB = KqaDataBase.MongoDB(host="192.168.200.215", dbname="core_engine", username="core_engine", password="core_engine")

            mongoDB.find_one("Device", query = {"_id": 5}, returnedcol = {'className':1}
        """
        mydatabase = self.client[databasename]
        returnlist = mydatabase.get_collection(collectionname).find_one(query, returncol)

        return returnlist

    def find_all(self, databasename, collectionname, query=None, returncol=None):
        """
        Base on the query condition to search out all the matched records, and return the specific columns which are included in returncol.

        :param databasename: The name of the database - it is a string
        :param collectionname: The name of the collection - it is a string
        :param query: The conditions that the results must match
        :param returnedcol: The fields need to be included in the results. If it is not provided, default to return all the columns
                            And the "_id" default to be returned, if not required, just add {"_id": 0}
        :return: All records which is matched with query condition returned, and include the returnedcol

        The use is like:

        from ncsqa import qadatabase
        mongoDB = qadatabase.MongoDB(host="192.168.200.215", dbname="core_engine", username="core_engine", password="core_engine")

        mongoDB.find_all("Device", query = {"_id": 5}, returncol = {'className':1}
        """
        mydatabase = self.client[databasename]
        returnlist = list(mydatabase.get_collection(collectionname).find(query, returncol))

        return returnlist

    def find_all_num(self, databasename, collectionname, query=None, returncol=None):
        mydatabase = self.client[databasename]
        returnlist = list(mydatabase.get_collection(collectionname).find(query, returncol))

        return len(returnlist)

    def delete(self, databasename, collectionname, data):
        mydatabase = self.client[databasename]
        mydatabase.get_collection(collectionname).delete_one(data)

    def get_delete_number(self, databasename, collectionname, data):
        mydatabase = self.client[databasename]
        result = mydatabase.get_collection(collectionname).delete_many(data)
        return result.deleted_count

    def update(self, databasename, collectionname, data, newdata):
        print("update...")
        mydatabase = self.client[databasename]
        mydatabase.get_collection(collectionname).update(data, newdata)

#
# if __name__ == "__main__":
#     mongoDB = MongoDB()
#     # result = mongoDB.find_one("vap-analytics", "App", query={"_id": "kedacom-app-kedacom"})
#     # print(result)
#     # result1 = mongoDB.find_all("vap-analytics", "App")
#     # print(result1)
#     result3 = mongoDB.find_all_num("vms-ds", "Device", {"name": "device_test_0068"})
#     mongoDB.delete("vms-ds", "Device", {"name": "device_test_0068"})
#     result4 = mongoDB.find_all("vms-ds", "Device", {"name": "device_test_0068"})
#     print(result3)
#
#     print(result4)
    a=False