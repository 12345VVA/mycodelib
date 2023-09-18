import wx
import requests
import urllib.parse
from urllib.parse import urlparse
import os
import time
from ftplib import FTP

outFile = os.getcwd()


class HelloFrame(wx.Frame):

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(HelloFrame, self).__init__(*args, **kw)

        # create a panel in the frame
        panel = wx.Panel(self)
        # IP输入框
        wx.StaticText(panel, -1, 'IP:', size=(30, 20), pos=(10, 10))
        self.IpText = wx.TextCtrl(panel, -1, size=(100, 20), pos=(40, 10))
        # 密码输入框
        wx.StaticText(panel, -1, '密码:', size=(30, 20), pos=(160, 10))
        self.PassText = wx.TextCtrl(panel, -1, size=(100, 20), pos=(200, 10))
        # 创建连接
        self.CreateConnect = wx.Button(panel,
                                       -1,
                                       "读取序列号",
                                       size=(60, 20),
                                       pos=(310, 10))
        self.Bind(wx.EVT_BUTTON, self.OnCreateConnect, self.CreateConnect)
        # 选择输出文件夹按钮
        self.OutFile = wx.Button(panel,
                                 -1,
                                 "选择文件夹",
                                 size=(80, 30),
                                 pos=(10, 40))
        self.Bind(wx.EVT_BUTTON, self.OnOutFile, self.OutFile)
        # 开始导出
        self.Start = wx.Button(panel, -1, "开始导出", size=(80, 30), pos=(100, 40))
        self.Bind(wx.EVT_BUTTON, self.OnStart, self.Start)
        # 调试信息显示框
        self.Inform = wx.TextCtrl(panel,
                                  -1,
                                  size=(370, 130),
                                  pos=(10, 80),
                                  style=wx.TE_MULTILINE)

    def OnCreateConnect(self, event):
        ip = self.IpText.GetValue()
        self.content(ip)

    def OnStart(self, event):
        ip = self.IpText.GetValue()
        password = self.PassText.GetValue()
        if ip == '' or password == '':
            self.Inform.AppendText("请输入设备IP地址以及密码\n")
        else:
            self.Inform.AppendText("照片存放目录" + outFile + "\n")
            self.getPerson(ip, password)

    def OnOutFile(self, event):
        self.OutFile = wx.DirSelector(message="选择输出文件夹",
                                      default_path="",
                                      style=0,
                                      pos=wx.DefaultPosition,
                                      parent=None)
        global outFile
        outFile = self.OutFile
        self.Inform.AppendText(self.OutFile)

    def content(self, ip):
        url = 'http://' + ip + ':8090/getDeviceKey'
        try:
            response = requests.get(url, timeout=(5, 15))
            # print(response.text)
            res = response.json()
            if res['code'] == "LAN_SUS-0":
                self.Inform.AppendText("连接成功:" + res['data'] + "\n")
            else:
                self.Inform.AppendText("连接失败:\n")
            # print(res)
        except:
            self.Inform.AppendText("连接失败:\n")

    def getPerson(self, ip, password):
        host = "http://" + ip + ":8090"
        findurl = "/person/find"
        params1 = {"pass": password, "id": -1}
        try:
            response = requests.get(host + findurl,
                                    params=params1,
                                    timeout=(5, 15))
            # print(response.text)
            res = response.json()
            # print(res['data'])
            if res['code'] == 'LAN_SUS-0':
                self.Inform.AppendText("获取人员信息成功！\n")
                for i in res['data']:
                    # print(i['id'], i['name'])
                    time.sleep(0.3)
                    self.getFaceUrl(ip, password, i['id'], i['name'])
                self.Inform.AppendText("照片导出完成！\n")
            elif res['code'] == 'LAN_EXP-1001':
                self.Inform.AppendText("密码错误\n")
            else:
                self.Inform.AppendText("未知错误！\n")
        except:
            self.Inform.AppendText("获取人员信息失败，请检查IP地址是否正确\n")

    def getFaceUrl(self, ip, password, id, name):
        host = "http://" + ip + ":8090"
        faceurl = "/face/find"
        params = {"pass": password, "personId": id}
        urlencoded_params = urllib.parse.urlencode(params)
        try:
            response = requests.post(host + faceurl, params=urlencoded_params)
            res = response.json()
            if res['code'] == 'LAN_SUS-0':
                # print('获取照片成功')
                # print(res['data'][0]['path'])
                self.Inform.AppendText("获取" + id + name + "照片成功！" +
                                       res['data'][0]['path'] + "\n")
                parsed_url = urlparse(res['data'][0]['path'])
                if parsed_url.scheme == "ftp":
                    self.downloadFtp(ip, password, res['data'][0]['path'], id,
                                     name)
                elif parsed_url.scheme == "http":
                    self.downloadHttp(res['data'][0]['path'],
                                      id + name + '.jpg')
                else:
                    pass
            elif res['code'] == 'LAN_EXP-1001':
                self.Inform.AppendText("获取" + id + name + "照片失败！\n")
            else:
                self.Inform.AppendText("未知错误！\n")
        except:
            self.Inform.AppendText("获取" + id + name + "照片地址失败！\n")

    def downloadHttp(self, url, new_name):
        global outFile
        response = requests.get(url)
        if response.status_code == 200:
            with open(outFile + '\\' + new_name, 'wb') as f:
                f.write(response.content)
        else:
            print(f"请求失败，状态码为 {response.status_code}")

    def downloadFtp(self, ip, password, path, id, name):
        parsed_url = urllib.parse.urlparse(path)
        filename = parsed_url.path.split("/")[-1]
        path_without_filename = "/".join(parsed_url.path.split("/")[:-1])
        try:
            ftp = FTP()  # 替换为实际的 FTP 服务器地址
            ftp.connect(ip, 8010)
            ftp.login('admin', password)  # 替换为实际的用户名和密码
            ftp.set_pasv(True)
            ftp.cwd('.' + path_without_filename)  # 替换为实际的 FTP 文件夹路径
            local_filename = os.path.join(outFile, id + name + '.jpg')
            # 设置文件保存的本地路径
            with open(local_filename, 'wb') as f:
                ftp.retrbinary('RETR ' + filename, f.write)
            # print(f'Downloaded {id+name}.jpg')
            ftp.quit()
        except:
            self.Inform.AppendText("照片存储失败！\n")
            time.sleep(0.1)


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = HelloFrame(None, title='人员照片导出工具')
    frm.Show()
    app.MainLoop()
