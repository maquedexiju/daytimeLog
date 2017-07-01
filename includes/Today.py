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

#global BASEPATH

#Builder.load_file('includes/Controls/Timer.kv')
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
        self.menu.Init(Save=self.SaveLog,Export=self.ExportLog)
        self.navigator.Init(0)
        #self.log.viewMode=True
        self.Refresh()

    def SaveLog(self,instance=None):
        data=self.log.GetLog()
        if data:
            self.DB.Save(data)

    def ExportLog(self,instance=None):
        data=self.log.GetLog()
        filePath=self.BASEPATH+'tmp.csv'
        with open(filePath, 'w') as csvFile:
            fieldNames=['ID', ''''Date',''' 'Start Time','Duration','Tag','Content']
            writer=csv.DictWriter(csvFile, fieldnames=fieldNames)
            writer.writeheader()
            writer.writerow({'ID':data[0]['day']})
            for record in data:
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
    '''
    def EditLog(self,*args):
        self.menu.EnterEdit()
        self.log.EnterEdit()

    def LeaveEdit(self):
        self.log.LeaveEdit()
    '''

    def Refresh(self):
        now=date.today()-timedelta(days=1)
        if self.date!=datetime.strftime(now,'%Y-%m-%d'):
            LogThisDay=self.DB.SearchDate(now)
            self.date=datetime.strftime(now,'%Y-%m-%d')
            self.log.DrawLog(LogThisDay,self.date)