# url编译包
from urllib import parse

url = 'https://www.iqiyi.com/v_19rrfzbn2c.html'
# 反斜杠 字符集
# a=parse
# Tk 消息盒子包 当程序错误 弹窗提示
import tkinter.messagebox as msg
# 做桌面编程
import tkinter as tk
# 控制浏览器的包 当用户点击了播放的时候会调用这个包
import webbrowser

# 正则表达式 判断用户输入的网址 是否有错误
import re

'''
基于类编程
方便扩展 二次开发
手机支持 生成二维码 二维码包含了解析网址的所有信息 直接跳转到解析网站
pyinstaller -F -w -i D:\home\lrn\favicon.ico play_video.py

'''


class App:
	def __init__(self, width=500, height=300):
		self.w = width
		self.h = height
		self.title = '荣先生_视频破解'
		# 软件名
		self.root = tk.Tk(className=self.title)
		# vip视频播放地址 字符串类型
		self.url = tk.StringVar()
		# 定义播放源 视频播放通道 整形类型
		self.v = tk.IntVar()
		# 默认选择 第一个
		self.v.set(1)
		# 定义软件的布局 空间
		# Frame空间 定义了2个空间，名字都叫
		frame_1 = tk.Frame(self.root)
		frame_2 = tk.Frame(self.root)
		# 控件内容设置 按钮 button 输入框
		group = tk.Label(frame_1, text='暂时只有一个播放通道：', padx=10, pady=10)
		tb = tk.Radiobutton(frame_1, text='唯一通道', variable=self.v, value=1, width=10, height=3)

		label = tk.Label(frame_2, text='请输入视频链接：', padx=10, pady=10)
		# 定义输入框
		entry = tk.Entry(frame_2, textvariable=self.url, highlightcolor='Fuchsia', highlightthickness=1, width=35)
		# command 绑定函数 输入字符 点击播放 需要电泳video_play这个函数去做
		play = tk.Button(frame_2, text='播放', font=('楷体', 12), fg='Purple', width=2, height=1, command=self.video_play)

		# 控件布局
		frame_1.pack()  # 显示控件
		frame_2.pack()

		# 确定控件在软件中的位置
		group.grid(row=0, column=0)  # row 是行，column列
		tb.grid(row=0, column=1)
		label.grid(row=0, column=0)  # 空间2的
		entry.grid(row=0, column=1)
		play.grid(row=0, column=3, ipadx=10, ipady=10)  # 设置位置

	def video_play(self):
		# 视频解析网址
		port = 'http://www.wmxz.wang/video.php?url='
		# 做判断
		if re.match(r'^https?:/{2}\w.+$', self.url.get()):
			# 拿到
			ip = self.url.get()
			print('ip',ip)
			# 然后做视频播放地址编码
			ip = parse.quote_plus(ip)
			# 自动打开浏览器 指向用户输入的视频播放网址
			webbrowser.open(port + ip)
		else:
			msg.showerror(title='错误', message='视频地址无效,请重新输入！')

	def loop(self):
		# 自由拖软件大小
		self.root.resizable(True, True)
		self.root.mainloop()


if __name__ == '__main__':
	app = App()
	app.loop()
