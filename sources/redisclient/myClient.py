import redis

host = 'bllose.online/redis'

creds_provider = redis.UsernamePasswordCredentialProvider("xk-contract", "46f1rPPYf7LIfYm8")
user_connection = redis.Redis(host="10.68.63.80", port=6379, credential_provider=creds_provider)
print(user_connection.ping())

keys = user_connection.keys()

# for key in keys:
#   print('Key:', key)
#   print('Value:', user_connection.get(key))


#   增加数据：set key value（如果key存在，则修改为新的value）
print(user_connection.set('str_type', 'str_value'))  # 打印True
#   追加数据：append key value
print(user_connection.append('str_type', '_new'))  # 打印13，字符长度
#   查看数据：get key
print(user_connection.get('str_type'))

# #   hash类型的值是一个键值对集合，如：h_test : { field1:value1, field2:value2,...}
# #   添加数据：hset key field value
# print(user_connection.hset('hash_type', 'filed', 'value'))  # 打印成功添加数据的条数
# #   查看域值：hget key field
# print(user_connection.hget('hash_type', 'filed'))
# #   查看所有的field：hkeys key
# print(user_connection.hkeys('hash_type'))
# #   查看所有的value：hvals key
# print(user_connection.hvals('hash_type'))
# #   查看所有的键值对：hgetall key
# print(user_connection.hgetall('hash_type'))