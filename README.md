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


```
https://www.chia.net/2023/03/19/introducing-chia-blockchain-database-bittorent-checkpoints/

chia_plot -n 1 -c xch1xlsrr8nzlvs4gg5vyv2wa539vjv92967d07wrgy7pf9ylrewjdusdqcgj0 -t /tempDir/25 -2 /tempDir2/75 -d /finaldir

Showing all public keys derived from your master seed and private key:

Label: 大姐
Fingerprint: 137505866
Master public key (m): ac7776cbac61e8efd186ad9a8727f81621e6c2b3a95d4e9bc8704092c59d0f397cfa61c91f7265f885a161a8022e1fc8
Farmer public key (m/12381/8444/0/0): b1cea9913bfed6beb9831f5f48316eb1b994ffb9464ccffd67c6d09dc3db4bf5b8a61deca8ff89e45ccc49ad52a3d199
Pool public key (m/12381/8444/1/0): 8af3e65163a88e993fed9ff68d2c8666721f0cbdee82bbe7c5868ec9f2c55dadc28a16e3677b6a4de14c8b645ce76daf
First wallet address: xch15muplra6afam3t4dlm0ndy0dvyauqd7dmy55gdchea0qywgfltaq4nrzjv


Testing plot G:\xchpool\plot-k32-2023-05-03-21-12-f09ef7743841fc1b65d730489ba443eccfd12e46fcf6b1e21c907265942e35e0.plot k=32
2023-05-04T18:43:21.930  chia.plotting.check_plots        : INFO        Pool contract address:  xch1xlsrr8nzlvs4gg5vyv2wa539vjv92967d07wrgy7pf9ylrewjdusdqcgj0
2023-05-04T18:43:21.938  chia.plotting.check_plots        : INFO        Farmer public key:      adc081fa0e4cd8260687fdb3de0417b4568402f03110b50040d119401f9ea6178bae2fc77e373f4732faaa21dfa60aeb
2023-05-04T18:43:21.939  chia.plotting.check_plots        : INFO        Local sk:               <PrivateKey 2259be4ba69a2c21075c758761c1d9bdb964921b33ad05f723e06bdb6e2724ec>


Testing plot G:\xchpool\plot-k32-2023-05-03-23-06-72115acdf7983827f36c98da215174f7ea01aeae6333b18636d448bd6dbcf111.plot k=32
2023-05-04T18:44:24.273  chia.plotting.check_plots        : INFO        Pool contract address:  xch1xlsrr8nzlvs4gg5vyv2wa539vjv92967d07wrgy7pf9ylrewjdusdqcgj0
2023-05-04T18:44:24.287  chia.plotting.check_plots        : INFO        Farmer public key:      adc081fa0e4cd8260687fdb3de0417b4568402f03110b50040d119401f9ea6178bae2fc77e373f4732faaa21dfa60aeb
2023-05-04T18:44:24.287  chia.plotting.check_plots        : INFO        Local sk:               <PrivateKey 70b0d9adb9a0d1d1cca30985faf8054dcc65819d84aa79dd19d3e09869b5dc0a>


Wallet height: 3613416
Sync status: Synced
Wallet id 2:
Current state: FARMING_TO_POOL
Current state from block height: 3581647
Launcher ID: 13a6613f9dedf396602462d861df13dc739057b006b946b37c58ef422c8d071d
Target address (not for plotting): xch1pkpv9ceqx7mhm2wglh2ar486fwx05zqzd5kqfq6fq6m5rlwtdl3qyz7076
Number of plots: 0
Owner public key: 81439dc6df6dcd40db246c5b57dcd3441b1b69650788fbf29e40468deb740a5f7f32eaf42f6254ea443dacaf23470eba
Pool contract address (use ONLY for plotting - do not send money to this address): xch1uxt4uhpj7750xxxedhgape8l0h422jq37m0332uq7y4fmz7ffz2sqe49dk
Current pool URL: https://asia.xchpool.org
Current difficulty: 1
Points balance: 0
Points found (24h): 0
Percent Successful Points (24h): 0.00%
Payout instructions (pool will pay to this address): xch16f770ddnkc0wypaq30n7vygp0avj6whhpw6fzdsa2jv6vtsrchrq2hy7wl
Relative lock height: 100 blocks

Wallet id 3:
Current state: FARMING_TO_POOL
Current state from block height: 3608906
Launcher ID: 40e852ac2401c3f2091738e1aa8fb5b16a3f789ec0bf59b8b048eb1475837319
Target address (not for plotting): xch1pkpv9ceqx7mhm2wglh2ar486fwx05zqzd5kqfq6fq6m5rlwtdl3qyz7076
Number of plots: 0
Owner public key: a67620b06c204399f3a5ab4d69d3061ee23abbfab57965e56a8baae8113c3b370a8583775e84be696314385c9d3341ce
Pool contract address (use ONLY for plotting - do not send money to this address): xch1xlsrr8nzlvs4gg5vyv2wa539vjv92967d07wrgy7pf9ylrewjdusdqcgj0
Current pool URL: https://pool.xchpool.org
Current difficulty: 1
Points balance: 0
Points found (24h): 0
Percent Successful Points (24h): 0.00%
Payout instructions (pool will pay to this address): xch1rthk608aejg0txaeywqh20nant8h97mkwla3usqr8k6tt7mvg3pq2q38yn
Relative lock height: 100 blocks
```
