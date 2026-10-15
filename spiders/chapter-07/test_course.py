import requests
# url = 'https://zhjw.hpu.edu.cn/eams/homeExt.action'
url = 'https://zhjw.hpu.edu.cn/eams/courseTableForStd!courseTable.action'
data = {
    'ignoreHead': 1,
    'setting.kind': 'std',
    'startWeek':'' ,
    'project.id': 1,
    'semester.id': 184,
    'ids': 110695
}
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
    'cache-control':'no-cache',
    'connection':'keep-alive',
    'content-length':'80',
    'cookie':'semester.id=184; JSESSIONID=CCCD79AD9B9EB77968133B39A429ED2C; SERVERNAME=c5; GSESSIONID=CCCD79AD9B9EB77968133B39A429ED2C; JSESSIONID=1EC919DEB36029667B040A954AA8E63C'
}
response = requests.post(url,data=data,headers=headers)
if response.status_code==200:
    print(response.text)