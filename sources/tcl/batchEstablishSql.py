
# sql_string = "INSERT INTO `xk-contract`.contract_filter_rule (order_no, fund_id, scene_code_json, is_delete, create_time, update_time, creator, updator, columns_json)\r\n VALUES('{orderNo}', '129', '[\"PCI001\"]', 1, now(), now(), '', '', NULL); \r\nINSERT INTO `xk-contract`.filter_rule (order_no, filter_type, is_delete, create_time, update_time, creator, updator)\r\n VALUES('{orderNo}', 'WAIT_MERGE_RECHECK', 0, now(), now(), 'sys', 'sys');"

# orderNos = input("orderNos: ")

# orderList = orderNos.split(",")

# for orderNo in orderList:
#     print(sql_string.replace('{orderNo}', orderNo))


orderDict = {}

curLine = input('start: ')

while len(curLine) > 1:
    if '"' in curLine:
        curLine = curLine.replace('"', '')
    if '\t' in curLine:
        orderArray = curLine.split('\t')
        orderDict[orderArray[0]] = orderArray[1]
    curLine = input()

# print(orderDict)

sqlMsg = r"('{oldOrderNo}', '{newOrderNo}', 'system', now(), 'system', 1, now(), 0),"
mqMsg = r'"{\"orderNo\":\"{oldOrderNo}\",\"approvalNodeId\":1}"'

sqlMsgList = []
mqMsgList = []
for key, value in orderDict.items():
    tempSqlMsg = sqlMsg.replace('{oldOrderNo}', key)
    tempSqlMsg = tempSqlMsg.replace('{newOrderNo}', value)

    tempMqMsg = mqMsg.replace('{oldOrderNo}', key)

    sqlMsgList.append(tempSqlMsg)
    mqMsgList.append(tempMqMsg)

for sql in sqlMsgList:
    print(sql)

print("")
print("")
print("")

for mq in mqMsgList:
    print(mq)