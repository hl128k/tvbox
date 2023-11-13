import re
import datetime
import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
with open('./url.json', 'r', encoding='utf-8') as f:
    urlJson = json.load(f)
nameList = []
reList = ["https://ghproxy.com/https://raw.githubusercontent.com", "https://raw.fgit.cf/",
          "https://raw.fastgit.org", "https://raw.iqiq.io",
          "https://github.moeyy.xyz/https://raw.githubusercontent.com", "https://fastly.jsdelivr.net/gh/"]
reRawList = [False, False,
          False, False,
          False, True]
for item in urlJson:
    urlReq = requests.get(item["url"], verify=False)
    for reI in range(len(reList)):
        urlName = item["name"]
        urlPath = item["path"]
        reqText = urlReq.text
        if urlName != "gaotianliuyun_0707":
            reqText = reqText.replace("'./", "'" + urlPath) \
                .replace('"./', '"' + urlPath)
        if reRawList[reI]:
            reqText = reqText.replace("/raw/", "@")
        else:
            reqText = reqText.replace("/raw/", "/")
        reqText = reqText.replace("'https://github.com", "'" + reList[reI]) \
            .replace('"https://github.com', '"' + reList[reI]) \
            .replace("'https://raw.githubusercontent.com", "'" + reList[reI]) \
            .replace('"https://raw.githubusercontent.com', '"' + reList[reI])
        fp = open("./tv/" + str(reI) + "/" + urlName + ".json", "w+", encoding='utf-8')
        fp.write(reqText)
now = datetime.datetime.now()
fp = open('README.md', "w+", encoding='utf-8')
fp.write("# 提示\n\n")
fp.write("如果有收录您的配置，您也不希望被收录请[issues](https://github.com/hl128k/tvbox/issues)，必将第一时间移除\n\n")
fp.write("如果有好的地址配置需要镜像化请提交[issues](https://github.com/hl128k/tvbox/issues)\n\n")
fp.write("本人不对任何数据源负责，任何情况问题请自行负责，请勿以任何形式进行传播\n\n")
fp.write("# TvBox 配置\n\n")
fp.write("本页面只是收集Box，自用请勿宣传\n\n")
fp.write("所有资源全部搜集于网络，不保证可用性\n\n")
fp.write("因电视对GitHub访问问题，所以将配置中的GitHub换成镜像源\n\n")
fp.write("本次更新时间为：" + now.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
fp.write("更新仅为自动更新，实际更新情况请以原始路径为准，内容参考url.json\n\n")
fp.write(
    "如果有必要手动输入建议使用短链如：[http://gg.gg/](http://gg.gg/)，[https://suowo.cn/](https://suowo.cn/)，[https://dlj.li/](https://dlj.li/) 等\n\n")
fp.write("删除列表，请复制项目后自行对tv目录下的数字目录内的文件进行镜像使用\n\n")
fp.close()
