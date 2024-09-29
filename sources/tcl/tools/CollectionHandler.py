import json
import logging

def ranking_standardization(target_list: list, key: str, span: int, startNum: int = 10):
    """
    排序标准化

    对一个list中的某个字段进行排序标准化
    1、源排序顺序不变, 从小到大
    2、所有排列间隔根据 span 标准化
    3、以名字为key值的字段作为标准化

    @param startNum: 排序首位数字，默认是 10
    """
    target_list.sort(key=lambda d: d[key])

    begin = True
    preNum = startNum
    for target in target_list:
        if begin:
            target[key] = startNum
            begin = False
            continue
        preNum += span
        target[key] = preNum
        

def mbyq_tabs_standardization(pageKeyObject :json):
    """
    传入pageKey对象
    """
    if 'tabs' not in pageKeyObject:
        logging.error('{..., tabs:[], ...} 不存在!')
        return
    tabs = pageKeyObject['tabs']
    for tab in tabs:
        """
        
        """
        


if __name__ == '__main__':
    
    absFileName = f'D:\\workplace\\20240830\\129_光鑫宝-共富_OrderDetail.json'
    with open(absFileName, 'r', encoding='utf-8') as file:
        content = file.read()
        data = json.loads(content)
        ranking_standardization(data['tabs'][0]['groups'], 'groupIndex', 10)

        for group in data['tabs'][0]['groups']:
            ranking_standardization(group['items'], 'itemIndex', 10)

        with open(f'D:\\workplace\\20240830\\129_光鑫宝-共富_OrderDetail_sorted.json', 'w') as file:
            file.write(json.dumps(data))

    print('DONE')
        