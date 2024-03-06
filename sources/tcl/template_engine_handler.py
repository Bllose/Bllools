import pymysql
import json
import logging


class template():
    def __init__(self, host='10.51.2.199', port=3306, user='pvuser', passwd='3GOZOtXJ^EdRnzhF'):
        try:
            self.db = pymysql.connect(host='10.51.2.199', user='pvuser', passwd='3GOZOtXJ^EdRnzhF', port=3306)
            self.cursor = self.db.cursor()
        except:
            logging.error('something wrong!')
        self.version = None

        """
        初始化库中存量的生效中的资方列表
        """
        self._fund_dict = {}
        sql = 'select id, fund_name from `xk-order`.`fund_info` where is_delete = false and status = 0;'
        self.cursor.execute(sql)
        fundsTuple = self.cursor.fetchall()
        for fund in fundsTuple:
            self._fund_dict[fund[0]] = fund[1]

        """
        初始化每个资方下的页面信息
        """
        self._fund_page_key_dict = {}
        origin_sql = 'select page_key, page_type from `xk-order`.`page_v2` where is_delete = false and fund_id = {} group by page_key, page_type;'
        for fundId, _ in self._fund_dict.items():
            sql = origin_sql.replace("{}", str(fundId))
            self.cursor.execute(sql)
            self._fund_page_key_dict[fundId] = self.cursor.fetchall()

        """
        执行计划，使用者定制
        """
        self._plan = {}


    @property
    def fund_page_key_dict(self):
        return self._fund_page_key_dict

    @property
    def fund_dict(self):
        """
        获取所有生效中的资方列表
        """
        return self._fund_dict
    
    @property
    def plan(self):
        return self._plan
    

    def plan_show_rule(self):
        """
        计划针对“显示规则”进行处理
        """
        self._plan.clear()
        self._plan['itemKey'] = 'displayRule'
        return self

    
    def plan_funds(self, fund_scope):
        """
        计划需要处理的资方范围列表
        列表中包含了pageKey
        @param fund_scop: 目前支持举例: 129, '129', [129, 131], 'all', '光瑞宝'
        """
        if isinstance(fund_scope, str):
            if 'all' == fund_scope.lower():
                self._plan['fundsDict'] = self._fund_page_key_dict
            else:
                try :
                    self._plan['fundsDict'] = {int(fund_scope): self._fund_page_key_dict[int(fund_scope)]}
                except ValueError :
                    for key, value in self._fund_dict.items():
                        if value == fund_scope:
                            self._plan['fundsDict'] = {key: self._fund_page_key_dict[key]}

        elif isinstance(fund_scope, list):
            self._plan['fundsDict'] = {key: value for key, value in self._fund_page_key_dict.items() if key in fund_scope}
        elif isinstance(fund_scope, int):
            self._plan['fundsDict'] = {key: value for key, value in self._fund_page_key_dict.items() if key == fund_scope}
        else:
            logging.error('资方范围选择有误! 输入参数为:' + fund_scope)
        return self
    
    def check_if_have_the_rule(self, rule_name: str):
        """
        检查计划中范围内是否存在指定的 方法 rule_name
        @param rule_name: 需要检查的方法名
        """
        if not isinstance(rule_name, str):
            logging.error("方法名必须是一条string! 接收到的方法名类型是:" + type(rule_name))
            return
        logBuilder = ['\n']
        if logging.getLogger().level <= logging.INFO:
            logBuilder.append('当前任务处理目标对象包括:')
            logBuilder.append(str(self._plan['itemKey']) + '\n')
            fundNames = [value for key, value in self._fund_dict.items() if key in self._fund_page_key_dict.keys()]
            logBuilder.append('当前任务处理数据所属资方范围:')
            logBuilder.append(str(fundNames) + '\n')
            logBuilder.append('排查目标 -> 包含规则 : ' + rule_name)
            logging.info(''.join(logBuilder))
            logBuilder.clear()
            logBuilder.append('\n')
        
        origin_sql = r"select page_key, page_name, tabs from `xk-order`.`page_v2` where is_delete = false and fund_id = {1} and page_key = '{2}';"
        indent = '\t'
        for fundId, pageKeys in self._plan['fundsDict'].items():
            logging.info(indent + self._fund_dict[fundId])
            temp_sql = origin_sql.replace('{1}', str(fundId))
            for pageKey, _ in pageKeys:
                sql = temp_sql.replace('{2}', pageKey)

                # 组装好了指定资方下的页面key，从数据库中查询到配置好的json报文
                self.cursor.execute(sql)
                page_group = self.cursor.fetchall()
                logging.info(indent + indent + page_group[0][0] + ' [' + page_group[0][1] + ']')
                group = json.loads(page_group[0][2])
                theTab = group[0]['groups']

                for curTab in theTab:
                    items = curTab['items']
                    groupName = curTab['groupName']
                    for item in items:
                        if self._plan['itemKey'] in item:
                            theTarget = item[self._plan['itemKey']]
                            if theTarget is None or not isinstance(theTarget, str):
                                continue
                            if rule_name in theTarget:
                                logging.info(indent + indent + indent + groupName + ' itemIndex:' + str(item['itemIndex']) + ' ' + item['labelName'] + ' -> ' + theTarget)


    def connectCheck(self):
        if self.version is None:
            self.cursor.execute("SELECT VERSION()")
            self.version = self.cursor.fetchone()[0]
        return self.version
    
    def end(self):
        self.db.close()



if __name__ == '__main__':
    handler = template()
    logging.basicConfig(level=logging.INFO)
    handler.plan_show_rule().plan_funds('光瑞宝').check_if_have_the_rule('analysisFamoueOut')
    handler.end()

