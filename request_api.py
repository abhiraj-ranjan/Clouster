class call:
    def __init__(self, username=None, password=None, radio=None):
        import requests
        
        try :
            self.session = requests.session()
        except Exception:
            print('Failed to connect')
        self.login(username, password, radio)
        
    def login(self, username, password, radio):    
        #var declare
        self.cbaseurl = 'http://vbpsdel.accevate.com/'
        self.baseurl  = 'https://vbpsdelf.accevate.com/'
        self.urls     = {'online_classes':self.baseurl+'app121/student/online_class/?id=',
                     'online_test':self.baseurl+'app121/online-test?id=',
                     'google_form_test':self.baseurl+'app121/student/google-form-test?id=',
                     'academics':self.cbaseurl+'HTML/Acadmic.php',
                     'personalData':self.cbaseurl+'HTML/Complete-Profile.php',
                     'notice':self.cbaseurl+'HTML/Notice.php',
                     'post-online_classes':self.baseurl+'app121/student/online_class/ajax'}

        #returns TEACHER_ACCESS if radio == TEACHER , location = staff_new/
        #elif    STUDENT_ACCESS if radio == STUDENT , location = HTML/index.php
        #elif    NONE if no radio assigned
        #else    Invalid username and password
        global out
        out = self.session.post(self.cbaseurl+"ajaxLogin.php", data = {"username":username, "password":password, "radios":"STUDENT"})
        
        self._returnText = out.text
        print('api_RETURN : ' + self._returnText)
        self.refresh()

    def refresh(self):
        import re
        src     = self.session.get(self.cbaseurl+"HTML/index.php")
        output  = src.text
        self.id = str(src.text)[str(src.text).find('<li><a href="https://vbpsdelf.accevate.com/app121/student/google-form-test?id=')+len('<li><a href="https://vbpsdelf.accevate.com/app121/student/google-form-test?id='):].split('"')[0]

        print('starting extraction')
        self.getPersonalData()
        self.getNotice()
        self.getAcademicData()
        self.getZoomClasses()
        
        #print(self.Assig, end='\n\n')
        #print(self.id, end='\n\n')
        #print(self.personalData, end='\n\n')
        #print(self.notice, end='\n\n')
        #print(self.zoomLinkData)


    def getNotice(self):
        print('getting notice')
        import bs4
        html  = bs4.BeautifulSoup(self.session.get(self.urls['notice']).text, features="lxml")
        print('data src gained. \nextracting values ...')
        table = html.find('table', attrs={'id':"da-ex-datatable-numberpaging", 'class':"da-table"}) 
        rows  = table.findAll('tr')
        data  = [[td.findChildren(text=True) for td in tr.findAll('td')] for tr in rows]
        data  = [[u"".join(d).strip() for d in l] for l in data]
        del data[0]
        
        links = list()
        for i in table.findAll('a'):
            links.append(str(i).split()[1][6:-1])
            
        for ind, i in enumerate(data):
            i.append(links[ind])
            
        data = [[i for ind, i in enumerate(a) if ind != 0] for a in data]
        
        self.notice = data = [[i for ind, i in enumerate(a) if ind != 3] for a in data]
        print('notice data acquired')
        
    def getZoomClasses(self):
        print("getting today's classes")
        import pandas as pd
        import re
        import numpy as np
        import requests

        log          = self.session.get("https://vbpsdelf.accevate.com/app121/student/online_class/?id="+self.id)
        html         = log.text
        print('data source gained.\nExtracting Data ...')
        table        = pd.read_html(html)[0]
        list_periods = table.get('Period').to_list()
        list_periods = [re.findall('\(.*?\)', i)[0][1:-1] for i in list_periods]
        numpy_table  = table.to_numpy()

        start     = 0
        add_attrs = {}
        link_data = []
        links     = list()
        
        while html.find('data-live_link=', start) != -1:
            a = html.find('data-live_link=', start)
            attrs = html[a+len('data-live_link='):].split()
            add_attrs[attrs[7].split('"')[1]] = attrs[0][1:-1]

            live_link  = attrs[0][1:-1]
            adm_no     = attrs[1][1:-1]
            stu_id     = attrs[2][1:-1]
            session    = attrs[3][1:-1]
            period     = attrs[4][1:-1]
            subject    = attrs[5][1:-1]
            
            start = a+1

        for i in range(len(list_periods)):
            numpy_table[i][0]     = list_periods[i]
            if list_periods[i] in add_attrs:
                numpy_table[i][2] = add_attrs[list_periods[i]]
            else:
                numpy_table[i][2] = 'NO LINK'
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        
        #table['join'] = ['' for i in range(table.shape[0])]

        self.zoomlinks = table
        print('data analyse complete')

    def getAcademicData(self):
        print('getting Academic Data')
        import bs4
        html  = bs4.BeautifulSoup(self.session.get(self.urls['academics']).text, features="lxml")
        print('Data source gained.\nAnalysing data ...')
        table = html.find('table', attrs={'id':'da-ex-datatable-numberpaging', 'class':'da-table'}) 
        rows  = table.findAll('tr')
        data  = [[td.findChildren(text=True) for td in tr.findAll('td')] for tr in rows]
        data  = [[u"".join(d).strip() for d in l] for l in data]
        del data[0]
        data  = [[i for ind, i in enumerate(a) if ind != 0] for a in data]
        
        links = list()
        for i in table.findAll('a'):
            links.append(str(i).split()[1][6:-1])
            
        for ind, i in enumerate(data):
            i.append(links[ind])
        
        self.Assig = [[i for ind, i in enumerate(a) if ind != 2] for a in data]
        print('Academic Data extracted.')
    
    def getPersonalData(self):
        
        import bs4
        print('getting personal data')
        _src = self.session.get(self.urls['personalData']).text
        html = bs4.BeautifulSoup(_src, features="lxml")

        print('data source gained.\nAnalysing data ...')
        
        name  = _src[_src.find('id="ctl00_ContentPlaceHolder1_LBLNAme">')+39:].split('</span>')[0]
        table = html.find('table', attrs={'class':'da-table da-detail-view'})
        rows  = table.findAll('tr')
        data  = [[td.findChildren(text=True) for td in tr.findAll('td')] for tr in rows]
        data  = [[u"".join(d).strip() for d in l] for l in data]
        self.personalData = {q[0].split(':')[0].strip(): q[1] for q in data}

        src    = self.session.get("http://vbpsdel.accevate.com/HTML/index.php").text
        print(src[str(src).find('<object class="responsive" data=')+len('<object class="responsive" data="'):].split()[0][:-1])
        pic    = self.session.get(src[str(src).find('<object class="responsive" data=')+len('<object class="responsive" data="'):].split()[0][:-1]).content
        with open('./icons/user.jpeg', 'wb') as file:
            file.write(pic)
        _class = src[src.find('<span style="color:black;font-weight:bold;">Class : </span><b>')+62:].split('</b><br />')[0]
        
        self.personalData['pic']   = pic
        self.personalData['name']  = name
        self.personalData['class'] = _class
        print('personal Data extracted')
        
    def markattendence_class(self, adm_no='', stu_id='', session='', period='', subject=''):
        self.session.post(self.mbaseurl+'app121/student/online_class/ajax', data={"stu_id":stu_id, "adm_no":adm_no, "session":session, "period":period, "subject":subject, "ajax":1, "action":"save_attendance"})


#sess = call(username='abh133')
