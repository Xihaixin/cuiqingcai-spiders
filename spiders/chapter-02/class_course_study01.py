import os
import random

FOLDER_PATH = '../results'
N = 10
TEST_N = 4
file_mapping = {}
count = 0
for index, filename in enumerate(os.listdir(FOLDER_PATH)):
    if filename.endswith('.json'):
        file_mapping[index] = filename[:-5]
        count += 1

movie_lovers = {}
user_lover = {}
test_user = {}
START_N = 2
END_N = 6
for i in range(1, N+1):
    user_name = 'user' + str(i)
    movie_lovers[user_name] = random.randint(START_N, END_N)
    user_lover[user_name] = random.sample(range(count), movie_lovers[user_name])

test_user['test_user'] = random.sample(range(count), TEST_N)

def check_movie(test_user_num):
    same_love_user = []
    for user_name, movies_watched in user_lover.items():
        if set(test_user_num).intersection(set(movies_watched)):
            same_love_user.append(user_name)
    return same_love_user

total_same_user = []
for movie_num in test_user['test_user']:
    total_same_user.append(check_movie([movie_num]))

# 打印结果
cn =0
for i, user in enumerate(total_same_user):
    if not user:
        cn+=1
    else:
        movieName_index = test_user['test_user'][i]
        print(f"电影编号为:{test_user['test_user'][i]}-->({file_mapping[movieName_index]}) 的相同喜好用户: {user}")
        # 获取具有相同喜好的用户的电影列表
        if len(user)==1:
            ustr = user[0]
            print(f'{ustr}推荐的电影列表为{user_lover[ustr]}')
            print([file_mapping[i] for i in range(len(user_lover[ustr]))])
    if cn == len(test_user['test_user']):
        print('您的观影口味独特，其他十位用户过去观看过的电影与您的观影记录未出现重合')
        print('我们将基于您观看过的电影的类型为您推荐电影')
        




    

