#!/usr/bin/env python
# Funtion:  文件校验工具
# Author:   tengjuyuan
# Filename: MD5_Hash.py

__Author__ = "tengjuyuan"

import wx
import os,time
import hashlib
import binascii

# wildcard = u"Python 文件 (*.py)|*.py|" \
#            u"编译的 Python 文件 (*.pyc)|*.pyc|" \
#            u" 垃圾邮件文件 (*.spam)|*.spam|" \
#            "Egg file (*.egg)|*.egg|" \
#            "All files (*.*)|*.*"

class MD5_Hash_Frame(wx.Frame):
    def __init__(self, parent):
        # wx.Frame.__init__(self, parent, -1, "MD5-Hash tools V1.0", size=(600,400))
        super(MD5_Hash_Frame, self).__init__(parent, -1, "MD5-Hash tools V1.0  --by tengjuyuan ", size=(600,420))
        panel = wx.Panel(self)
        self.setupMenuBar(panel)
        self.Show(True)

    def setupMenuBar(self, parent):
        # 创建文本框
        self.t1 = wx.TextCtrl(parent, size = (550, 260), pos = (15,10),style=wx.TE_MULTILINE )
        # 创建按钮
        self.find_button = wx.Button(parent, -1, u"浏览(B)...", (16, 280), (80,30) )    # size = (70,25),
        self.clear_button = wx.Button(parent, -1, u"清除(L)", (16+96,280), (80,30))
        self.copy_button = wx.Button(parent, -1, u"复制(C)", (16+96*2, 280), (80,30))
        self.save_button = wx.Button(parent, -1, u"保存(S)", (16+96*3, 280), (80,30))
        self.stop_button = wx.Button(parent, -1, u"停止(T)", (16+96*4, 280), (80,30))
        # 创建选择盒子
        self.version_box = wx.CheckBox(parent, -1, u"版本(V)", (500,280))
        self.time_box = wx.CheckBox(parent, -1, u"时间(D)", (500, 280+20))
        self.md5_box = wx.CheckBox(parent, -1, u"MD5(M)", (500, 280+20*2))
        self.sha1_box = wx.CheckBox(parent, -1, u"SHA1(H)", (500, 280+20*3))
        self.crc32_box = wx.CheckBox(parent, -1, u"CRC32(R)", (500, 280+20*4))
        # 创建进度条
        self.static1 = wx.StaticText(parent, -1, '文件',pos=(20,320),size=(50,25))
        self.static2 = wx.StaticText(parent, -1, '总计',pos=(20,350),size=(50,25))
        self.sigle_gauge = wx.Gauge(parent, -1, 100, (60, 320), (420,20))
        self.totle_gauge = wx.Gauge(parent, -1, 100, (60, 350), (420,20))
        # self.gauge.SetBezelFace(3)
        # self.gauge.SetShadowWidth(3)
        # 设置默认值
        self.version_box.SetValue(True)
        self.time_box.SetValue(True)
        self.md5_box.SetValue(True)
        self.sha1_box.SetValue(True)
        self.crc32_box.SetValue(True)
        self.stop_button.Enable(False)

        # 绑定事件
        self.Bind(wx.EVT_CLOSE, self.closewindows)
        self.Bind(wx.EVT_BUTTON, self.find_file, self.find_button)
        self.Bind(wx.EVT_BUTTON, self.clear_text, self.clear_button)
        self.Bind(wx.EVT_BUTTON, self.copy_text, self.copy_button)
        self.Bind(wx.EVT_BUTTON, self.save_file, self.save_button)
        self.Bind(wx.EVT_BUTTON, self.stop_calc, self.stop_button)

        # self.Bind(wx.EVT_IDLE, self.onidle)
        self.file_cnt = 0
        self.deal_file_cnt = 0

    def find_file(self,event):
        ''' 打开目录，浏览文件 '''
        dlg = wx.FileDialog(None, "选择散列值文件",
                        os.getcwd(),
                        defaultFile="",
                        style=wx.FD_OPEN| wx.FD_MULTIPLE
                        )   #wildcard=wildcard
        info = ""
        if dlg.ShowModal() == wx.ID_OK:
            self.file_cnt = len(dlg.GetPaths())
            self.totle_gauge.SetRange(100 * self.file_cnt)
            for index,path in enumerate(dlg.GetPaths()):    # 依次循环各个文件
                self.sigle_gauge.SetValue(0)
                self.totle_gauge.SetValue(0)
                if self.version_box.GetValue():
                    info += "文件："+path+"\n"
                info += "大小：" + str(self.getfile_info(path)[0]) + "字节\n"
                if self.time_box.GetValue():
                    info += "修改时间："+self.getfile_info(path)[1] + "\n"
                md5 = self.gethash_info(path)
                if self.md5_box.GetValue():
                    info += "MD5：" + md5[0] + "\n"
                if self.sha1_box.GetValue():
                    info += "SHA1：" + md5[1] + "\n"
                if self.crc32_box.GetValue():
                    info += "CRC32："  + self.getCRC32_info(path)  + "\n"
                info += "\n"
                self.sigle_gauge.SetValue(100)
                self.totle_gauge.SetValue(100 * (index+1))

        self.t1.SetValue(info)
        # print(info)

    def clear_text(self, event):
        ''' 清除文本框内容 '''
        self.t1.Clear()

    def copy_text(self, event):
        ''' 复制文本框内容 '''
        text_obj = wx.TextDataObject()
        text_obj.SetText(self.t1.GetValue())
        # wx.TheClipboard.Open()
        if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():    # 打开剪切板
            wx.TheClipboard.SetData(text_obj)
            wx.TheClipboard.Flush()
        else:
            wx.MessageBox("Unable to open the clipboard", "Error")
        wx.TheClipboard.Close()

    def save_file(self, event):
        '''将文本框内容保存到文件 '''
        wildcard = "Text Files (*.txt)|*.txt|" "All files (*.*)|*.*"
        dlg = wx.FileDialog(None, u"选择散列值文件",
                            os.getcwd(),
                            defaultFile="",
                            style=wx.FD_SAVE,   #|wx.FD_OVERWRITE_PROMPT
                            wildcard=wildcard
                            )
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.t1.GetValue())     # 将文本框中的内容写入到文件中

    def stop_calc(self, event):
        ''' 停止计算 '''
        pass

    def closewindows(self, envet):
        self.Destroy()

    def getfile_info(self,path):
        '''获得文件的相关信息'''
        size = os.stat(path).st_size
        modtime = os.path.getmtime(path)
        offtime = time.strftime('%z',time.localtime())
        offtime_second = int(offtime[1:3])*60*60+int(offtime[3:])*60
        if offtime[0] == "+":
            modtime += offtime_second
        elif offtime[0] == "-":
            modtime -= offtime_second
        modtime = time.strftime(u"%Y-%m-%d  %H:%M:%S", time.gmtime(modtime))
        return (size, modtime)

    def gethash_info(self, path):
        '''获得文件的MD5，SHA1校验值'''
        with open(path, 'rb') as f:
            md5 = hashlib.md5()
            sha1 = hashlib.sha1()
            for i in f:
                md5.update(i)
                sha1.update(i)
            return (md5.hexdigest().swapcase(), sha1.hexdigest().swapcase())

    def getCRC32_info(self, path):
        ''' 获得文件的CRC32校验值 '''
        with open(path, 'rb') as f:
            return '%X' % (binascii.crc32(f.read()) & 0xffffffff)

    def __del__(self):
        pass
        # self.Destroy()

if __name__ == "__main__":
    app = wx.App()
    frame = MD5_Hash_Frame(None)
    app.MainLoop()  # 循环监听事件