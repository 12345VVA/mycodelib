import wx
import os
import PyPDF2
import time
'''
file_path = os.getcwd()
print(file_path)
print(os.path.realpath(__file__))
print(os.path.split(os.path.realpath(__file__)))
'''

# pdf1 = r'C:\Users\显为技术\OneDrive\桌面显为智能科技(苏州)有限公司-环境管理与扬尘监测系统.pdf'
# pdf2 = r'C:\Users\显为技术\OneDrive\桌面显为智能科技(苏州)有限公司-环境管理与扬尘监测系统.pdf'
# pdf3 = r'C:\Users\显为技术\OneDrive\桌面显为智能科技(苏州)有限公司-环境管理与扬尘监测系统.pdf'
# pdf4 = r'E:\Desktop\1\4.pdf'
# pdf5 = r'E:\Desktop\1\5.pdf'

# file_pdf = PdfFileMerger()
# file_pdf.append(pdf1)
# file_pdf.append(pdf2)
# file_pdf.append(pdf3)
# file_pdf.append(pdf4)
# file_pdf.append(pdf5)


# file_pdf.write(r"E:\Desktop\1\6.pdf")
class RefactorExample(wx.Frame):
    InFile = {}
    InFileNum = 0
    OutFile = os.getcwd()

    def __init__(self, parent, id, size):
        wx.Frame.__init__(self,
                          parent,
                          id,
                          "PDF合并",
                          style=wx.CAPTION | wx.CLOSE_BOX | wx.FRAME_SHAPED,
                          size=size)
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour("White")
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.createMenuBar()
        # 打开文件按钮
        self.OpenButton = wx.Button(panel,
                                    -1,
                                    "打开文件",
                                    size=(80, 30),
                                    pos=(10, 10))
        self.Bind(wx.EVT_BUTTON, self.OnOpenButton, self.OpenButton)
        # 选择输出文件夹按钮
        self.OutButton = wx.Button(panel,
                                   -1,
                                   "输出文件夹",
                                   size=(80, 30),
                                   pos=(100, 10))
        self.Bind(wx.EVT_BUTTON, self.OnOutButton, self.OutButton)
        # 输出文件夹显示框
        self.OutText = wx.TextCtrl(panel, -1, size=(230, 30), pos=(190, 10))
        # 调试信息显示框
        self.Inform = wx.TextCtrl(panel,
                                  -1,
                                  size=(320, 260),
                                  pos=(10, 50),
                                  style=wx.TE_MULTILINE)
        # 开始合并按钮
        self.StartButton = wx.Button(panel,
                                     -1,
                                     "开始合并",
                                     size=(80, 30),
                                     pos=(340, 50))
        self.Bind(wx.EVT_BUTTON, self.OnStart, self.StartButton)

    def menuData(self):
        return (("&文件", ("&打开", "&Open in status", self.OnOpen),
                 ("&退出", "Quit", self.OnCloseWindow)),
                ("&编辑", ("&复制", "Copy", self.OnCopy),
                 ("&剪切", "Cut", self.OnCut), ("&粘贴", "Paste", self.OnPaste),
                 ("", "", ""), ("&选项", "DisplayOptions", self.OnOptions)))

    def createMenuBar(self):
        menuBar = wx.MenuBar()
        for eachMenuData in self.menuData():
            menuLabel = eachMenuData[0]
            menuItems = eachMenuData[1:]
            menuBar.Append(self.createMenu(menuItems), menuLabel)
        self.SetMenuBar(menuBar)

    def createMenu(self, menuData):
        menu = wx.Menu()
        for eachLabel, eachStatus, eachHandler in menuData:
            if not eachLabel:
                menu.AppendSeparator()
                continue
            menuItem = menu.Append(-1, eachLabel, eachStatus)
            self.Bind(wx.EVT_MENU, eachHandler, menuItem)
        return menu

    def OnOpenButton(self, event):
        self.InFile[self.InFileNum] = wx.FileSelector(message="选择一个文件",
                                                      default_path="",
                                                      default_filename="",
                                                      default_extension="",
                                                      wildcard="*.pdf",
                                                      flags=0,
                                                      parent=None,
                                                      x=-1,
                                                      y=-1)
        self.InFileNum = self.InFileNum + 1
        self.Inform.AppendText(
            os.path.basename(self.InFile[self.InFileNum - 1]) + "\n")

    def OnOutButton(self, event):
        self.OutFile = wx.DirSelector(message="选择输出文件夹",
                                      default_path="",
                                      style=0,
                                      pos=wx.DefaultPosition,
                                      parent=None)
        self.OutText.AppendText(self.OutFile)

    def OnStart(self, event):
        NewPdf = PyPDF2.PdfFileMerger()
        for i in range(0, self.InFileNum, 1):
            try:
                NewPdf.append(self.InFile[i])
            except UserWarning:
                print("文件读取失败")
            except:
                pass
            else:
                pass
        NowTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        try:
            NewPdf.write(self.OutFile + os.sep + str(NowTime) + "out.pdf")
        except:
            self.Inform.AppendText("合并失败，权限不足\n")
        else:
            self.Inform.AppendText("合并成功，文件路径" + self.OutFile + "\n")
        self.InFile = {}
        self.InFileNum = 0

    def OnPrev(self, event):
        pass

    def OnNext(self, event):
        pass

    def OnLast(self, event):
        pass

    def OnFirst(self, event):
        pass

    def OnOpen(self, event):
        pass

    def OnCopy(self, event):
        pass

    def OnCut(self, event):
        pass

    def OnPaste(self, event):
        pass

    def OnOptions(self, event):
        pass

    def OnCloseWindow(self, event):
        self.Destroy()


class HomeApp(wx.App):

    def __init__(self):
        wx.App.__init__(self)
        frame = RefactorExample(parent=None, id=-1, size=(450, 380))
        frame.Show()


if __name__ == '__main__':
    app = HomeApp()
    app.MainLoop()
