'''
  从Github 获取star 排序降序的repository list 1000个；
  r.json captures json in python,
  then we can access json like accessing any python objects,
  等价于import json, then json.loads()
'''

import json
import requests
import time

OUTPUT_CSV_FILE = 'originalRepositoryList.csv'
URL = 'https://api.github.com/search/repositories?q=android+pushed:>2018-01-01+topic:app&sort=stars&order=desc'

'''
#write response of page 1 into json file
apps = r.json()
with open('response_apps.json', 'w') as f:
    f.write(json.dumps(apps, indent=2))
    
#obtain total page num of response
apps_header = r.headers['link']
pattern = re.compile(r'(\d+)(>; rel="last")')
totalPageNum = int(pattern.search(apps_header).group(1))
'''

totalPageNum = 34 #github api 最多只返回1000个item， 每页只返回30个，所以只能查到34页
countOfRepo = 0
repositories = []

repositories.append({
    'total count': countOfRepo
})

for currentPageNum in range(1, totalPageNum+1):
    url = f'{URL}&page={str(currentPageNum)}'
    t1 = time.perf_counter()  # capture current time in python
    print(f'Requesting for page {str(currentPageNum)}')
    r = requests.get(url)
    repos = r.json()

    for repo in repos['items']:
        repo_name = repo['name']
        repo_owner = repo['owner']['login']
        repo_url = repo['html_url']
        repo_desc = repo['description']

        data = {
            'repository_name': repo_name,
            'repository_owner': repo_owner,
            'repository_url': repo_url,
            'repository_description': repo_desc
        }

        repositories.append(data)
        countOfRepo += 1

        print(f'Got {repo_name} ')

    t2 = time.perf_counter()
    print(f'Finished page {str(currentPageNum)} in {t2-t1} seconds')
    time.sleep(r.elapsed.total_seconds())

with open('original_repository_list.json', 'w') as f:
     json.dump(repositories, f, indent=2)







