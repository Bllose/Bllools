# 分组工具
针对男女分组工具。  
遵守几个原则：  
1. 尽可能男女平均分配  
2. 多次分组，尽量让重复组队的次数最少 

``` python
    from grouping.balance import OriginData, Grouping

    # OriginData 用以加载数据源，当前识别excel文档, 精确到 sheet 页
    # 其内部类config可以配置具体数据数据所属栏位
    od = OriginData()
    od.set_path(os.path.abspath('../../resources')).set_file_name(r'HIT22VCteam.xlsx').set_sheet_name(r'Sheet1')
    
    # key 用来指定排序的关键编号， 比如班号
    # datas 的设定就是历代所分小组记录， 多次分组通过 -, ~ 等符号关联
    od.config().set_key(r'B').set_name(r'C').set_gender(r'D').set_datas(r'E-J')
    
    # 将加载好的数据送给 Grouping, 由其具体进行分组
    grouping = Grouping(od.load())
    
    # process 正式开始分组, 其中参数order指定本次分组的组数
    grouping.process(order=7).showTheLastGroup().showTheLastOrder()
```