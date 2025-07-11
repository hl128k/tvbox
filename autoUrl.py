import base64
import re
import datetime
import requests
import json
import urllib3
from Crypto.Cipher import AES
LEGAL_SHIELD = """
// 技术处理声明 (绑定至输出文件)
// 本文件由技术工具自动生成，开发者：
//   a) 未创建/修改任何实质内容
//   b) 不知晓具体数据内容
//   c) 已通过The Unlicense放弃所有权利
// 原始数据责任完全归属配置提供者
"""

def main():
    print("""
    !!! 技术工具声明 !!!
    本脚本仅为开源技术工具，功能仅限于:
    1. 读取本地JSON配置(url.example.json)
    2. 对其中URL进行域名替换操作
    3. 生成转换后的配置文件
    
    本工具不处理、不存储、不审查任何实际内容数据
    所有最终内容由原始配置决定，与工具无关
    """)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    with open('./url.example.json', 'r', encoding='utf-8') as f:
        urlJson = json.load(f)
    nameList = []
    reList = ["https://ghproxy.net/https://raw.githubusercontent.com", "https://raw.kkgithub.com",
              "https://gcore.jsdelivr.net/gh", "https://mirror.ghproxy.com/https://raw.githubusercontent.com",
              "https://github.moeyy.xyz/https://raw.githubusercontent.com", "https://fastly.jsdelivr.net/gh"]
    reRawList = [False, False,
                 True, False,
                 False, True]
    for item in urlJson:
        urlData = get_json(item["url"])
        for reI in range(len(reList)):
            urlName = item["name"]
            urlPath = item["path"]
            reqText = urlData
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

    collectionJson = {
        "urls": []
    }
    for item in urlJson:
        if "_" in item["name"]:
            urlItem = {
                "url": "./"+ item["name"] + ".json",
                "name": item["name"]
            }
            collectionJson["urls"].append(urlItem)
    collectionJson_data = json.dumps(collectionJson, ensure_ascii=False, indent=4)
    for reI in range(len(reList)):
        fp = open("./tv/" + str(reI) + "/collection.json", "w+", encoding='utf-8')
        fp.write(collectionJson_data)

    now = datetime.datetime.now()
    fp = open('README.md', "w+", encoding='utf-8')
    fp.write("# [![Powered by DartNode](https://dartnode.com/branding/DN-Open-Source-sm.png)](https://dartnode.com \"Powered by DartNode - Free VPS for Open Source\") \n\n")
    fp.write("""## 免责声明 (Disclaimer)

### 1. 权利声明
本仓库遵循 **The Unlicense** 协议：
- 所有代码及内容归属于公共领域（Public Domain）
- 作者已永久放弃一切著作权及相关权利
- **允许任何人在全球范围内无条件地使用、复制、修改、商业应用及分发**

### 2. 无担保声明 (No Warranty)
本仓库内容按 **"原样"（AS IS）** 提供：
- **不提供任何明示或暗示的担保**，包括但不限于：
  - 适销性 (Merchantability)
  - 特定用途适用性 (Fitness for Purpose)
  - 准确性 (Accuracy) 或持续性服务 (Continuous Availability)
- 作者不对功能缺失、数据丢失或服务中断负责

### 3. 用户责任 (Your Responsibility)
您理解并同意：
- 使用行为必须**遵守所在国家/地区的法律法规**
- 需自行评估内容合法性及技术风险
- 对使用导致的**任何直接/间接后果承担全部责任**
-  **[详细技术免责声明](./TECHNICAL_DISCLAIMER.md)**

### 4. 第三方内容 (Third-party Content)
- 本项目仅为**技术工具**（自动处理公开网络链接）
- 不生成、存储或审核任何实质内容
- 引用的第三方数据源由其提供者负责
- **不认可任何被处理的第三方内容**

### 5. DMCA 与内容移除政策
尊重知识产权。如果您是版权所有者，并认为本仓库引用的内容侵犯了您的合法权益，请按照以下流程与我们联系：
- 在仓库的 "Issues" 页面创建一个新的 Issue。
- 提供充分的版权证明材料。
- 提供您希望移除的具体链接。
承诺在收到有效通知后的48小时内进行审查和处理。这是我们遵守 DMCA “安全港”条款的承诺。

""")
    
    fp.write("本次自动测试时间为：" + now.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
    fp.write("测试示例为url.example.json\n\n")
    fp.write("感谢各位大佬的无私奉献.\n\n")
    fp.close()

def get_json(url):
    key = url.split(";")[2] if ";" in url else ""
    url = url.split(";")[0] if ";" in url else url
    data = get_data(url)
    if not data:
        raise Exception()
    if is_valid_json(data):
        return data
    if "**" in data:
        data = base64_decode(data)
    if data.startswith("2423"):
        data = cbc_decrypt(data)
    if key:
        data = ecb_decrypt(data, key)
    return data
def get_ext(ext):
    try:
        return base64_decode(get_data(ext[4:]))
    except Exception:
        return ""

def get_data(url):
    if url.startswith("http"):
        urlReq = requests.get(url, verify=False)
        return urlReq.text
    return ""

def ecb_decrypt(data, key):
    spec = AES.new(pad_end(key).encode(), AES.MODE_ECB)
    return spec.decrypt(bytes.fromhex(data)).decode("utf-8")

def cbc_decrypt(data):
    decode = bytes.fromhex(data).decode().lower()
    key = pad_end(decode[decode.index("$#") + 2:decode.index("#$")])
    iv = pad_end(decode[-13:])
    key_spec = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
    data = data[data.index("2324") + 4:-26]
    decrypt_data = key_spec.decrypt(bytes.fromhex(data))
    return decrypt_data.decode("utf-8")

def base64_decode(data):
    extract = extract_base64(data)
    return base64.b64decode(extract).decode("utf-8") if extract else data

def extract_base64(data):
    match = re.search(r"[A-Za-z0-9]{8}\*\*", data)
    return data[data.index(match.group()) + 10:] if match else ""

def pad_end(key):
    return key + "0000000000000000"[:16 - len(key)]

def is_valid_json(json_str):
    try:
        json.loads(json_str)
        return True
    except json.JSONDecodeError:
        return False


main()
