import pymongo  

# 创建 MongoDB 客户端  
client = pymongo.MongoClient(host='localhost', port=27017)  

# 建立或连接到 test 数据库  
db = client.test  

# 指定集合  
collection = db.students  

# 插入数据  
student = {  
    'id': '20170101',  
    'name': 'Jordan',  
    'age': 20,  
    'gender': 'male'  
}  

student1 = {
    'id':'20180102',
    'name':'Stedive',
    'age':19,
    'gender':'male'
}

student2 = {
    'id':'20190203',
    'name':'Yuehan',
    'age':21,
    'gender':'male'
}

student3 = {
    'id':'20200104',
    'name':'Peter',
    'age':22,
    'gender':'female'
}

# 使用 insert_one 方法插入单个文档  
result = collection.insert_one(student)  
result = collection.insert_many([student1,student2,student3])

# 输出插入结果  
print(f'Inserted student with id {result}')