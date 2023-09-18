import requests
import urllib.parse
from ftplib import FTP
import os

ip = "192.168.16.121"
password = "12345678"


def getPerson(ip, password):
    host = "http://" + ip + ":8090"
    findurl = "/person/find"
    params1 = {"pass": password, "id": -1}

    response = requests.get(host + findurl, params=params1)
    # print(response.text)
    res = response.json()
    # print(res['data'])
    if res['code'] == 'LAN_SUS-0':
        for i in res['data']:
            print(i['id'], i['name'])
            getFaceUrl(ip, password, i['id'], i['name'])
        print('获取人员信息成功')
    elif res['code'] == 'LAN_EXP-1001':
        print('密码错误，获取人员信息失败')
    else:
        print('未知错误，获取人员信息失败')


def getFaceUrl(ip, password, id, name):
    host = "http://" + ip + ":8090"
    faceurl = "/face/find"
    params = {"pass": password, "personId": id}
    urlencoded_params = urllib.parse.urlencode(params)
    response = requests.post(host + faceurl, params=urlencoded_params)
    res = response.json()
    if res['code'] == 'LAN_SUS-0':
        print('获取照片成功')
        print(res['data'][0]['path'])
        downloadImg(ip, password, res['data'][0]['path'], id, name)
    elif res['code'] == 'LAN_EXP-1001':
        print('密码错误，获取人员信息失败')
    else:
        print('未知错误，获取人员信息失败')


def downloadImg(ip, password, path, id, name):
    parsed_url = urllib.parse.urlparse(path)
    filename = parsed_url.path.split("/")[-1]
    path_without_filename = "/".join(parsed_url.path.split("/")[:-1])
    ftp = FTP()  # 替换为实际的 FTP 服务器地址
    ftp.connect(ip, 8010)
    ftp.login('admin', password)  # 替换为实际的用户名和密码
    ftp.set_pasv(True)
    ftp.cwd('.' + path_without_filename)  # 替换为实际的 FTP 文件夹路径
    local_filename = os.path.join('./image', id + name + '.jpg')  # 设置文件保存的本地路径
    with open(local_filename, 'wb') as f:
        ftp.retrbinary('RETR ' + filename, f.write)
    print(f'Downloaded {id+name}.jpg')
    # download_file(ftp, filename, id, name)
    ftp.quit()


getPerson(ip, password)
