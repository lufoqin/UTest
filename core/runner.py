# -*- coding: utf-8 -*-
import json
import os
import shutil
import sys
import pytest
import pytz
from configs import settings
from datetime import datetime
from core.case_parse.base import Process
from core.case_parse.generator import Generator
from core.utils.common_tools import json_to_string, str_to_json
from core.logs import log
from core.translate import Translate
from core.results import ResultSave, AllureReport
from core.message_notify import MsgNotify


class Runner(object):
    def __init__(self, case_type, filepath):
        self.case_type = case_type
        self.filepath = filepath
        self.project_tmp_dir = settings.project_tmp_dir
        self.test_result_tmp_dir = settings.test_result_tmp_dir
        self.task_common_test_file_path = \
            os.path.join(settings.current_path, "testcase", "auto_create", "task_common.py")
        self._prepare()
        self.msg_notify = MsgNotify()

    def run(self, **kwargs):
        log.info('=================start=================')
        if self.case_type == 'old':
            self._run_translate()
        else:
            self._run_test(**kwargs)

    def _prepare(self):
        """
        正式执行任务前的预处理
        :return:
        """
        # 清空.tmp目录并重新创建
        shutil.rmtree(self.project_tmp_dir, ignore_errors=True)
        os.makedirs(self.project_tmp_dir)
        os.makedirs(self.test_result_tmp_dir)

    def _post(self):
        """

        :return:
        """
        pass

    def _create_testcase_file(self):
        """
        func: 根据excel文件生成测试用例文件
        :return:
        """
        testsuites = Process(filepath=self.filepath)
        gn = Generator(testsuites)
        gn.generate_common_test()
        gn.generate_testsuite()

    def _run_task_common_init_testcase(self, allure_report_dir):
        """
        func: 执行初始化测试套和恢复测试套的用例
        初始化和恢复用例的测试文件路径存放在<project_dir>/testcase/auto_create/task_common.py
        初始化测试套的用例执行完毕后，将获取的全局变量和用例接口变量写入临时文件中，待后续其他测试用例使用
        :return:
        """

        from testcase.auto_create.task_common import common_interface_vars
        test_module = "{}::TestInitSteps".format(self.task_common_test_file_path)
        log.info('run the task init steps')
        pytest.main([test_module, "-v", "-s", "--alluredir={}".format(allure_report_dir)])
        global_vars_save_path = settings.project_tmp_dir
        if not os.path.isdir(global_vars_save_path):
            os.makedirs(global_vars_save_path)
        log.info('all the global vars is: {}'.format(common_interface_vars.interface_vars))
        with open(settings.save_global_var_tmp_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(common_interface_vars.interface_vars, ensure_ascii=False))

    def _run_task_common_clear_testcase(self, allure_report_dir):
        test_module = "{}::TestClearSteps".format(self.task_common_test_file_path)
        log.info('run the task clear steps')
        pytest.main([test_module, "-v", "-s", "--alluredir={}".format(allure_report_dir)])
        # log.info('remove global vars tmp file')
        # if os.path.isfile(settings.save_global_var_tmp_file):
        #     os.remove(settings.save_global_var_tmp_file)

    def _run_test(self, **kwargs):
        filepath = self.filepath
        platform = kwargs.get('platform') or "default"
        allure_results_path = kwargs.get("allure_results_path")
        is_open_serve = kwargs.get('is_open_serve') or "open"
        num_processes = kwargs.get('num_processes') or 'auto'

        start_time = datetime.now(tz=pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.split(filepath)[1].rstrip('.xls').rstrip('.xlsx')  # 测试用例名，后续保存测试结果需要用到

        #  测试报告路径默认在report/[测试文件名]/里，文件名以当时的时间为名字
        # 如果是通过jenkins开始任务的，allure的报告存放到jenkins的home目录下
        if platform == 'jenkins':
            allure_report_dir = allure_results_path or os.path.join(settings.allure_reports_path, filename, start_time)
        else:
            allure_report_dir = os.path.join(settings.allure_reports_path, filename, start_time)

        excel_report_file = os.path.join(settings.excel_reports_path, filename, "Excel", start_time + ".xls")

        log.info('**********start to create testcase file**********')
        self._create_testcase_file()

        log.info('**********start to execute testcase***********')
        self._run_task_common_init_testcase(allure_report_dir)
        if str(num_processes) == '0':
            run_cmd = ["./testcase/auto_create", "-v", "-s", "--alluredir={}".format(allure_report_dir)]
        else:
            run_cmd = ["./testcase/auto_create", "-v", "-s", "-n", "{}".format(num_processes), "--dist", "loadfile",
                     "--alluredir={}".format(allure_report_dir)]

        pytest.main(run_cmd)  # pytest的启动入口

        self._run_task_common_clear_testcase(allure_report_dir)
        excel_report_file = ResultSave().gen_excel_report(excel_report_file)  # 保存测试结果到Excel文件
        self._read_test_summary()
        if platform == 'jenkins':
            server_url = '请通过jenkins主页查看，访问url：http://192.168.215.94:8080'
        else:
            server_url = AllureReport().create_allure_report(allure_report_dir,
                                                             isopen=is_open_serve)  # 生成allure测试报告，并打开报告服务
        end_time = datetime.now(tz=pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d_%H-%M-%S")
        report_text = """测试开始时间: {}\n测试结束时间: {}\n测试用例文件名: {}\n测试报告保存路径:\n    Excel: {},\n   allure: {}\n测试报告服务地址: {}\n
    """.format(start_time, end_time, os.path.split(filepath)[1], os.path.split(excel_report_file)[1],
               os.path.split(allure_report_dir)[1], server_url)

        self.msg_notify.send_reports(report_text, excel_report_file)  # 根据Excel中的配置，发送钉钉消息和邮件通知

    def _read_test_summary(self):
        with open(settings.test_result_summary_file, 'r', encoding='utf-8') as f:
            report_info = str_to_json(f.read())
            self.msg_notify.set_testresult(**report_info)

    def _run_translate(self):
        """
        解析旧平台用例的入口
        :return: 处理完后，会在日志结尾处提示新生成的新用例的路径
        """
        Translate(self.filepath).parse_case()
