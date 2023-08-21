import wencai as wc

# 若需中文字段则cn_col=True,chromedriver路径不在根目录下需指定execute_path
wc.set_variable(cn_col=True)

wc.get_iwencai('沪深300,净利润增长大于20%')