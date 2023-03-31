# 此模块为自定义扩展模块

## 使用方法：
1. 将需要的python文件放到preCompile目录下
2. 使用python setup.py sdist命令进行打包，打包完成之后会在当前目录下生成一个dist目录，其中有preCompile模块生成的tar包
3. 在当前目录（setup.py目录）下执行pip install .命令即可安装

注：若想打包为.wheel文件则需要查看是否已安装wheel库，若未安装执行命令pip install wheel即可，然后再在当前目录使用python setup.py bdist_wheel即可