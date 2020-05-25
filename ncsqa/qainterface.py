import requests
import os
from qaconfig import InterfaceConstant as ic
from qaconfig import TestCases as tc


class InterFace:

    def __init__(self, method, path, headers=None, param=None, data=None, form_data=None, json=None,
                 swapper=None, indicator=None, files=None):
        self._method = method
        self._path = ic.base_url + path

        if indicator == "headers" and isinstance(headers, dict):
            strjson = str(headers)
            for key, value in swapper.items():
                strjson = strjson.replace(key, str(value))
                self._headers = eval(strjson)
        else:
            self._headers = headers

        if indicator == "data" and isinstance(data, dict):
            strjson = str(data)
            for key, value in swapper.items():
                strjson = strjson.replace(key, str(value))
                self._data = eval(strjson)
        else:
            self._data = data

        if indicator == "json" and isinstance(json, dict):
            strjson = str(json)
            for key, value in swapper.items():
                strjson = strjson.replace(key, str(value))
                self._json = eval(strjson)
        else:
            self._json = json

        if indicator == "param" and isinstance(param, dict):
            strjson = str(param)
            for key, value in swapper.items():
                strjson = strjson.replace(key, str(value))
                self._param = eval(strjson)
        else:
            self._param = param

        if indicator == "path":
            for key, value in swapper.items():
                self._path = self._path.replace(key, str(value))

        if indicator == "form-data" and isinstance(form_data, dict):
            strjson = str(form_data)
            for key, value in swapper.items():
                strjson = strjson.replace(key, str(value))
                self.form_data = eval(strjson)
        else:
            self.form_data = form_data

        if isinstance(files, dict):
            filepath = os.path.join(tc.PROJECT_DIR, "data", "upload", files.get("file"))
            (file_path, tempfilename) = os.path.split(filepath)
            self._files = {'file': (tempfilename, open(filepath, "rb"), 'image/png')}
        else:
            self._files = files

        # print(self._path)
        if self._method == "get":
            self._response = requests.get(self._path, params=self._param, headers=self._headers)
        elif self._method == "post":
            self._response = requests.post(self._path, data=self._data, json=self._json, files=self._files, headers=self._headers)
        elif self._method == "put":
            self._response = requests.put(self._path, data=self._data, json=self._json, headers=self._headers)
        elif self._method == "delete":
            self._response = requests.delete(self._path, headers=self._headers)

    status_ok = requests.codes.ok

    @property
    def responseurl(self):

        return self._response.url

    @property
    def httpstatuscd(self):

        return self._response.status_code

    @property
    def responsejson(self):

        return self._response.json()

    @property
    def responsetext(self):

        return self._response.text

    @property
    def responsecontent(self):
        return self._response.content