# -*- coding: utf-8 -*-
import os
import sys
import argparse
from core.logs import log
from core.runner import Runner


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('-f', '--file', help='excel file path', required=True)  # 需要处理的excel文件
    #  进行处理的类型：old：转换旧平台的用例，new：执行新平台的用例，默认为new
    args.add_argument('-t', '--type', help='old or new. --old platform testcase,will convert to the new platform '
                                           'testcase;  --new: Generate test cases using Excel files and execute them.'
                                           'default:new')

    args.add_argument('-p', '--platform', help='what platform does it run on, optional: default, jenkins')
    args.add_argument('-a', '--allure_results', help='where is the allure results path')
    args.add_argument('-s', '--open_allure_serve', help='whether to open the allure serve, default is true')
    args.add_argument('-n', '--num_processes', help='set the numbers of multiple processes to run tests, default is '
                                                    'use as many processes as your computer has CPU cores')

    parse = args.parse_args()
    file_path = os.path.abspath(parse.file)
    # file_path = os.path.abspath('./testcase/一体化云柜机接口用例.xls')
    type_ = parse.type if parse.type else "new"
    by_platform = parse.platform if parse.platform else "default"
    allure_results_path = parse.allure_results
    open_allure_serve = parse.open_allure_serve or "open"
    num_processes = parse.num_processes or 'auto'
    log.debug('processes_num: {}'.format(num_processes))
    try:
        if num_processes == 'auto':
            pass
        elif int(num_processes) >= 0:
            num_processes = str(int(num_processes))
        else:
            log.error('-n/--num_processes value is invalid,exit')
            sys.exit(-1)
    except ValueError:
        log.error('-n/--num_processes value is invalid,exit')
        sys.exit(-1)

    kwargs = {"platform": by_platform,
              "allure_results_path": allure_results_path,
              "is_open_serve": open_allure_serve,
              "num_processes": num_processes
              }

    if type_ == "new" or type_ == "old":
        Runner(type_, file_path).run(**kwargs)
    else:
        log.error("the arg of type is invalid, only support 'new' or 'old'")
        print("the arg of type is invalid, only support 'new' or 'old'")
        sys.exit(-1)

