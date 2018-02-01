import requests
import csv
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    issue_no_indicator = ('class', 'issue-link')
    summary_indicator = ('id', 'summary-val')
    description_indicator = ('class', 'user-content-block')
    indicators = [issue_no_indicator, summary_indicator]

    def __init__(self):
        HTMLParser.__init__(self)
        self.flag = False
        self.des_flag = False
        self.des_get_value_flag = False
        self.data_list = []
        self.description = []

    def handle_starttag(self, tag, attrs):

        for i in self.indicators:
            if i in attrs:
                self.flag = True
        if self.description_indicator in attrs:
            self.des_flag = True
        if self.des_flag and tag == 'p':
            self.des_get_value_flag = True

    def handle_data(self, data):
        if self.flag:
            self.data_list.append(data.strip())
        if self.des_get_value_flag:
            self.description.append(data.strip())

    def handle_endtag(self, tag):
        if self.flag:
            self.flag = False
        if self.des_get_value_flag:
            self.des_get_value_flag = False

    def write_value_into_file(self):
        issue = Issue(customer_tracking_id=self.data_list[0], summary=self.data_list[1],
                      description=','.join(self.description))
        data_list = ['', issue.summary, issue.issue_type, issue.versions, issue.components, issue.assignee,
                     issue.reporter, issue.severity, issue.priority, issue.environment, issue.problem_steps,
                     issue.test_phase, issue.triage, issue.product, issue.description, issue.test_phase_old,
                     issue.customer_tracking_ID, issue.severity_old]

        with open('DBS_ISSUES_LIST.csv', 'a', newline='') as csvfile:
            print(issue.customer_tracking_ID)
            writer = csv.writer(csvfile)
            writer.writerow(data_list)


class Issue(object):
    def __init__(self, customer_tracking_id, summary, description):
        self.summary = summary  # line[1]
        self.issue_type = "Bug"  # line[2]
        self.versions = "PendingBuild"  # line[3]
        self.components = "Cash - Generic"  # line[4]
        self.assignee = "cluwei"  # line[5]
        self.reporter = "lieric"  # line[6]
        self.severity = "Minor"  # line[7]
        self.priority = "Minor"  # line[8]
        self.environment = "UAT"  # line[9]
        self.problem_steps = "Refer to description"  # line[10]
        self.test_phase = "Customer User Acceptance Testing (UAT)"  # line[11]
        self.triage = "Triage Completed"  # line[12]
        self.product = "Online Banking-Custom"  # line[13]
        self.description = description  # line[14]
        self.test_phase_old = "11.UAT"  # line[15]
        self.customer_tracking_ID = customer_tracking_id  # line[16]
        self.severity_old = "3"  # line[17]

if __name__ == "__main__":
    host = "https://116.12.252.147/"
    path = "dcifjira/browse/"
    username_password = ('huina', 'ideal3@pwd33')
    issue_list = [""]
    for i in issue_list:
        try:
            r = requests.get(host+path+i, verify=False, auth=username_password)
            parser = MyHTMLParser()
            parser.feed(r.text)
            parser.write_value_into_file()
        except Exception as e:
            print("Get this issue failed,please retry")
            print(e)
            continue
