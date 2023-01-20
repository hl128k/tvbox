import re
import datetime
import requests
import urllib3
p1 = re.compile(r"[(](.*?)[)]", re.S)
p2 = re.compile(r"^(https://ghproxy.com/https://raw.githubusercontent.com/tv-player/tvbox-line/main/tv/)", re.I)
urllib3.disable_warnings()
req = requests.get('https://raw.fastgit.org/tv-player/TvBox/main/README.md', verify=False)
nameList=[]
reList=["https://ghproxy.com/https://raw.githubusercontent.com","https://cdn.staticaly.com/gh","https://raw.fastgit.org","https://raw.kgithub.com","https://raw.iqiq.io","https://github.moeyy.xyz/https://raw.githubusercontent.com"]
for url in re.findall(p1,req.text):
    reflag=re.search(p2, url)
    if reflag:
        urlReq = requests.get(url, verify=False)
        for reI in range(len(reList)):
            urlname=url.replace("https://ghproxy.com/https://raw.githubusercontent.com/tv-player/tvbox-line/main/tv/", "")
            reqtext=urlReq.text
            reqtext=reqtext.replace("/raw/", "/").replace("'https://github.com", "'"+reList[reI]).replace("'https://raw.githubusercontent.com", "'"+reList[reI])
            fp = open("./tv/"+str(reI)+"/"+urlname, "w+",encoding='utf-8')
            fp.write(reqtext)
        nameList.append(urlname)
now = datetime.datetime.now()
fp = open('README.md', "w+",encoding='utf-8')
fp.write("# TvBox 配置\n\n")
fp.write("所有数据均来自于网络，不保证可用性\n\n")
fp.write("原始数据来源：https://github.com/tv-player/TvBox\n\n")
fp.write("因电视对GitHub访问问题，所以将配置中的GitHub换成镜像源\n\n")
fp.write("本次更新时间为："+now.strftime("%Y-%m-%d %H:%M:%S")+"\n\n")
fp.write("如果有必要手动输入建议使用短链如：[http://gg.gg/](http://gg.gg/)，[https://suowo.cn/](https://suowo.cn/)，[https://dlj.li/](https://dlj.li/) 等\n\n")
fp.write("删除列表，请复制项目后自行对tv目录下的数字目录内的文件进行镜像使用\n\n")
fp.close()
