# -*- coding: utf-8 -*-
"""
author：lufoqin
func：用例处理工具集
"""
import ast
import json
import os
import random
import re
import string
from string import Template
import pytz
from datetime import datetime, timedelta
from xeger import Xeger
from core.utils.common_tools import json_search
from core.CustomExceptions import TestcaseErrorException, VarReplaceException
from core.logs import log
from core.databases.db_helper import DbHelper
from core.utils.common_tools import str_to_json, json_to_string


class TmpObj(object):
    """
    临时过渡类，无实际作用
    """

    def __init__(self):
        self.interface_vars = {}


class ErrorCollector(object):
    def __init__(self):
        self.container = {}

    def add(self, type_, name, value):
        if not self.container.get(type_):
            self.container[type_] = {}
        value = str(value)
        if not self.container.get(type_).get(name):
            self.container[type_][name] = value
        else:
            self.container[type_][name] += " | {}".format(value)


class PreProcess(object):
    def __init__(self):
        self.object_list = []
        self.testcase = None
        self.interface_vars = {}
        self.error_collector = ErrorCollector()

    def add_random_str_for_var(self, testcase):
        testcase = testcase
        if not isinstance(testcase, dict):
            self.error_collector.add('add_random_str', 'testcase_error', testcase)
            raise TestcaseErrorException('testcase is not a dict format')

        pattern_random = re.compile(r"@$")
        random_str = generate_random_str()
        try:
            content = json_to_string(testcase, ensure_ascii=False)
        except Exception as e:
            log.error(string.Template("testcase json dumps fail, error info: $e").substitute(e=e))
            self.error_collector.add('add_random_str', 'json_dumps_fail', e)
            raise TestcaseErrorException("testcase json dumps fail, error info is: {}".format(e))
        content = re.sub(pattern_random, random_str, content)
        # log.debug(string.Template("after replaced random string: $content").substitute(content=content))
        pattern = re.compile(r"\$\S+\$")
        key_words = re.findall(pattern, content)
        log.debug(string.Template("所有需要添加随机字符的变量为: $key_words").substitute(key_words=key_words))

        if key_words:
            """
            循环遍历所有待替换的字符，如果待替换的字符在传入的对象列表中有对应的属性，则进行替换
            否则不作处理
            对象替换按传入的对象的下标进行排序，匹配到了之后，退出循环，即取最先匹配到的对象的属性值
            """
            for key_word in key_words:
                real_word = key_word.lstrip('$').rstrip('$')

                log.debug(string.Template("正在替换变量：$s").substitute(s=real_word))
                content = content.replace(key_word, real_word + generate_random_str(8))

        content = content.replace(random_str, r'$')
        try:
            json_content = str_to_json(content)
            self.testcase = json_content
            return json_content
        except Exception as e:
            log.error("testcase json loads fail, the error info: {}, the content is: {}".format(e, content))
            self.error_collector.add('add_random_str', 'json_loads_fail', (e, content))
            raise TestcaseErrorException("testcase json loads fail, the error info: {}, the content is: {}".format(e, content))

    def parse_case_vars(self, testcase, var_object: object):
        """
        func: 解析用例变量，如果用例中存在用例变量，则将用例变量存储到接口变量中，以供后续变量引用
        :param testcase: 单条测试用例
        :param var_object: 接口变量存储对象
        :return:
        """
        log.debug('start to parse testcase vars')
        if not isinstance(testcase, dict):
            self.error_collector.add('parse_case_vars', 'testcase_error', testcase)
            raise TestcaseErrorException('testcase is not a dict object')
        if not hasattr(var_object, "interface_vars"):
            var_object.interface_vars = {}
        case_var = testcase.get('case_vars')
        if case_var:
            for k, v in case_var.items():
                var_object.interface_vars[k] = v

    def datetime_translate(self, testcase: dict):
        """
        将用例中符合日期格式的变量替换成对应的时间日期
        :param testcase: 需要处理的用例
        :return: 处理后的用例
        """
        log.info('start to translate datetime')
        testcase = testcase
        time_format = "%Y-%m-%d %H:%M:%S"
        date_format = "%Y-%m-%d"
        if not isinstance(testcase, dict):
            self.error_collector.add('datetime_translate', 'testcase_error', testcase)
            raise TestcaseErrorException("testcase is not a dict format")

        # 用于匹配时间格式，包含时分秒
        pattern_now = re.compile(r'<#dnow\(\)>')
        pattern_now_opr = re.compile(r'(<#dnow\(\)\s*([+-])\s*(\d+)>)')
        pattern_time = re.compile(r'(<#d(\d{4}-\d{1,2}-\d{1,2}\s\d{2}:\d{2}:\d{2})>)')
        pattern_time_opr = re.compile(r'(<#d(\d{4}-\d{1,2}-\d{1,2}\s\d{2}:\d{2}:\d{2})\s*([+-])\s*(\d+)>)')

        # 用于匹配日期格式，不包含时分秒
        pattern_date = re.compile(r'<#ddate\(\)>')
        pattern_date_opr = re.compile(r'(<#ddate\(\)\s*([+-])\s*(\d+)>)')
        pattern_date_str = re.compile(r'(<#d(\d{4}-\d{1,2}-\d{1,2})>)')
        pattern_date_opr_str = re.compile(r'(<#d(\d{4}-\d{1,2}-\d{1,2})\s*([+-])\s*(\d+)>)')

        try:
            content = json_to_string(testcase, ensure_ascii=False)
        except Exception as e:
            log.error(string.Template("testcase json dumps fail, error info: $e").substitute(e=e))
            self.error_collector.add('datetime_translate', 'json_dumps_fail', testcase)
            raise TestcaseErrorException("testcase json dumps fail, error info is: {}".format(e))

        # 匹配时间格式，包含时分秒
        key_words_now = re.findall(pattern_now, content)
        key_words_now_opr = re.findall(pattern_now_opr, content)
        key_words_time = re.findall(pattern_time, content)
        key_words_time_opr = re.findall(pattern_time_opr, content)

        # 匹配日期格式，不包含时分秒
        key_words_date = re.findall(pattern_date, content)
        key_words_date_opr = re.findall(pattern_date_opr, content)
        key_words_date_str = re.findall(pattern_date_str, content)
        key_words_date_opr_str = re.findall(pattern_date_opr_str, content)

        # 获取当前时间
        now_time = datetime.now(tz=pytz.timezone("Asia/Shanghai"))
        now_time_str = now_time.strftime(time_format)
        date_str = now_time.strftime(date_format)
        # 获取当前日期

        if key_words_now:
            log.debug("时间替换：<#dnow()> ----> {}".format(now_time_str))
            content = content.replace(r'<#dnow()>', now_time_str)
        if key_words_now_opr:
            for key_word in key_words_now_opr:
                operation = key_word[1]
                if operation == '+':
                    _time = now_time + timedelta(minutes=float(key_word[2]))
                elif operation == '-':
                    _time = now_time - timedelta(minutes=float(key_word[2]))
                else:
                    log.error('时间运算符号不支持，不做处理')
                    self.error_collector.add('datetime_translate', '时间运算符不支持', str(key_word))
                    continue

                log.debug("时间替换：{} ----> {}".format(key_word[0], _time.strftime(time_format)))
                content = content.replace(key_word[0], _time.strftime(time_format))
        if key_words_time:
            for key_word in key_words_time:
                log.debug("时间替换：{} ----> {}".format(key_word[0], key_word[1]))
                content = content.replace(key_word[0], key_word[1])
        if key_words_time_opr:
            for key_word in key_words_time_opr:
                operation = key_word[2]
                try:
                    _datetime = datetime.strptime(key_word[1], time_format)
                except Exception as e:
                    log.error("时间字符串无法转换为strptime，请检查时间是否符合规范，默认转换为当前时间，错误信息:{}".format(str(e)))
                    self.error_collector.add('datetime_translate', '时间字符串格式异常', str(key_word[1]))
                    continue
                if operation == '+':
                    switch_time = _datetime + timedelta(minutes=float(key_word[3]))
                elif operation == '-':
                    switch_time = _datetime - timedelta(minutes=float(key_word[3]))
                else:
                    log.error('时间运算符号不支持，不做处理')
                    self.error_collector.add('datetime_translate', '时间运算符不支持', str(key_word))
                    continue
                log.debug("时间替换：{} ----> {}".format(key_word[0], switch_time.strftime(time_format)))
                content = content.replace(key_word[0], switch_time.strftime(time_format))

        if key_words_date:
            log.debug("时间替换：<#ddate()> ----> {}".format(date_str))
            content = content.replace(r'<#ddate()>', date_str)
        if key_words_date_opr:
            for key_word in key_words_date_opr:
                operation = key_word[1]
                if operation == '+':
                    _time = now_time + timedelta(days=float(key_word[2]))
                elif operation == '-':
                    _time = now_time - timedelta(days=float(key_word[2]))
                else:
                    log.error('时间运算符号不支持，不做处理')
                    self.error_collector.add('datetime_translate', '时间运算符不支持', str(key_word))
                    continue
                log.debug("时间替换：{} ----> {}".format(key_word[0], _time.strftime(date_format)))
                content = content.replace(key_word[0], _time.strftime(date_format))
        if key_words_date_str:
            for key_word in key_words_date_str:
                log.debug("时间替换：{} ----> {}".format(key_word[0], key_word[1]))
                content = content.replace(key_word[0], key_word[1])
        if key_words_date_opr_str:
            for key_word in key_words_date_opr_str:
                operation = key_word[2]
                try:
                    _datetime = datetime.strptime(key_word[1], date_format)
                except Exception as e:
                    log.error("时间字符串无法转换为strptime，请检查时间是否符合规范，默认转换为当前时间，错误信息:{}".format(str(e)))
                    self.error_collector.add('datetime_translate', '时间字符串格式异常', str(key_word[1]))
                    continue
                if operation == '+':
                    switch_date = _datetime + timedelta(days=float(key_word[3]))
                elif operation == '-':
                    switch_date = _datetime - timedelta(days=float(key_word[3]))
                else:
                    log.error('时间运算符号不支持，不做处理')
                    self.error_collector.add('datetime_translate', '时间运算符不支持', str(key_word))
                    continue
                log.debug("时间替换：{} ----> {}".format(key_word[0], switch_date.strftime(date_format)))
                content = content.replace(key_word[0], switch_date.strftime(date_format))

        try:
            json_content = str_to_json(content)
            self.testcase = json_content
            return json_content
        except Exception as e:
            log.error("testcase json loads fail, the error info: {}".format(str(e)))
            self.error_collector.add('datetime_translate', 'json_loads_fail', content)
            raise VarReplaceException

    def dyparam_parse(self, testcase: dict, var_object: object):
        """
        func: 根据dyparam里的sql信息，进行数据库查询，将查询到的结果存入var_object对象的interface_vars属性中
        :param dyparam: 测试用例中的dyparam信息经过json转换后的内容
        :param var_object: 用于存放测试sheet接口变量的对象
        :return: 添加了从数据库中查询出来的值之后的var_object对象
        """
        if not isinstance(testcase, dict):
            self.error_collector.add('dyparam_parse', 'testcase_error', str(testcase))
            raise TestcaseErrorException("testcase is not a dict")
        dyparam = testcase.get('dyparam')
        if not dyparam:
            return None
        if not isinstance(dyparam, dict):
            self.error_collector.add('dyparam_parse', 'dyparam_error', str(dyparam))
            raise TestcaseErrorException("dyparam is not a dict type")
        if not hasattr(var_object, "interface_vars"):
            var_object.interface_vars = {}
        log.info('进行dyparam解析')
        for name_, sql_info in dyparam.items():
            ip = sql_info.get('ip')
            port = sql_info.get('port')
            pwd = sql_info.get('pwd')
            user = sql_info.get('user')
            db_type = sql_info.get('db_type')
            values = sql_info.get('values')
            sql = sql_info.get('sql')
            rs = DbHelper().query(ip=ip, port=port, user=user, pwd=pwd, db_type=db_type, sql=sql)
            if not rs:
                log.warning("sql: {} 查询结果为空".format(sql))
                for var_name, reslut_key in values.items():
                    var_object.interface_vars[var_name] = ""
                continue

            rs = rs[0]
            try:
                for var_name, reslut_key in values.items():
                    log.info('添加interface_var: {}={}'.format(var_name, rs.get(reslut_key)))
                    var_object.interface_vars[var_name] = rs.get(reslut_key)
            except Exception as e:
                self.error_collector.add('dyparam_parse', 'add_interface_vars_fail', e)
                log.error('add interface_vars fail, error info is: {}'.format(e))
                return False
        return var_object

    def var_replace(self, testcase=None, object_list=None):
        """
        功能：解析测试用例中是否存在需要变量替换的字符串
        流程：根据传入的用例和需要检查的对象列表，判断对象列表中是否包含有用例中需要转换的变量字符串，如果有，则将对应的字符串转换为对应的变量值
        """
        if not testcase:
            testcase = self.testcase
        else:
            testcase = testcase
        if not object_list:
            object_list = self.object_list
        else:
            object_list = object_list
        if not isinstance(testcase, dict):
            self.error_collector.add('var_replace', 'testcase_error', testcase)
            raise TestcaseErrorException('testcase is not a dict format')
        if not isinstance(object_list, list):
            self.error_collector.add('var_replace', 'object_list_error', object_list)
            raise TestcaseErrorException("object list is not a list object")
        # self._add_vars_by_testcase_params_header()
        # object_list.append(self)
        pattern_front = re.compile(r"@{")
        pattern_back = re.compile(r"@}")
        random_front = generate_random_str()
        random_back = generate_random_str()
        try:
            content = json_to_string(testcase, ensure_ascii=False)
        except Exception as e:
            self.error_collector.add('var_replace', 'json_dumps_fail', testcase)
            log.error(string.Template("testcase json dumps fail, error info: $e").substitute(e=e))
            raise VarReplaceException
        content = re.sub(pattern_front, random_front, content)
        content = re.sub(pattern_back, random_back, content)
        # log.debug(string.Template("after replaced random string: $content").substitute(content=content))
        pattern = re.compile(r"\{\w+\}")
        key_words = re.findall(pattern, content)
        log.debug(string.Template("所有需要进行变量替换的变量为: $key_words").substitute(key_words=key_words))

        if key_words:
            """
            循环遍历所有待替换的字符，如果待替换的字符在传入的对象列表中有对应的属性，则进行替换
            否则不作处理
            对象替换按传入的对象的下标进行排序，匹配到了之后，退出循环，即取最先匹配到的对象的属性值
            """
            for key_word in key_words:
                real_word = key_word.lstrip('{').rstrip('}')
                for index in range(0, len(object_list)):
                    if not object_list[index]:
                        continue
                    log.debug(Template("$o对象的interface_vars属性$a").substitute(o=object_list[index].__class__.__name__,
                                                                a=object_list[index].__dict__.get('interface_vars')))
                    if not hasattr(object_list[index], "interface_vars"):
                        log.debug(Template("$o对象没有interface_vars属性").substitute(o=object_list[index]))
                        continue
                    attr_dict = object_list[index].__dict__
                    interface_var_dict = attr_dict["interface_vars"]  # 获取对象的所有属性值
                    if real_word in interface_var_dict:
                        log.debug(Template("正在替换变量：$s").substitute(s=real_word))
                        content = content.replace(key_word, str(interface_var_dict[real_word]))
                        break

        content = content.replace(random_front, r'{')
        content = content.replace(random_back, r'}')
        try:
            json_content = str_to_json(content)
            self.testcase = json_content
            return json_content
        except Exception as e:
            self.error_collector.add('var_replace', 'json_loads_fail', (e, content))
            log.error("testcase json loads fail, the error info: {}, the content is: {}".format(e, content))
            raise VarReplaceException

    def mathematical_parse(self, testcase: dict):
        """
        func: 將符合 "<#math>非空字符" 格式的用例字符進行数学运算，并用运算后的结果替换原来的字符
        :param testcase: 测试用例
        :return: 转换后的测试用例
        """
        log.info('start to parse mathematical')
        try:
            content = json_to_string(testcase, ensure_ascii=False)
        except Exception as e:
            self.error_collector.add('mathematical_parse', 'json_dumps_fail', (e, testcase))
            log.error(string.Template("testcase json dumps fail, error info: $e").substitute(e=e))
            raise TestcaseErrorException

        pattern = re.compile(r'((\\")?<#math>\s*([^\\\'"]+)(\\")?)')
        log.debug(content)
        key_word_list = re.findall(pattern, content)
        if key_word_list:
            for key_word in key_word_list:
                log.debug(key_word)
                exp = key_word[2].replace("\\'", '').replace('\\"', '')
                word = key_word[0]
                try:
                    res = str(eval(exp))
                    log.info('运算表达式：{} 运算后的结果为：{}'.format(exp, res))
                    content = content.replace(word, res)
                except Exception as e:
                    self.error_collector.add('mathematical_parse', '运算表达式执行出错', (e, exp))
                    log.error('{} 运算表达式执行出错，错误信息：{}'.format(exp, e))
        try:
            content_json = str_to_json(content)
            self.testcase = content_json
            return content_json
        except Exception as e:
            self.error_collector.add('mathematical_parse', 'json_loads_fail', (e, content))
            log.error('mathematical_parsed format json fail, the error info is: {}'.format(e))
            raise VarReplaceException

    def generate_str_by_regular(self, testcase: dict):
        """
        func: 将用例中需要根据给定正则表达式生成符合条件随机字符串的字段进行转换
        :param testcase: 测试用例
        :return: 转换后的测试用例
        """
        log.info('start to switch regular rule')
        testcase = testcase
        xeger_obj = Xeger(limit=10)
        try:
            content = json_to_string(testcase, ensure_ascii=False)
        except Exception as e:
            self.error_collector.add('generate_str_by_regular', 'json_dumps_fail', (e, testcase))
            log.error(string.Template("testcase json dumps fail, error info: $e").substitute(e=e))
            raise TestcaseErrorException

        pattern = re.compile(r'(<#regstr>(\S+))')
        key_word_list = re.findall(pattern, content)
        if key_word_list:
            for key_word in key_word_list:
                try:
                    item = '\\'.join(key_word[1].split('\\\\'))
                    log.info('进行正则表达式转换：{}'.format(item))
                    random_str = xeger_obj.xeger(item)
                    content = content.replace(key_word[0], random_str)
                except Exception as e:
                    self.error_collector.add('generate_str_by_regular', '生成正则表达式失败', (e, key_word[1]))
                    log.error('{}正则表达式规则生成字符串失败，失败原因:{}'.format(key_word[1], e))
        log.debug('转换后的内容：{}'.format(content))
        try:
            json_content = str_to_json(content)
            self.testcase = json_content
            return json_content
        except Exception as e:
            self.error_collector.add('generate_str_by_regular', 'json_loads_fail', (e, content))
            log.error("generate_str_by_regular testcase json loads fail, the error info: {}".format(str(e)))
            raise TestcaseErrorException

    def add_random_num_for_case(self, testcase: dict):
        """
        :func 根据规则<#p>\d 生成随机的数字
        :param testcase:
        :return:
        """
        log.info('start to switch the random num')
        try:
            content = json_to_string(testcase, ensure_ascii=False)
        except Exception as e:
            self.error_collector.add('add_random_num_for_case', 'json_dumps_fail', (e, testcase))
            log.error(string.Template("testcase json dumps fail, error info: $e").substitute(e=e))
            raise TestcaseErrorException

        pattern = re.compile(r'(<#p>(\S+))')
        key_word_list = re.findall(pattern, content)
        if key_word_list:
            for key_word in key_word_list:
                random_str = '\\'.join(key_word[1].split('\\\\'))
                log.info('随机数字替换前的内容为：{}'.format(random_str))
                for i in random_str.split('\\d'):
                    random_str = random_str.replace('\\d', str(random.randint(0, 9)), 1)
                log.info('随机数字替换后的内容为：{}'.format(random_str))
                content = content.replace(key_word[0], random_str)
        log.debug('转换后的内容：{}'.format(content))
        try:
            json_content = str_to_json(content)
            self.testcase = json_content
            return json_content
        except Exception as e:
            self.error_collector.add('add_random_num_for_case', 'json_loads_fail', (e, content))
            log.error("generate_str_by_regular testcase json loads fail, the error info: {}".format(str(e)))
            raise TestcaseErrorException

    def _add_vars_by_testcase_params_header(self):
        """
        func: 将测试用例中的params和header中的参数，添加到用例变量中
        该方法暂未使用
        :return:
        """
        testcase = self.testcase
        params = testcase['params']
        header = testcase['header']
        if params:
            for k, v in params.items():
                self.interface_vars[k] = v
        if header:
            for k, v in header.items():
                self.interface_vars[k] = v

    def pre_process(self, testcase, object_list, caller: object = None):
        """
        :func: 用例api请求前的处理程序
        :param testcase:
        :param object_list:
        :param caller:
        :return:
        """
        ivs = TmpObj()
        civs = TmpObj()
        log.info('start to pre process')
        if not isinstance(testcase, dict):
            log.error('testcase is not a dict type')
            return testcase
        if not isinstance(object_list, list):
            log.error('object_list is not list type')
            return testcase
        for obj in object_list:
            if obj.__class__.__name__ == "InterfaceVars":
                log.debug('InterfaceVars is: {}'.format(obj.interface_vars))
                ivs = obj
            elif obj.__class__.__name__ == "CommonInterfaceVars":
                log.debug('CommonInterfaceVars is: {}'.format(obj.interface_vars))
                civs = obj
            else:
                log.error("this object type is not supported")

        testcase = testcase
        self.object_list = object_list
        # 如果需要处理的内容不包含InterfaceVars这个对象，则用例变量和动态变量存储到CommonInterfaceVars中
        if not isinstance(ivs, TmpObj):
            prior_ivs = ivs
        else:
            prior_ivs = civs
        try:
            testcase = self.add_random_str_for_var(testcase)
            testcase = self.add_random_num_for_case(testcase)
            testcase = self.datetime_translate(testcase)
            testcase = self.generate_str_by_regular(testcase)
            self.parse_case_vars(testcase, prior_ivs)
            self.dyparam_parse(testcase, prior_ivs)
            testcase = self.var_replace(testcase, [ivs, civs])
            testcase = self.mathematical_parse(testcase)
        except TestcaseErrorException:
            # log.error('testcase is ill-formatted')
            pass
        except VarReplaceException:
            pass
            # log.error('var replace error')
        except Exception as e:
            log.error('pre process testcase has Exception, error info is: {}'.format(str(e)))
            self.error_collector.add('not_detail_exception', 'pre_process', e)

        if caller:
            setattr(caller, 'error_collector', None)  # first: clear the error_collector of caller
            setattr(caller, 'error_collector', self.error_collector)
        return testcase

    def store_global_vars(self, global_vars: dict, store_obj: object):
        """
        author:lfq
        :func 对全局变量进行preprocess处理
        :param global_vars: 全局变量内容，dict格式
        :param store_obj: 用于保存全局变量内容的对象
        :return:store_obj
        """
        log.info('start to parse global vars')
        if not global_vars:
            log.info('global vars is empty')
            return
        if not hasattr(store_obj, 'interface_vars'):
            store_obj.interface_vars = {}

        log.info('before pre process, the global vars is: {}'.format(global_vars))

        global_vars = self.pre_process(global_vars, [], store_obj)
        log.info('after pre process, the global vars is: {}'.format(global_vars))
        for ky, val in global_vars.items():
            store_obj.interface_vars[ky] = val
        log.info('store obj interface_vars attr info is: {}'.format(store_obj.interface_vars))
        return store_obj

    def store_local_var(self, local_vars: list, store_obj: object, common_obj: object):
        """
        :func 预处理local_vars，在local var局部变量在正式被使用之前，先进行变量替换、特殊格式转换等操作，并将处理之后的local_vars
        存储到测试套的变量存储对象中
        :param local_vars: 测试套的local_vars
        :param store_obj: 测试套用来存储变量的对象
        :param common_obj: 初始化测试套用来存储变量的对象
        :return: 添加了local_vars之后的store_obj
        """
        log.info('start to parse local vars')
        if not local_vars:
            log.info('local vars is empty')
            return

        if not hasattr(store_obj, 'interface_vars'):
            log.info('store_obj has no interface_vars attribute')
            store_obj.interface_vars = {}
        for lv in local_vars:
            if not isinstance(lv, dict):
                log.error('local vars is not a dict, do not store, the local vars info is: {}'.format(lv))
                continue

            lv = self.pre_process(lv, [common_obj], store_obj)
            log.debug('the local vars is: {} after pre process'.format(lv))
            store_obj.interface_vars[list(lv.keys())[0]] = list(lv.values())[0]
        return store_obj

    def read_task_common_global_vars(self, caller: object = None):
        """
        func: 读取由全局初始化用例和全局变量生成的全局变量内容
        :return: json化后的全局变量内容
        """
        from configs.settings import save_global_var_tmp_file
        gvs = None
        if os.path.isfile(save_global_var_tmp_file):
            try:
                with open(save_global_var_tmp_file, 'r', encoding='utf-8') as f:
                    gvs = str_to_json(f.read())

            except Exception as e:
                log.error('read task common global vars error,the error info is: {}'.format(e))
                self.error_collector.add('read_global_vars', 'exception', e)
        if caller:
            setattr(caller, 'error_collector', None)
            setattr(caller, 'error_collector', self.error_collector)

        return gvs



