# -*- coding: utf-8 -*-
import json

import jmespath
from core.logs import log
import ast


def json_search(exp, data, options=None):
    try:
        return jmespath.search(exp, data, options)
    except Exception as e:
        log.error('json search error, error info is: {}'.format(e))
        return None


def str_to_json(string_: str):
    """
    func:将字符串转换为json格式
    :param string_:
    :return:
    """
    if not isinstance(string_, str):
        raise TypeError('malformed string')
    return ast.literal_eval(string_)


def json_to_string(node: dict, **kwargs):
    """
    func：将字典转换为string
    :param node:
    :return:
    """
    kwargs['ensure_ascii'] = kwargs.get('ensure_ascii') or False
    if not isinstance(node, dict):
        raise ValueError('malformed node')
    return json.dumps(node, **kwargs)


import dominate
from dominate.tags import *
from dominate import tags


class HtmlCreator(object):
    """
    生成html文本
    """

    def __init__(self, charset='utf-8', title='Report'):
        self.doc = dominate.document(title=title)
        self.charset = charset
        self._add_default_head()

    def simple_add(self, tag='', content='', color=''):
        if not hasattr(tags, tag) and tag:
            raise ValueError('can not supported this tag')

        if color:
            color = 'color: {}'.format(color)

        with self.doc:
            if not tag:
                tag = tags.p
            else:
                tag = getattr(tags, tag)
            if isinstance(content, dict):
                pre(str(json_to_string(content, ensure_ascii=False, indent=2)), style=color)

            else:
                for item in content.split('\n'):
                    if item:
                        tag(item, style=color)

        return str(self.doc)

    def _add_default_head(self):
        with self.doc.head:
            meta(charset=self.charset)
