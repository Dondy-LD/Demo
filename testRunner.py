#! /usr/bin/env/python3
# _*_coding:utf-8_*_

import os
import subprocess
from ncsqa import qasummaryreport

root_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))


def run_tests():
    #command = "pytest -s " + os.path.join(root_path, "cases", "test_cases.py::TestCases") + " --html=" + os.path.join(root_path, "reports", "qa_testing_report.html")
    command_pre = "pytest -s " + os.path.join(root_path, "cases", "test_cases.py::TestCases::test_precondition") + " --html=" + os.path.join(root_path, "reports", "qa_testing_report1.html")
    # command = "pytest -s " + os.path.join(root_path, "cases", "test_cases.py::TestCases::test_cases") + " --html=" + os.path.join(root_path, "reports", "qa_testing_report2.html")
    command_allure = "pytest -s " + os.path.join(root_path, "cases", "test_cases.py::TestCases") + " --alluredir=" \
                     + os.path.join(root_path, "allure_results")
    command_td = "pytest -s " + os.path.join(root_path, "cases", "test_cases.py::TestCases::test_teardown") + " --html=" + os.path.join(root_path, "reports", "qa_testing_report3.html")
    subprocess.run(command_pre, shell=True)
    # subprocess.run(command, shell=True)
    subprocess.run(command_allure, shell=True)
    subprocess.run(command_td, shell=True)
    # subprocess.run(command, shell=True)
    # command_generate_report = "allure generate " + os.path.join(root_path, "allure_results") + " -o " + os.path.join(
    #     root_path, "allure_report") + " --clean"
    # subprocess.run(command_generate_report, shell=True)


if __name__ == "__main__":
    run_tests()
    qasummaryreport.final_testing_job_result(os.path.join(root_path, "reports", "qa_testing_report.html"))  # To parse html report to get final result (True/False) of audit service testing