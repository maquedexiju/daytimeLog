from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from includes.Controls.AdaptView import AdaptView
from includes.Controls.Navigator import Navigator
from includes.Controls.Menu import Menu
from includes.Controls.Timer import Timer
from includes.Controls.Log import Log
import re
from datetime import *
import csv
import platform
import subprocess

Builder.load_file('includes/Today.kv')

class TodayView(AdaptView):
    timer=ObjectProperty(None)
    menu=ObjectProperty(None)
    log=ObjectProperty(None)
    navigator=ObjectProperty(None)
    recordIndex=[]
    date=None
    def __init__(self,screenName,sysArgs,**kwargs):
        super(TodayView,self).__init__(screenName,sysArgs,**kwargs)
        #self.menu.Init(Save=self.SaveLog,Export=self.ExportLog)
        self.menu.Init(Export=self.ExportLog)
        self.navigator.Init(0)
        #self.log.viewMode=True
        self.Refresh()

    def SaveLog(self,instance=None):
        data=self.log.GetLog()
        self.DB.Save(data)

    def ExportLog(self,instance=None):
        data=self.log.GetLog()
        filePath=self.FILEPATH+'tmp.csv'
        with open(filePath, 'w',encoding='utf-8') as csvFile:
            fieldNames=['ID','Start Time','Duration','Tag','Content']
            writer=csv.DictWriter(csvFile, fieldnames=fieldNames)
            writer.writeheader()
            day=None
            for record in data:
                if record['day']!=day:
                    writer.writerow({'ID':record['day']})
                    day=record['day']
                writer.writerow({'ID':record['id'],\
                #'Date':record['day'],\
                'Start Time':record['time'],\
                'Duration':record['duration'],\
                'Tag':record['tag'],\
                'Content':record['job']})
            sys=platform.system()
            if sys=='Window':
                os.startfile(filePath)
            elif sys=='Linux':
                subprocess.call(["xdg-open", filePath])
            elif sys=='Darwin':
                subprocess.call(["open", filePath])

    def Refresh(self):
        now=date.today()
        if self.date!=datetime.strftime(now,'%Y-%m-%d'):
            LogThisDay=self.DB.SearchDate(now)
            self.date=datetime.strftime(now,'%Y-%m-%d')
            self.log.Clear()
            self.log.DrawLog(LogThisDay,self.date)

    def on_enter(self,*args):
        def tmpfunction(time=None):
            now=date.today()
            LogThisDay=self.DB.SearchDate(now)
            self.date=datetime.strftime(now,'%Y-%m-%d')
            self.SaveLog()
            self.log.Clear()
            self.log.DrawLog(LogThisDay,self.date)
        Clock.schedule_once(tmpfunction,0.2)
        super(TodayView, self).on_enter()

    def on_leave(self,*args):
        self.SaveLog()
        super(TodayView,self).on_leave()
