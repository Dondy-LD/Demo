# import requests
# # #
# # url22 = 'http://172.16.35.218:8807/vms/device/addMultipleDevice'
# # test222 = 'C:\\Users\\p1321768\\PycharmProjects\\qa-ummi-device-service-testing\\data\\upload\\Tem.xlsx'
# # files = {'file':  ('Tem.xlsx', open(test222, 'rb'), 'xlsx')}
# # testdata = {"createdId": "superadmin"}
# # # files = {'file': ('report.jpg', open('/home/lyb/sjzl.mpg', 'rb'))}     #显式的设置文件名
# # # #
# # r = requests.post(url22, files=files, data=testdata)
# # print(r.text)
# # #
#
# test_url = 'http://172.16.35.218:8807/vms/device/deviceIcon/upload'
# test = 'C:\\Users\\p1321768\\PycharmProjects\\qa-ummi-device-service-testing\\data\\upload\\test.jpg'
# test_files = {'file': open(test, 'rb')}
# r = requests.post(url=test_url, files=test_files)
# print(r.text)
#
# test = 'C:\\Users\\p1321768\\PycharmProjects\\qa-ummi-device-service-testing\\data\\upload\\test.jpg'
#
# url = 'http://172.16.35.218:8807/vms/device/deviceIcon/upload'
#
# # files = {'file': open(test, 'rb')}
#
# files = {
#         "file": ('uploadDeviceIcon01.PNG', open(test, 'rb'), 'image/png')
#     }
#
#
# r = requests.post(url, files=files)
# print(r.text)
# # # # import time
# # # # now_time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
# # # # print(type(now_time))
# #
# # import jsonpath
# #
# # aaa = {
# #     "status": 200,
# #     "message": "Success",
# #     "data": {
# #         "totalNum": 16,
# #         "pageNo": 0,
# #         "pageSize": 10,
# #         "items": [
# #             {
# #                 "createdId": "superadmin",
# #                 "lastUpdatedId": "superadmin",
# #                 "createdDate": "2020-05-18T08:12:04.567+0000",
# #                 "lastUpdatedDate": "2020-05-18T08:12:04.567+0000",
# #                 "version": 0,
# #                 "deviceId": "e40bf0cd19d448d485efacdd180982c4",
# #                 "deviceName": "device_test_0027",
# #                 "deviceUri": "tcp://10.20.5.27:8000/",
# #                 "modelId": "hikvision-ipc",
# #                 "deviceType": "ipc",
# #                 "channelCount": 0,
# #                 "vmsStatus": "unavailable",
# #                 "firmware": None,
# #                 "verdorModel": None,
# #                 "userName": None,
# #                 "modelName": "Hikvision IP Camera"
# #             },
# #             {
# #                 "createdId": "superadmin",
# #                 "lastUpdatedId": "superadmin",
# #                 "createdDate": "2020-05-18T08:12:04.267+0000",
# #                 "lastUpdatedDate": "2020-05-18T08:12:04.267+0000",
# #                 "version": 1,
# #                 "deviceId": "7ed42c1b9bd54a3aabf82eecd43cc830",
# #                 "deviceName": "device_test_0026",
# #                 "deviceUri": "tcp://10.20.5.26:8000/",
# #                 "modelId": "hikvision-ipc",
# #                 "deviceType": "ipc",
# #                 "channelCount": 0,
# #                 "vmsStatus": "authentication-failed",
# #                 "firmware": None,
# #                 "verdorModel": None,
# #                 "userName": None,
# #                 "modelName": "Hikvision IP Camera"
# #             },
# #             {
# #                 "createdId": "superadmin",
# #                 "lastUpdatedId": "superadmin",
# #                 "createdDate": "2020-05-18T07:57:25.797+0000",
# #                 "lastUpdatedDate": "2020-05-18T07:57:32.097+0000",
# #                 "version": 2,
# #                 "deviceId": "deb0c32884a94bbbae3ff63df33a4871",
# #                 "deviceName": "device_test_hik12",
# #                 "deviceUri": "tcp://10.20.5.12:8000/",
# #                 "modelId": "hikvision-ipc",
# #                 "deviceType": "ipc",
# #                 "channelCount": 1,
# #                 "vmsStatus": "active",
# #                 "firmware": "V5.5.0@25/7/2018",
# #                 "verdorModel": "DS-2DE2204IW-DE3/W",
# #                 "userName": None,
# #                 "modelName": "Hikvision IP Camera"
# #             },
# #             {
# #                 "createdId": "superadmin",
# #                 "lastUpdatedId": "superadmin",
# #                 "createdDate": "2020-05-18T05:06:18.887+0000",
# #                 "lastUpdatedDate": "2020-05-18T05:06:24.377+0000",
# #                 "version": 5,
# #                 "deviceId": "b30f1a433eb544e2a8da3cfaec7d33b5",
# #                 "deviceName": "device_test_0044",
# #                 "deviceUri": "rtsp://10.20.5.44:8082/",
# #                 "modelId": "general-rtsp",
# #                 "deviceType": "ipc",
# #                 "channelCount": 0,
# #                 "vmsStatus": "authentication-failed",
# #                 "firmware": None,
# #                 "verdorModel": None,
# #                 "userName": None,
# #                 "modelName": "general-rtsp"
# #             },
# #             {
# #                 "createdId": "superadmin",
# #                 "lastUpdatedId": "superadmin",
# #                 "createdDate": "2020-05-18T04:26:31.200+0000",
# #                 "lastUpdatedDate": "2020-05-18T04:26:31.200+0000",
# #                 "version": 0,
# #                 "deviceId": "832a8879d3974919a050006e68703db7",
# #                 "deviceName": "device_test_77",
# #                 "deviceUri": "tcp://10.20.5.77:8000/",
# #                 "modelId": "hikvision-ipc",
# #                 "deviceType": "ipc",
# #                 "channelCount": 0,
# #                 "vmsStatus": "unavailable",
# #                 "firmware": None,
# #                 "verdorModel": None,
# #                 "userName": None,
# #                 "modelName": "Hikvision IP Camera"
# #             },
# #             {
# #                 "createdId": "superadmin",
# #                 "lastUpdatedId": "superadmin",
# #                 "createdDate": "2020-05-15T10:23:46.140+0000",
# #                 "lastUpdatedDate": "2020-05-15T10:27:39.807+0000",
# #                 "version": 6,
# #                 "deviceId": "4b10f1bb27644d4c805c72c10424be9e",
# #                 "deviceName": "devicetest_update1",
# #                 "deviceUri": "rtsp://10.20.5.60:8082/",
# #                 "modelId": "general-rtsp",
# #                 "deviceType": "ipc",
# #                 "channelCount": 1,
# #                 "vmsStatus": "disconnected",
# #                 "firmware": "RTSP",
# #                 "verdorModel": None,
# #                 "userName": None,
# #                 "modelName": "general-rtsp"
# #             },
# #             {
# #                 "createdId": "superadmin",
# #                 "lastUpdatedId": "superadmin",
# #                 "createdDate": "2020-05-15T09:27:43.913+0000",
# #                 "lastUpdatedDate": "2020-05-15T09:30:19.527+0000",
# #                 "version": 3,
# #                 "deviceId": "33a7ced73dc447558bc770aba9fdb530",
# #                 "deviceName": "devicetest_update",
# #                 "deviceUri": "rtsp://10.20.5.30:8082/",
# #                 "modelId": "general-rtsp",
# #                 "deviceType": "ipc",
# #                 "channelCount": 0,
# #                 "vmsStatus": "unavailable",
# #                 "firmware": None,
# #                 "verdorModel": None,
# #                 "userName": None,
# #                 "modelName": "general-rtsp"
# #             },
# #             {
# #                 "createdId": "superadmin",
# #                 "lastUpdatedId": "superadmin",
# #                 "createdDate": "2020-05-15T02:39:11.090+0000",
# #                 "lastUpdatedDate": "2020-05-15T02:40:47.270+0000",
# #                 "version": 3,
# #                 "deviceId": "899838a7e4934feeae042effd3a97ab3",
# #                 "deviceName": "devicetestupdate",
# #                 "deviceUri": "rtsp://10.20.5.13:8082/",
# #                 "modelId": "general-rtsp",
# #                 "deviceType": "ipc",
# #                 "channelCount": 0,
# #                 "vmsStatus": "unavailable",
# #                 "firmware": None,
# #                 "verdorModel": None,
# #                 "userName": None,
# #                 "modelName": "general-rtsp"
# #             },
# #             {
# #                 "createdId": "superadmin",
# #                 "lastUpdatedId": "superadmin",
# #                 "createdDate": "2020-05-14T02:02:09.567+0000",
# #                 "lastUpdatedDate": "2020-05-14T02:02:09.567+0000",
# #                 "version": 0,
# #                 "deviceId": "a1bb46e11add44eeb8b08de2e832729e",
# #                 "deviceName": "device_test_0094",
# #                 "deviceUri": "tcp://10.20.5.94:8000/",
# #                 "modelId": "hikvision-ipc",
# #                 "deviceType": "ipc",
# #                 "channelCount": 0,
# #                 "vmsStatus": "unavailable",
# #                 "firmware": None,
# #                 "verdorModel": None,
# #                 "userName": None,
# #                 "modelName": "Hikvision IP Camera"
# #             },
# #             {
# #                 "createdId": "superadmin",
# #                 "lastUpdatedId": "superadmin",
# #                 "createdDate": "2020-05-14T02:02:03.407+0000",
# #                 "lastUpdatedDate": "2020-05-14T06:54:05.373+0000",
# #                 "version": 2,
# #                 "deviceId": "cfbc979e4d224fcd8a13b8dd369f918a",
# #                 "deviceName": "device_test_0017",
# #                 "deviceUri": "rtsp://10.20.5.17:554/",
# #                 "modelId": "general-rtsp",
# #                 "deviceType": "ipc",
# #                 "channelCount": 1,
# #                 "vmsStatus": "active",
# #                 "firmware": "RTSP",
# #                 "verdorModel": "RTSPMediaServer",
# #                 "userName": None,
# #                 "modelName": "general-rtsp"
# #             }
# #         ]
# #     },
# #     "rel": True
# # }
# #
# # mm = jsonpath.jsonpath(aaa, "$..deviceId")
# # print(mm)
# ls1 = ['a', '1', 'b', '2']
# ls3 = ''.join(ls1)
# print(ls3)


mm = {"json-data": {
  "iconId":None,
  "modelId": "hikvision-ipc",
  "status": "offline",
  "{iconUri}": "8cd5a7ee-3eec-49c3-a4cc-d6808d469d33.png",
  "modelName": "Hikvision IP Camera",
  "createdId":"superadmin",
  "lastUpdatedId":"superadmin"
}}

swapper = {'{iconUri}': 'temp'}

if isinstance(mm, dict):
    strjson = str(mm)
    for key, value in swapper.items():
        strjson = strjson.replace(key, str(value))
        json = eval(strjson)

print(json)