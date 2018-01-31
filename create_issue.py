import requests
import re
import json
import csv

completed_list = "sync_completed_list.txt"
failed_list = "sync_failed_list.txt"


class Issue(object):
    def __init__(self, line):

        self.ACI_user_password = ('lieric', 'Word2224')
        self.request_headers = {
            'Content-Type': 'application/json'
        }
        self.host = "https://jira.aciworldwide.com/"
        self.create_issue_url = "rest/api/2/issue"

        self.project = line[0]
        self.summary = line[1]
        self.issue_type = line[2]
        self.versions = line[3]
        self.components = line[4]
        self.assignee = line[5]
        self.reporter = line[6]
        self.severity = line[7]
        self.priority = line[8]
        self.environment = line[9]
        self.problem_steps = line[10]
        self.test_phase = line[11]
        self.triage = line[12]
        self.product = line[13]
        self.description = line[14]
        self.test_phase_old = line[15]
        self.customer_tracking_ID = line[16]
        self.severity_old = line[17]

    def set_parameter(self):

        if re.match("IDEA", self.customer_tracking_ID):
            self.project = "DBSGU"
        elif re.match("AB", self.customer_tracking_ID):
            self.project = "DBSPS"
            self.assignee = "jgabay"
            self.components = "CB - Other "
            self.environment = "Production Env"
            self.test_phase_old = "12.Production"
            self.test_phase = "Product Acceptance Testing (PAT)"

        payload =\
        {
            "fields": {
                "project": {
                    "key": self.project
                },
                "summary": "["+self.customer_tracking_ID+"]" + self.summary,
                "issuetype": {
                    "name": self.issue_type
                },
                "versions": [
                    {
                        "name": self.versions
                    }
                ],
                "components": [
                    {
                        "name": self.components
                    }
                ],
                "assignee": {
                    "name": self.assignee
                },
                "reporter": {
                    "name": self.reporter
                },
                "customfield_15594": {  # Severity
                    "value": self.severity
                },
                "priority": {
                    "name": self.priority
                },
                "environment": self.environment,
                "customfield_10031": self.problem_steps,  # Problem Steps
                "customfield_15592": {  # Test Phase
                    "value": self.test_phase
                },
                "customfield_15590": {  # Triage
                    "value": self.triage
                },
                "customfield_16010": {  # Product
                    "value": self.product
                },
                "description": self.description,
                "customfield_10170": self.customer_tracking_ID,  # Customer Tracking ID (DBSGU)
                "customfield_10081": {  # Test Phase (Old)
                    "value": self.test_phase_old
                },
                "customfield_10331": {  # Severity (Old) DBSGU
                    "value": self.severity_old,
                },
            }
        }
        return payload

    def send_create_issue_request(self):

        r = requests.post(self.host+self.create_issue_url,
                                      headers=self.request_headers, auth=self.ACI_user_password, data=json.dumps(self.set_parameter()))
        print(r.text)
        print(self.customer_tracking_ID, r.json()["key"], r.status_code)
        return r

    def record_complete_item(self, response):
        with open(completed_list, "a") as f:
            f.write(self.customer_tracking_ID + " >> " + response.json()["key"] + "\n")

if __name__ == "__main__":

    with open('DBS_ISSUES_LIST.csv', 'r') as input_file:
        reader = csv.reader(input_file)
        line_no = 0
        for line in reader:
            line_no += 1
            if line_no != 1:
                try:
                    issue = Issue(line)
                    r = issue.send_create_issue_request()
                    issue.record_complete_item(r)
                except Exception as e:
                    print(e)
                    with open(failed_list, 'a') as f:
                        print(issue.customer_tracking_ID)
                        f.write(issue.customer_tracking_ID + "\n")
                    continue
