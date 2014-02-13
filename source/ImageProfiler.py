	#!/usr/bin/python

import sys
import os
import wx

class PrimaryFrame(wx.Frame):
	""" Create custom frame class """
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(200,100))
		self.control = wx.TextCtrl(self, style=wx.TE_LEFT)
		self.Show(True)

def main():
	print("Test code; please remove")
	app = wx.App(False)
	frame = PrimaryFrame(None, "Image Profiler")
	frame.Show(True)
	app.MainLoop()
	print("Done")


if  __name__ =='__main__':
	main()