from bs4 import BeautifulSoup
import pytest
import os


@pytest.mark.skip(reason="hello")
def test_retrieve_data():
    soup = BeautifulSoup(open("test_event_subscribe.html"), "html.parser")
    status = ['passed', 'skipped', 'failed', 'xfailed', 'xpassed', 'rerun']
    summary = {}
    totalcase = 0
    for item in status:
        soupel = soup.find('span', attrs={'class': item})
        if soupel is not None:
            summary[item] = soupel.string[0]
            totalcase += int(soupel.string[0])

    summary["total"] = str(totalcase)

    print(summary)


def final_testing_job_result(report_file):
    try:
        report_file = open(report_file, encoding='utf-8')
        soup = BeautifulSoup(report_file, "html.parser")
        failed = soup.find('span', attrs={'class': 'failed'})
        xfailed = soup.find('span', attrs={'class': 'xfailed'})
        error = soup.find('span', attrs={'class': 'error'})
        _failednum = 0
        _xfailednum = 0
        _errornum = 0
        final_testing_result = "True"

        if failed is not None:
            _failednum = int(failed.string[0])

        if xfailed is not None:
            _xfailednum = int(xfailed.string[0])

        if error is not None:
            _errornum = int(error.string[0])

        testing_result = _failednum + _xfailednum + _errornum

        if testing_result > 0:
            final_testing_result = "False"

        filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        if filepath:
             filepath = filepath + "/"

        file = open(filepath + "final_testing_job_result.txt", 'w')
        file.write("final_testing_job_result = " + final_testing_result)

    except Exception as e:
        print("count the test cases number failed: " + str(e))
    finally:
        if 'file' in vars() and file is not None:
            file.close()

