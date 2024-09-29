import json
import logging


def remove_all_None_value(json_str: str) -> str:
    """
    将json对象中所有null值抹除掉之后，返回一个完整的非空json
    """
    target = json.loads(json_str)
    done = remove_none_values(target)
    try:
      result_str = json.dumps(done)
    except Exception as e:
       logging.error(f'转换json报文失败:{e}')
       logging.warning(f'处理后的直接结果{done}')
       import traceback
       traceback.print_exc()
    else:
       # 正常执行
       logging.debug(f'源 -> {json_str}')
       logging.debug(f'果 -> {result_str}')
    return result_str


def remove_none_values(data) -> json:
    if isinstance(data, dict):  
        # 如果是字典，则遍历并递归清理  
        return {k: remove_none_values(v) for k, v in data.items() if v is not None}  
    elif isinstance(data, list):  
        # 如果是列表，则遍历列表中的每个元素并递归清理  
        return [remove_none_values(item) for item in data if item is not None]  
    else:  
        # 如果不是字典或列表，则直接返回原始值（不做任何更改）  
        return data  


if __name__ == '__main__':
  json_str = '{"version":"v10","isSign":true,"isRushSign":false,"templateId":null,"objectNo":"GF240925095735049135","sceneCode":"PCI001","imageCode":null,"sceneName":null,"signMethod":1,"controlSignNodes":null,"channel":3,"tenantKey":null,"organACode":null,"organAName":null,"organBCode":null,"organBName":null,"legalName":null,"legalIdNo":null,"legalMobile":null,"legalBName":null,"legalBIdNo":null,"legalBMobile":null,"spouseName":null,"spouseIdCard":null,"fillElement":null,"reqFillElement":null,"lockId":null,"isReuse":null,"reuseValidDays":null,"needSignUrl":true,"needCosignerUrl":true,"createAccountId":true,"signTasks":null}'
  print(remove_all_None_value(json_str))