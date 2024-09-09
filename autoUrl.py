import base64
import re
import datetime
import requests
import json
import urllib3
from Crypto.Cipher import AES


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    with open('./url.json', 'r', encoding='utf-8') as f:
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
    fp.write("# 提示\n\n")
    fp.write("感谢各位大佬的无私奉献.\n\n")
    fp.write(
        "如果有收录您的配置，您也不希望被收录请[issues](https://github.com/hl128k/tvbox/issues)，必将第一时间移除\n\n")
    fp.write("# 免责声明\n\n")
    fp.write("本项目（tvbox）的源代码是按“原样”提供，不带任何明示或暗示的保证。使用者有责任确保其使用符合当地法律法规。\n\n")
    fp.write(
        "所有以任何方式查看本仓库内容的人、或直接或间接使用本仓库内容的使用者都应仔细阅读此声明。本仓库管理者保留随时更改或补充此免责声明的权利。一旦使用、复制、修改了本仓库内容，则视为您已接受此免责声明。\n\n")
    fp.write(
        "本仓库管理者不能保证本仓库内容的合法性、准确性、完整性和有效性，请根据情况自行判断。本仓库内容，仅用于测试和学习研究，禁止用于商业用途，不得将其用于违反国家、地区、组织等的法律法规或相关规定的其他用途，禁止任何公众号、自媒体进行任何形式的转载、发布，请不要在中华人民共和国境内使用本仓库内容，否则后果自负。\n\n")
    fp.write(
        "本仓库内容中涉及的第三方硬件、软件等，与本仓库内容没有任何直接或间接的关系。本仓库内容仅对部署和使用过程进行客观描述，不代表支持使用任何第三方硬件、软件。使用任何第三方硬件、软件，所造成的一切后果由使用的个人或组织承担，与本仓库内容无关。\n\n")
    fp.write(
        "所有直接或间接使用本仓库内容的个人和组织，应 24 小时内完成学习和研究，并及时删除本仓库内容。如对本仓库内容的功能有需求，应自行开发相关功能。所有基于本仓库内容的源代码，进行的任何修改，为其他个人或组织的自发行为，与本仓库内容没有任何直接或间接的关系，所造成的一切后果亦与本仓库内容和本仓库管理者无关 \n\n")
    fp.write("# 介绍\n\n")
    fp.write("自用请勿宣传\n\n")
    fp.write("所有数据全部搜集于网络，不保证可用性\n\n")
    fp.write("因电视对GitHub访问问题，所以将配置中的GitHub换成镜像源\n\n")
    fp.write("本次自动更新时间为：" + now.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
    fp.write("当前内容来源详情请查看url.json\n\n")
    fp.write("如果感兴趣,请复制项目后自行研究使用\n\n")
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