def generate_random_str(length=16):
    """
    func: 生成随机字符串
    :param length: 字符串的长度
    :return: 随机字符串
    """
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


class PostProcess(object):
    def __init__(self):
        self.testcase = None
        self.response = None
        self.ivs = TmpObj()
        self.civs = TmpObj()
        self.container = ErrorCollector()

    def parse_interface_var(self, testcase=None, response=None, object_=None) -> object:
        """
        func: 解析接口变量，如果测试用例中存在接口变量，则从api响应结果中查找对应的响应值，存储到测试文件的接口变量中
        :param testcase: 需要解析的测试用例
        :param response: api请求响应内容
        :param object_: 接收接口变量属性值存储的对象
        :return: 增加接口变量后的对象
        """
        log.info('start to parse interface var')
        if not testcase:
            testcase = self.testcase
        if not response:
            response = self.response
        if not object_:
            object_ = self.ivs
        if not isinstance(testcase, dict) and not isinstance(response, dict):
            return 'testcase or response is not a dict, testcase type is: {}, response type is: {}'\
                .format(type(testcase), type(response))
        if not hasattr(object_, 'interface_vars'):
            object_.interface_vars = {}
        interface_var = testcase.get('interface_var')
        if interface_var:
            for k, v in interface_var.items():
                try:
                    res = json_search(v, response)
                    log.info('parse interface var: {}, value is: {}'.format(k, res))
                    if isinstance(res, list):
                        object_.interface_vars[k] = res[0]
                    elif res is None:
                        object_.interface_vars[k] = 'None'
                    else:
                        object_.interface_vars[k] = res
                except Exception as e:
                    log.error(
                        string.Template("get interface_var:$v from response fail,error info: $e").substitute(v=v, e=e))
        return object_

    def post_process(self, testcase, response, object_list):
        """
        func: 用例执行完请求后的处理程序
        :param testcase:
        :param response:
        :param object_list:
        :return:
        """
        if not isinstance(testcase, dict) or not isinstance(response, dict) or not isinstance(object_list, list):
            log.error('params type error')
            return testcase
        for obj in object_list:
            if obj.__class__.__name__ == "InterfaceVars":
                self.ivs = obj
            elif obj.__class__.__name__ == "CommonInterfaceVars":
                self.civs = obj
            else:
                log.error('this object type is not supported')
        self.testcase = testcase
        self.response = response
        if not isinstance(self.ivs, TmpObj):
            prior_ivs = self.ivs
        else:
            prior_ivs = self.civs
        self.parse_interface_var(self.testcase, self.response, prior_ivs)


