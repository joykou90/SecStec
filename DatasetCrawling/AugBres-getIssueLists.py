'''
   call Github issue API to get issue list tagged with 'bug';
   2018年1月1号以后更新的open&closed 的issue;
   capture issue id, name, state, html url  and body within response in a file called 'original_issue_list.json'
'''
import json
import requests
import re
import time

results = []

with open('InteractiveApp_repository_list.json') as f:
    apps = json.load(f)

for app in apps[1:]:
    owner_name = app['repository_owner']
    app_name = app['repository_name']

    print(f'Requesting for issue list of {app_name}')

    url = f'https://api.github.com/repos/{owner_name}/{app_name}/issues'

    if app_name == 'WordPress-Android':
        payload = {
            'labels': '[Type] Bug',
            'state': 'all',
            'since': '2018-01-01T00:00:00Z'
        }
    else:
        payload = {
            'labels': 'bug',
            'state': 'all',
            'since': '2018-01-01T00:00:00Z'
        }


    r = requests.get(url, params = payload, auth=('joykou90', '63546f9a7272968ef84fe337f53fba1502ed6cb2'))
    header = r.headers.get('link')
    issues = r.json()

    for issue in issues[0:]:
        issue_id = issue['id']
        title = issue['title']
        state = issue['state']
        issue_url = issue['html_url']
        issue_description = issue['body']

        data = {
            'issue_id': issue_id,
            'title': title,
            'state': state,
            'issue_url': issue_url,
            'description': issue_description
        }
        results.append(data)


    #当返回的issue list 超过一页时
    if header!=None:
        pattern = re.compile(r'(\d+)(>; rel="last")')
        totalPageNum = int(pattern.search(header).group(1))
        page = 2

        while page <= totalPageNum:
            payload['page'] = page

            print(f'Requesting for page {page} of {app_name}')
            r2 = requests.get(url, params=payload, auth=('joykou90', '63546f9a7272968ef84fe337f53fba1502ed6cb2'))
            newPageIssues = r2.json()

            for newPageIssue in newPageIssues[0:]:
                newIssue_id = newPageIssue['id']
                newTitle = newPageIssue['title']
                newState = newPageIssue['state']
                newIssue_url = newPageIssue['html_url']
                newIssue_description = newPageIssue['body']

                newData = {
                    'issue_id': newIssue_id,
                    'title': newTitle,
                    'state': newState,
                    'issue_url': newIssue_url,
                    'description': newIssue_description
                }
                results.append(newData)

            page += 1

            time.sleep(r.elapsed.total_seconds())

    time.sleep(r.elapsed.total_seconds())


with open('original_issue_list.json','w') as f2:
    json.dump(results, f2, indent=2)











