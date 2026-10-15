import requests

'''
这里的url是在百度搜索框中键入“python”后返回的结果，这个url
与我们直接使用selenium得到的url并不相同。
'''

url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=Python&fenlei=256&rsv_pq=0xce8d2e0000057f75&rsv_t=529cdEVm7PyJU8ArDtOE0pmzq8hh7OADQo4eZCzFpYpfYSnQ9NSpNUY%2F36rd&rqlang=en&rsv_enter=1&rsv_dl=tb&rsv_sug3=12&rsv_sug1=9&rsv_sug7=101&rsv_sug2=0&rsv_btype=i&inputT=5802&rsv_sug4=6454&rsv_sug=1'

try:
    response = requests.get(url)
    if response.status_code == 200:
        print(response.text)
    else:
        print(f"Failed to retrieve data: Status code {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")