# -*- coding: utf-8 -*-
import json
from json.decoder import JSONDecodeError

import requests
import string
from core.logs import log
from core.CustomExceptions import *
from requests.models import Response


class ApiHandler(object):
    def __init__(self, api_info):
        self.api_info = api_info
        log.debug(string.Template("api_info: $api_info").substitute(api_info=self.api_info))
        self.method = self.api_info['method']
        self.url = self.api_info['url']
        self.params = self.api_info['params'] if self.api_info['params'] else None
        self.header = self.api_info['header'] if self.api_info['header'] else None
        self.response: Response
        self._determine_content_type()

    def _determine_content_type(self):
        """
        :func: 判断请求头的content-type的类型，如果是application/json的话，默认对dict类型的请求参数进行json.dumps()转换为json格式
        :return:
        """
        if self.header and self.method.lower() == "post":
            content_type = self.header.get('Content-Type') or self.header.get('content-type')\
                           or self.header.get('ContentType') or self.header.get('contentType') or ""
            if 'application/json' in content_type or 'Application/json' in content_type \
                    or 'Application/Json' in content_type:
                self.params = json.dumps(self.params)

    def api_request(self):
        """
        :func: api请求的主入口，并返回请求的响应内容
        :return:
        """
        res = self._dispatch()
        self.response = res
        return self._determine_response_type()

    def _dispatch(self):
        try:
            method = self.method.lower()
            if method == "get":
                return self.get()
            elif method == "post":
                return self.post()
            elif method == "put":
                return self.put()
            elif method == "delete":
                return self.delete()
            elif method == "patch":
                return self.patch()
            else:
                raise RequestMethodException("api request method not supported")
        except RequestMethodException:
            raise RequestMethodException
        except Exception as e:
            log.error(string.Template("api request fail, error info: $e").substitute(e=e))
            raise ApiRequestError

    def _determine_response_type(self):
        """
        :func: 判断响应内容是否可以进行json格式转换，如果不行的话，则对响应内容的json方法进行重写，默认将响应内容的text以json返回
        :return: re setattr 后的response
        """
        res = self.response
        try:
            res.json()
            return res
        except JSONDecodeError:
            log.info('response JSONDecode Error, Returns the response text in JSON format')
            setattr(res, "json", self._override_json)
            return res

    def _override_json(self):
        """
        :func: 如果接口返回的响应内容无法进行json，则重写响应的json方法，将响应内容的text内容以json的格式返回
        :return: {"text": self.response.text}
        """
        text = self.response.text
        content = {"text": text}
        return content

    def get(self):
        res = requests.get(url=self.url, params=self.params, headers=self.header)
        return res

    def post(self):
        res = requests.post(self.url, data=self.params, headers=self.header)
        return res

    def put(self):
        res = requests.put(self.url, data=self.params, headers=self.header)
        return res

    def delete(self):
        res = requests.delete(self.url, data=self.params, headers=self.header)
        return res

    def patch(self):
        res = requests.patch(self.url, data=self.params, headers=self.header)
        return res