class ResultProcess(object):
    def __init__(self):
        pass

    def result_check(self, testcase, response):
        error_info = ""
        flag = True
        if not isinstance(testcase, dict):
            log.error('params type error')
            error_info += "testcase or response params type error"
            return False, error_info
        try:
            res_json = response.json()
        except Exception as e:
            log.error('响应结果验证失败，错误信息：响应内容转换为json格式异常，异常信息：{}, 响应内容：{}'.format(e, response.text))
            return False, '响应结果验证失败，错误信息：响应内容转换为json格式异常，异常信息：{}, 响应内容：{}'.format(e, response.text)
        verify_fields = testcase.get('verify_fields')
        res_text = testcase.get('res_text')
        res_header = testcase.get('res_header')
        status_code = testcase.get('status_code')
        res_time = testcase.get('res_time')
        expression = testcase.get('expression')
        db_verify = testcase.get('db_verify')
        if verify_fields:
            res = self.check_verify_fields(verify_fields, res_json)
            if res:
                flag = False
                error_info += res + "\n"
            else:
                error_info += "响应字段验证成功\n"
        if res_text:
            res = self.check_response_text(res_text, res_json)
            if res:
                flag = False
                error_info += res + "\n"
            else:
                error_info += "响应内容验证成功\n"
        if res_header:
            res = self.check_response_header(res_header, response.headers)
            if res:
                flag = False
                error_info += res + "\n"
            else:
                error_info += "响应头验证成功\n"
        if status_code:
            res = self.check_status_code(status_code, response.status_code)
            if res:
                flag = False
                error_info += res + "\n"
            else:
                error_info += "响应状态码验证成功\n"
        if res_time:
            res = self.check_response_time(res_time, response.elapsed.total_seconds())
            if res:
                flag = False
                error_info += res + "\n"
            else:
                error_info += "响应时间验证成功\n"
        if expression:
            res = self.check_pyexpression(expression, res_json)
            if res:
                flag = False
                error_info += res + "\n"
            else:
                error_info += "py表达式验证成功\n"
        if db_verify:
            res = self.check_db_verify(db_verify)
            if res:
                flag = False
                error_info += res + "\n"
            else:
                error_info += "数据库验证成功\n"
        return flag, error_info

    @classmethod
    def _json_compare(cls, key, val, res):
        res = json_search(key, res)
        if isinstance(res, list):
            res = res[0]
        if str(val).lower() != str(res).lower():
            return False
        else:
            return True

    @classmethod
    def _reg_compare(cls, key, val, res):
        val = '\\'.join(val.lstrip('<#reg>').split('\\'))
        res = json_search(key, res)
        if isinstance(res, list):
            res = str(res[0])
        else:
            res = str(res)
        if not re.match(val, res, re.IGNORECASE):
            log.info('正则表达式匹配失败，待匹配字符：{}，响应内容：{}'.format(key, res))
            return False
        else:
            return True

    def check_verify_fields(self, fields, response):
        error_info = ""
        if not fields:
            return error_info
        if not isinstance(fields, dict):
            return "响应字段验证失败，错误信息：入参类型错误"

        for k, v in fields.items():
            if not str(v).startswith('<#reg>'):
                try:
                    if not self._json_compare(k, v, response):
                        error_info += "响应字段验证失败，错误信息： {} 不等于 {}, 响应值是: {}".format(k, v, str(json_search(k, response)))
                except Exception as e:
                    error_info += "响应字段验证失败，错误信息：对比结果{}时出现异常，异常信息:{}".format(k, e)
            else:
                try:
                    if not self._reg_compare(k, v, response):
                        error_info += "响应字段验证失败，错误信息：验证{}时，响应结果使用正则表达式匹配失败，请检查".format(k)
                except Exception as e:
                    error_info += "响应字段验证失败，错误信息：验证{}时，响应结果使用正则表达式匹配异常，异常信息：{}".format(k, e)
        return error_info

    @classmethod
    def check_response_text(cls, fields, response):
        error_info = ""
        log.debug(Template("fields: $fields, response: $response").substitute(fields=fields, response=response))
        if not fields:
            return error_info
        if isinstance(fields, str):
            log.debug('is a string fields, value is:'.format(fields))
            fs = fields.split(',')
        elif isinstance(fields, list):
            log.debug('is a list fields, value is: '.format(str(fields)))
            fs = fields
        else:
            log.error('fields param type error')
            return '响应内容验证失败，错误信息：入参类型错误'
        for text in fs:
            if not text:
                continue
            text = text.lstrip("'").lstrip('"').rstrip("'").rstrip('"')
            if text:
                log.debug(Template("待校验的内容: $text").substitute(text=text))
                if isinstance(response, dict):
                    try:
                        isempty = json_search(text, response)

                        if isempty is None:
                            error_info += Template("响应内容验证失败，错误信息：接口响应内容没有待校验的字段:$t，"
                                                   "响应内容:$res").substitute(t=text, res=response)
                    except Exception as e:
                        error_info += "响应字段验证失败，错误信息：对比结果{}时出现异常，异常信息:{}".format(text, e)
                else:
                    if text not in response:
                        error_info += Template("响应内容验证失败，错误信息：接口响应内容没有待校验的字段:$t，"
                                               "响应内容:$res").substitute(t=text, res=response)

        return error_info

    def check_response_header(self, fields, headers):
        error_info = ""
        if not fields:
            return error_info
        if not isinstance(fields, dict):
            return "响应头验证失败，错误信息：入参类型错误"

        for k, v in fields.items():
            if str(v).startswith('<#reg>'):
                try:
                    if not self._reg_compare(k, v, headers):
                        error_info += "响应头验证失败，错误信息：验证{}时，响应结果使用正则表达式匹配失败，请检查，响应头是：{}".format(k, headers)
                except Exception as e:
                    error_info += "响应头验证出错，错误信息：对比结果{}时出现异常，异常信息:{}".format(k, e)
            else:
                try:
                    if not self._json_compare(k, v, headers):
                        error_info += "响应头验证失败，错误信息： {} 不等于 {}, 响应头是: {}".format(k, v, headers)
                except Exception as e:
                    error_info += "响应头验证出错，错误信息：对比结果{}时出现异常，异常信息:{}".format(k, e)
        return error_info

    @classmethod
    def check_status_code(cls, code, res_code):
        error_info = ""
        if not code:
            return error_info
        try:
            code = int(code)
        except Exception as e:
            log.error(Template("响应状态码验证失败，错误信息：接口响应状态码入参错误，请检查, 入参值：$code").substitute(code=code))
            error_info += Template("响应状态码验证失败，错误信息：接口响应状态码入参错误，请检查, 入参值：$code").substitute(code=code)
            return error_info
        if code != res_code:
            error_info += Template("响应状态码验证失败，错误信息：接口响应码校验失败:预期值：$n，"
                                   "响应值:$res").substitute(n=code, res=res_code)
        return error_info

    @classmethod
    def check_response_time(cls, _time, res_time):
        error_info = ""
        if not _time:
            return error_info
        try:
            _time = float(_time)
            if _time < res_time:
                log.error(Template("响应时间验证失败，错误信息：接口响应时间超时，期望值: $t， 响应值: $r").substitute(t=_time, r=res_time))
                error_info += Template("响应时间验证失败，错误信息：接口响应时间超时，期望值: $t， 响应值: $r").substitute(t=_time, r=res_time)
                return error_info
        except Exception as e:
            log.error(Template("响应时间验证失败，错误信息：接口响应时间入参错误，请检查: $t").substitute(t=_time))
            error_info += Template("响应时间验证失败，错误信息：接口响应时间入参错误，请检查: $t").substitute(t=_time)
            return error_info

    @classmethod
    def check_pyexpression(cls, pys, response):
        error_info = ""
        response = response
        exe_pys = []
        if not pys:
            return error_info
        if isinstance(pys, list):
            exe_pys = pys
        elif isinstance(pys, str):
            exe_pys.append(pys)
        else:
            error_info += "py表达式验证失败，错误信息：py表达式入参错误，参数仅支持列表和字符串格式"
            return error_info
        for py in exe_pys:
            try:
                if not eval(py):
                    log.error(Template("py表达式验证失败，错误信息：py表达式执行失败，表达式内容：$py").substitute(py=py))
                    error_info += (Template("py表达式验证失败，错误信息：py表达式执行失败，表达式内容：$py").substitute(py=py))
            except Exception as e:
                error_info += Template("py表达式验证失败，错误信息：执行py表达式异常，表达式内容：$py, 异常信息：$e").substitute(py=py, e=e)

        return error_info

    @classmethod
    def check_db_verify(cls, sql_info):
        if not isinstance(sql_info, dict):
            return '数据库验证失败，错误信息：sql_info 入参类型错误，请传入dict类型'
        error_info = ""

        for check_name, sql_dict in sql_info.items():
            type_ = sql_dict.get('type') or '='
            ip = sql_dict.get('ip')
            port = sql_dict.get('port')
            pwd = sql_dict.get('pwd')
            user = sql_dict.get('user')
            db_type = sql_dict.get('db_type')
            check_values = sql_dict.get('check') or {}
            sql = sql_dict.get('sql')
            rs = DbHelper().query(ip=ip, port=port, user=user, pwd=pwd, db_type=db_type, sql=sql)
            if not rs:
                error_info += "数据库验证失败，错误信息：sql: {} 查询结果为空".format(sql)
                continue

            if type_ == "=" or type_ == "==":
                rs = rs[0]
                for k, v in check_values.items():
                    if str(rs.get(k)) != str(v):
                        log.error("数据库验证失败，错误信息：数据库验证失败，预期结果：{}等于{}, 查询结果：{}".format(k, v, rs))
                        error_info += "数据库验证失败，错误信息：数据库验证失败，预期结果：{}等于{}, 查询结果：{}\n".format(k, v, rs)
            elif type_ == "!" or type_ == "!=":
                rs = rs[0]
                for k, v in check_values.items():
                    if str(rs.get(k)) == str(v):
                        log.error("数据库验证失败，错误信息：数据库验证失败，预期结果：{}不等于{}, 查询结果：{}".format(k, v, rs))
                        error_info += "数据库验证失败，错误信息：数据库验证失败，预期结果：{}不等于{}, 查询结果：{}\n".format(k, v, rs)

            elif type_ == "~" or type_ == "~=":
                for k, v in check_values.items():
                    flag = False
                    for r in rs:
                        if str(r[k]) == str(v):
                            flag = True
                            break
                    if not flag:
                        log.error('数据库验证失败，错误信息：数据库验证失败，预期值：{}包含{},查询结果:{}'.format(k, v, rs))
                        error_info += '数据库验证失败，错误信息：数据库验证失败，预期值：{}包含{},查询结果:{}\n'.format(k, v, rs)

            elif type_ == "!~" or type_ == "~!":
                for k, v in check_values.items():
                    flag = True
                    for r in rs:
                        if str(r[k]) == str(v):
                            flag = False
                            break
                    if not flag:
                        log.error('数据库验证失败，错误信息：数据库验证失败，预期值：{}不包含{},查询结果:{}'.format(k, v, rs))
                        error_info += '数据库验证失败，错误信息：数据库验证失败，预期值：{}不包含{},查询结果:{}\n'.format(k, v, rs)
            else:
                log.error('数据库验证失败，错误信息：数据库验证类型不支持，请检查')
                error_info += "数据库验证失败，错误信息：数据库验证类型不支持，请检查"

        return error_info
