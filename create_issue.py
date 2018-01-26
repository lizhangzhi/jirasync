# import requests
# import json
import csv

if __name__ == "__main__":

    issues = csv.reader(open('DBS_ISSUES_LIST.csv', 'r'))
    for line in issues:
        project = line[0]
        summary = line[1]
        issue_type = line[2]
        versions = line[3]
        components = line[4]
        assignee = line[5]
        reporter = line[6]
        severity = line[7]
        priority = line[8]
        environment = line[9]
        problem_steps = line[10]
        test_phase = line[11]
        triage = line[12]
        product = line[13]
        description = line[14]
        print('project:', project, 'summary:', summary, 'issuetype:', issue_type, 'versions:', versions, 'components:', components,
              'assignee:', assignee, 'reporter:', reporter, 'severity:', severity, 'priority:', priority, 'environment:', environment,
              'problem_steps:', problem_steps, 'test_phase:', test_phase, 'triage:', triage, 'product:', product, 'description:', description)

        # payload =\
        # {
        #     "fields": {
        #         "project": {
        #             "key": project
        #         },
        #         "summary": summary,
        #         "issuetype": {
        #             "name": issue_type
        #         },
        #         "versions": [
        #             {
        #                 "name": versions
        #             }
        #         ],
        #         "components": [
        #             {
        #                 "name": components
        #             }
        #         ],
        #         "assignee": {
        #             "name": assignee
        #         },
        #         "reporter": {
        #             "name": reporter
        #         },
        #         "customfield_15594": {  # Severity
        #             "value": severity
        #         },
        #         "priority": {
        #             "name": priority
        #         },
        #         "environment": environment,
        #         "customfield_10031": problem_steps,  # Problem Steps
        #         "customfield_15592": {  # Test Phase
        #             "value": test_phase
        #         },
        #         "customfield_15590": {  # Triage
        #             "value": triage
        #         },
        #         "customfield_16010": {  # Product
        #             "value": product
        #         },
        #         "description": description,
        #     }
        # }
        #
        # headers = {
        #     'Content-Type': 'application/json'
        # }
        # r = requests.post('https://jira.aciworldwide.com/rest/api/2/issue',
        #                   headers=headers, auth=('lieric', 'Word2224'), data=json.dumps(payload))
        # print(r.text, r.status_code)
