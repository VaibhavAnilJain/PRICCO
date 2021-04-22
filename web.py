from flask import Flask, render_template, redirect, request, url_for, session
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
from flask_mysqldb import MySQL
import requests, time, urllib, MySQLdb.cursors
import wptools,re


web = Flask(__name__)

web.secret_key = 'PRICCO_WEB_123$&'

web.config['MYSQL_USER'] = 'root'
web.config['MYSQL_PASSWORD'] = ''
web.config['MYSQL_DB'] = 'pricco'
web.config['MYSQL_HOST'] = '127.0.0.1'


mysql = MySQL(web)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
           "Accept-Encoding": "gzip, deflate",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
           "Connection": "close", "Upgrade-Insecure-Requests": "1"}

def bubbleSort(a, b, c, d):
    n = len(a)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                b[j], b[j + 1] = b[j + 1], b[j]
                c[j], c[j + 1] = c[j + 1], c[j]
                d[j], d[j + 1] = d[j + 1], d[j]

def bubbleSortsecond(a, b, c):
    n = len(a)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                b[j], b[j + 1] = b[j + 1], b[j]
                c[j], c[j + 1] = c[j + 1], c[j]

@web.route('/')
def Home():
    if 'LoggedIn' in session:
        return render_template('Home.html')
    return render_template('Home.html')

@web.route('/Register', methods=['POST', 'GET'])
def Register():
    if request.method == 'POST':
        Fname = request.form['RegisterInputFirstName']
        Lname = request.form['RegisterInputLastName']
        Email = request.form['RegisterInputEmail']
        Paswd = request.form['RegisterInputPassword']
        Phone = request.form['RegisterInputPhoneNo']

        cur = mysql.connection.cursor()
        cur.execute("SELECT Email FROM USERS WHERE Email ='" + Email + "'")
        Email_Exist = cur.fetchone()

        cur.execute("SELECT Phone FROM USERS WHERE Phone ='" + Phone + "'")
        Phone_Exist = cur.fetchone()

        if Email_Exist:
            ErMessage = 'User Already Exist!!'
            return render_template('Register.html', ErMessage = ErMessage)
        elif Phone_Exist:
            ErMessage = 'Phone No. Already Exist!!'
            return render_template('Register.html', ErMessage = ErMessage)
        else:
            cur.execute("INSERT INTO USERS (Fname, Lname, Email, Paswd, Phone) VALUES (%s, %s, %s, %s, %s)", (Fname, Lname, Email, Paswd, Phone))
            mysql.connection.commit()
            return render_template('Login.html')

    return render_template('Register.html')

@web.route('/Login', methods=['POST', 'GET'])
def Login():
    if request.method == 'POST':
        Email = request.form['LoginInputEmail']
        Paswd = request.form['LoginInputPassword']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM USERS WHERE Email = '" + Email + "' AND Paswd = '" + Paswd + "'")
        AccDetails = cur.fetchone()

        if AccDetails:
            session['LoggedIn'] = True
            session['Id'] = AccDetails['Id']
            session['Fname'] = AccDetails['Fname']
            session['Lname'] = AccDetails['Lname']
            session['Email'] = AccDetails['Email']
            session['Phone'] = AccDetails['Phone']
            return render_template('Home.html')
        else:
            ErMessage = 'Email Id or Password Invalid!!'
            return render_template('Login.html', ErMessage = ErMessage)

    return render_template('Login.html')

@web.route('/Logout')
def Logout():
    session.pop('LoggedIn', None)
    session.pop('Id', None)
    session.pop('Fname', None)
    session.pop('Lname', None)
    session.pop('Email', None)
    session.pop('Phone', None)
    return redirect(url_for('Home'))

@web.route('/NewPassword')
def NewPassword():
    return render_template('NewPassword.html')

@web.route('/UpdatePassword', methods=['POST', 'GET'])
def UpdatePassword():
    if request.method == 'POST':
        Email = request.form['NewPasswordInputEmail']
        Phone = request.form['NewPasswordInputPhoneNo']
        NewPaswd = request.form['NewPasswordInputPassword']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("UPDATE USERS SET Paswd='" + NewPaswd + "' WHERE Email ='" + Email + "' OR Phone ='" + Phone + "'")
        mysql.connection.commit()

        ErMessage = "Your Password has successfully Changed. Now you can go Back and Login"

        return render_template('NewPassword.html', ErMessage = ErMessage)

    return render_template('NewPassword.html')

@web.route('/DeleteAccount/<string:Id>', methods=['POST', 'GET'])
def DeleteAccount(Id):
    if request.method == 'POST':
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("DELETE FROM USERS WHERE Id = {0}".format(Id))
        mysql.connection.commit()

        return redirect(url_for('Logout'))

@web.route('/HelpMessage/<string:Id>', methods=['POST', 'GET'])
def HelpMessage(Id):
    if request.method == 'POST':
        Message = request.form['MsgTextarea']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE USERS SET Message ='" + Message + "' WHERE Id = {0}".format(Id))
        mysql.connection.commit()

        disp_msg = "Sorry for the problem you have faced. We have received your issue and try to solve as soon as possible... ✍(◔◡◔)"

        return render_template('Profile.html', disp_msg = disp_msg)

@web.route('/ProductPrice')
def ProductPrice():
    if 'LoggedIn' in session:
        return render_template('ProductPrice.html')
    return render_template('ProductPrice.html')

@web.route('/Accessories')
def Accessories():
    if 'LoggedIn' in session:
        return render_template('Accessories.html')
    return render_template('Accessories.html')

@web.route('/AccessoriesSearch', methods=['POST', 'GET'])
def AccessoriesSearch():
    if request.method == 'POST':
        Search = request.form['Search']

        def Amazon():
            Amazon = []
            AmzNam = []
            AmzPrc = []
            APrice = []
            AmzNamFet = []
            AmzLinks = []
            AmzLink = []
            AmzImgs = []
            AmzImg = []
            AmazonDetails = []

            AmazonSeperator = '+'
            Amazon = Search.split(" ")
            AmazonSrc = AmazonSeperator.join(Amazon)

            AmazonLink = "https://amazon.in"
            AmazonSource = "https://www.amazon.in/s?k=" + AmazonSrc
            AmazonRequest = requests.get(AmazonSource, headers = headers)
            AmazonSoup = BeautifulSoup(AmazonRequest.content, features = "lxml")
            # anp = AmazonSoup.find_all('span', class_="a-size-medium a-color-base a-text-normal")
            # nm = []
            # nn = anp.span.find(class_="a-size-medium a-color-base a-text-normal")
            # print(nn)

            AmazonImgPage = urllib.request.urlopen(AmazonSource)
            AmazonImgSrc = BeautifulSoup(AmazonImgPage, features = "lxml")

            for i in AmazonSoup.find_all('span', class_="a-size-medium a-color-base a-text-normal"):
                string = i.text
                AmzNam.append(string.strip())

            for i in AmazonSoup.find_all('span', class_="a-price-whole"):
                string = i.text
                AmzPri = string.strip()
                AmzPriSrt = AmzPri.replace(',', '')
                PriSort = AmzPriSrt.replace('.', '')
                APrice.append(PriSort)
            AmzPrc = [float(i) for i in APrice]

            for each in AmzNam:
                if each.find("(Renewed)") != -1:
                    Fetch = each[10:]
                    head, sep, tail = Fetch.partition(')')
                    Fetch = ("(Renewed) " + head + sep)
                    AmzNamFet.append(Fetch)
                else:
                    head, sep, tail = each.partition(')')
                    Fetch = (head + sep)
                    AmzNamFet.append(Fetch)

            Links = AmazonSoup.find_all("a", attrs={'class': 'a-link-normal a-text-normal'})
            for Link in Links:
                AmzLinks.append(Link.get('href'))
            for EachLink in AmzLinks:
                AmzLink.append(AmazonLink + EachLink)

            for Img in AmazonSoup.findAll('img'):
                AmzImgs.append(Img.get('src'))
            for i in AmzImgs:
                if i[0:36] == 'https://m.media-amazon.com/images/I/':
                    AmzImg.append(i)
                else:
                    pass





            bubbleSortsecond(AmzPrc, AmzLink, AmzNamFet)

            for AmazonLink, AmazonName, AmazonPrice in zip(AmzLink, AmzNamFet, AmzPrc):
                AmazonDetails.append(AmazonLink)
                AmazonDetails.append(AmazonName)
                AmazonDetails.append(AmazonPrice)

            return AmazonDetails

        def Flipkart():
            FlipkartName = []
            FlipkartPrice = []
            FlipkartLinks = []
            FlkLink = []
            FlipkartDetails = []

            FlipkartSeperator = '%20'
            Flipkart = Search.split(" ")
            FlipkartSrc =FlipkartSeperator.join(Flipkart)

            FlipkartLink = "https://flipkart.in"
            FlipkartSource = "https://www.flipkart.com/search?q=" + FlipkartSrc
            FlipkartRequest = requests.get(FlipkartSource, headers = headers)
            FlipkartSoup = BeautifulSoup(FlipkartRequest.content, features = "lxml")

            for i in FlipkartSoup.find_all('div', class_="_4rR01T"):
                string = i.text
                FlipkartName.append(string.strip())

            for i in FlipkartSoup.find_all('div', class_="_30jeq3 _1_WHN1"):
                string = i.text
                FlkPri = string.strip()
                FlkPriSrt = FlkPri[1:]
                PriSort = FlkPriSrt.replace(',', '')
                FlipkartPrice.append(PriSort)

            Links = FlipkartSoup.find_all("a", attrs={'class': '_1fQZEK'})
            for Link in Links:
                FlipkartLinks.append(Link.get('href'))
            for EachLink in FlipkartLinks:
                FlkLink.append(FlipkartLink + EachLink)

            bubbleSortsecond(FlipkartPrice, FlipkartName, FlkLink)

            for FlipkartLink, FlipkartName, FlipkartPrice in zip(FlkLink, FlipkartName, FlipkartPrice):
                FlipkartDetails.append(FlipkartLink)
                FlipkartDetails.append(FlipkartName)
                FlipkartDetails.append(FlipkartPrice)

            return FlipkartDetails

        def RelianceDigi():
            RelName = []
            RelPrice = []
            RPrice = []
            Links = []
            RelLink = []
            Imgs = []
            RelImg = []
            RelianceDetails = []

            RelianceSeperator = '%20'
            Reliance = Search.split(" ")
            RelianceSrc = RelianceSeperator.join(Reliance)

            RelianceLink = "https://www.reliancedigital.in"
            RelianceSource = "https://www.reliancedigital.in/search?q=" + RelianceSrc

            RelianceVal = (Reliance[0])
            Opts = Options()
            Opts.add_argument("--headless")
            Opts.binary_location = '/usr/bin/google-chrome'
            ChromeDriver = '/home/vaibhav/bin/chromedriver'
            Driver = webdriver.Chrome(options = Opts, executable_path = ChromeDriver)
            Driver.get(RelianceSource)

            RelianceSourceSoup = Driver.page_source
            RelianceSoup = BeautifulSoup(RelianceSourceSoup, features = 'lxml')
            time.sleep(1)
            Driver.close()

            for i in RelianceSoup.find_all('p', class_="sp__name"):
                string = i.text
                RelName.append(string.strip())

            for i in RelianceSoup.find_all('span', class_="sc-bdVaJa hKEXmy"):
                string = i.text
                RelPri = string.strip()
                RelPriSrt = RelPri[1:]
                PriceSort = RelPriSrt.replace(',', '')
                RPrice.append(PriceSort)
            RelPrice = [float(i) for i in RPrice]

            Link = RelianceSoup.find_all('a')
            for i in Link:
                Links.append(i.get('href'))

            for i in Links:
                if i.startswith('/' + RelianceVal):
                    RelLink.append(RelianceLink + i)
                else:
                    pass
            n = []
            Img = RelianceSoup.find_all('img')
            for i in Img:
                Imgs.append(i.get('data-srcset'))

            for i in Imgs:
                if i != None:
                    n.append(i)

            for i in n:
                if i.startswith("/medias"):
                    RelImg.append(RelianceLink + i)
                else:
                    pass



            try:
                bubbleSort(RelPrice, RelName, RelLink, RelImg)

                for RelianceImg, RelianceLink, RelianceName, ReliancePrice in zip(RelImg, RelLink, RelName, RelPrice):
                    RelianceDetails.append(RelianceImg)
                    RelianceDetails.append(RelianceLink)
                    RelianceDetails.append(RelianceName)
                    RelianceDetails.append(ReliancePrice)
            except:
                RelianceDetails = []

            return RelianceDetails

        AmazonDetails = Amazon()
        FlipkartDetails = Flipkart()
        RelianceDetails = RelianceDigi()

        return render_template('AccessoriesOutputs.html', AmazonDetails = AmazonDetails,  FlipkartDetails = FlipkartDetails, RelianceDetails = RelianceDetails)

    return render_template('Accessories.html')

@web.route('/AccessoriesOutputs')
def AccessoriesOutputs():
    if 'LoggedIn' in session:
        return render_template('AccessoriesOutputs.html')
    return render_template('AccessoriesOutputs.html')

@web.route('/Groceries')
def Groceries():
    if 'LoggedIn' in session:
        return render_template('Groceries.html')
    return render_template('Groceries.html')

@web.route('/GroceriesSearch', methods=['POST', 'GET'])
def GroceriesSearch():
    if request.method == 'POST':
        Search = request.form['Search']

        def JioMart():
            JioMartName = []
            JioMartPrice = []
            JPrice = []
            Links = []
            JMLink = []
            JioMartImg = []
            JioMartDetails = []

            JioMartSeperator = '%20'
            JioMart = Search.split(" ")
            JioMartSrc = JioMartSeperator.join(JioMart)

            JioMartLink = "https://www.jiomart.com"
            JioMartSource = "https://www.jiomart.com/catalogsearch/result?q=" + JioMartSrc

            Opts = Options()
            Opts.add_argument("--headless")
            Opts.binary_location = '/usr/bin/google-chrome'
            ChromeDriver = '/home/vaibhav/bin/chromedriver'
            Driver = webdriver.Chrome(options = Opts, executable_path = ChromeDriver)
            Driver.get(JioMartSource)

            JioMartSourceSoup = Driver.page_source
            JioMartSoup = BeautifulSoup(JioMartSourceSoup, features='lxml')
            time.sleep(1)
            Driver.close()

            for i in JioMartSoup.find_all('span', class_="clsgetname"):
                string = i.text
                JioMartName.append(string.strip())

            for i in JioMartSoup.find_all('span', attrs={'id': 'final_price'}):
                string = i.text
                JmtPri = string.strip()
                JmtPriSrt = JmtPri[1:]
                PriSort = JmtPriSrt.replace(',', '')
                JPrice.append(PriSort)
            JioMartPrice = [float(i) for i in JPrice]

            Link = JioMartSoup.find_all('a', class_="category_name")
            for i in Link:
                Links.append(i.get('href'))
            for i in Links:
                JMLink.append(JioMartLink + i)

            JMImg = JioMartSoup.find_all('img', class_="product-image-photo")
            for i in JMImg:
                JioMartImg.append(i.get('src'))

            bubbleSort(JioMartPrice, JioMartName, JioMartImg, JMLink)

            for JioMartImg, JioMartLink, JioMartName,JioMartPrice in zip(JioMartImg, JMLink, JioMartName, JioMartPrice):
                JioMartDetails.append(JioMartImg)
                JioMartDetails.append(JioMartLink)
                JioMartDetails.append(JioMartName)
                JioMartDetails.append(JioMartPrice)

            return JioMartDetails

        def Grofers():
            GName = []
            GNames = []
            GroName = []
            GroPrice = []
            GPrice = []
            Links = []
            GroLink = []
            GroImg = []
            GrofersDetails = []

            Grofershttp = "https:"
            GrofersSeperator = '+'
            Grofers = Search.split(" ")
            GrofersSrc = GrofersSeperator.join(Grofers)

            GrofersLink = "https://grofers.com"
            GrofersSource = "https://grofers.com/s/?q=" + GrofersSrc

            Opts = Options()
            Opts.add_argument("--headless")
            Opts.binary_location = '/usr/bin/google-chrome'
            ChromeDriver = '/home/vaibhav/bin/chromedriver'
            Driver = webdriver.Chrome(options=Opts, executable_path=ChromeDriver)
            Driver.get(GrofersSource)

            GrofersSourceSoup = Driver.page_source
            GrofersSoup = BeautifulSoup(GrofersSourceSoup, features='lxml')
            time.sleep(1)
            Driver.close()

            Name = GrofersSoup.find_all('div', class_="plp-product__name")
            for i in Name:
                GName.append(i.get('title'))
            Names = GrofersSoup.find_all('div', class_="plp-product__quantity")
            for i in Names:
                GNames.append(i.get('title'))
            for i, j in zip(GName, GNames):
                GroName.append(i + " | " + j)

            for i in GrofersSoup.find_all('span', class_="plp-product__price--new"):
                string = i.text
                GroPri = string.strip()
                GroPriSrt = GroPri[1:]
                PriSort = GroPriSrt.replace(',', '')
                GPrice.append(PriSort)
            GroPrice = [float(i) for i in GPrice]

            Link = GrofersSoup.find_all('a', class_="product__wrapper")
            for i in Link:
                Links.append(i.get('href'))
            for i in Links:
                GroLink.append(GrofersLink + i)

            Img = GrofersSoup.find_all('img', class_="img-loader__img img-loader__img--shown img-loader__img--plp")
            for i in Img:
                GroImg.append(Grofershttp + i.get('src'))

            bubbleSort(GroPrice, GroImg, GroName, GroLink)

            for GrofersImg, GrofersLink, GrofersName, GrofersPrice in zip(GroImg, GroLink, GroName, GroPrice):
                GrofersDetails.append(GrofersImg)
                GrofersDetails.append(GrofersLink)
                GrofersDetails.append(GrofersName)
                GrofersDetails.append(GrofersPrice)

            return GrofersDetails

        JioMartDetails = JioMart()
        GrofersDetails = Grofers()

        return render_template('GroceriesOutputs.html', JioMartDetails = JioMartDetails, GrofersDetails = GrofersDetails)

    return render_template('Groceries.html')

@web.route('/GroceriesOutputs')
def GroceriesOutputs():
    if 'LoggedIn' in session:
        return render_template('GroceriesOutputs.html')
    return render_template('GroceriesOutputs.html')

@web.route('/ProductSpecification')
def ProductSpecification():
    if 'LoggedIn' in session:
        return render_template('ProductSpecification.html')
    return render_template('ProductSpecification.html')

@web.route('/ProSpecificationSearch', methods=['POST', 'GET'])
def ProSpecificationSearch():
    if request.method == 'POST':
        Search1 = request.form['Search1']
        Search2 = request.form['Search2']

        se1 = Search1.title()
        se2 = Search2.title()

        s1 = se1.replace(' ','_')
        s2 = se2.replace(' ', '_')

        so1 = wptools.page(s1).get_parse()
        so2 = wptools.page(s2).get_parse()


        infobox1 = so1.data['infobox']
        infobox2 = so2.data['infobox']


        m1 = infobox1['memory'].replace('|',' ')
        m4 = m1.replace('&nbsp', ' ')
        mem1 = re.sub(r'[^A-Za-z0-9 .]+', '',m4)
        infobox1['memory'] = mem1

        m2 = infobox2['memory'].replace('|',' ')
        m3 = m2.replace('&nbsp', ' ')
        mem2 = re.sub(r'[^A-Za-z0-9 .:/()=-]+', '',m3)
        infobox2['memory'] = mem2

        s1 = infobox1['storage'].replace('|',' ')
        s6 = s1.replace('&nbsp', ' ')
        str1 = re.sub(r'[^A-Za-z0-9 .:/()=-]+', '',s6)
        infobox1['storage'] = str1

        s2 = infobox2['storage'].replace('|',' ')
        s5 = s2.replace('&nbsp', ' ')
        str2 = re.sub(r'[^A-Za-z0-9 .:/()=-]+', '',s5)
        infobox2['storage'] = str2

        fc1 = infobox1['front_camera'].replace('|',' ')
        f4 = fc1.replace('&nbsp', ' ')
        fcam1 = re.sub(r'[^A-Za-z0-9 .:/()=-]+', '',f4)
        infobox1['front_camera'] = fcam1

        fc2 = infobox2['front_camera'].replace('|',' ')
        f3 = fc2.replace('&nbsp', ' ')
        fcam2 = re.sub(r'[^A-Za-z0-9 .:/()=-]+', '',f3)
        infobox2['front_camera'] = fcam2

        rc1 = infobox1['rear_camera'].replace('|', ' ')
        r4 = rc1.replace('&nbsp', ' ')
        rcam1 = re.sub(r'[^A-Za-z0-9 .:/()=-]+', '', r4)
        infobox1['rear_camera'] = rcam1

        rc2 = infobox2['rear_camera'].replace('|', ' ')
        r3 = rc2.replace('&nbsp', ' ')
        rcam2 = re.sub(r'[^A-Za-z0-9 .:/()=-]+', '', r3)
        infobox2['rear_camera'] = rcam2

        b1 = infobox1['battery'].replace('|', ' ')
        b4 = b1.replace('&nbsp', ' ')
        bt1 = re.sub(r'[^A-Za-z0-9 .:/()=-]+', '', b4)
        infobox1['battery'] = bt1

        b2 = infobox2['battery'].replace('|', ' ')
        b3 = b2.replace('&nbsp',' ')
        bt2 = re.sub(r'[^A-Za-z0-9 .:/()=-]+', '', b3)
        infobox2['battery'] = bt2




        return render_template('ProSpecOutput.html', infobox1 = infobox1, infobox2 = infobox2)

    return render_template('ProductSpecification.html')

@web.route('/ProSpecOutput')
def ProSpecOutput():
    if 'LoggedIn' in session:
        return render_template('ProSpecOutput.html')
    return render_template('ProSpecOutput.html')

@web.route('/Profile')
def Profile():
    if 'LoggedIn' in session:
        return render_template('Profile.html')
    return render_template('Profile.html')

@web.route('/About')
def About():
    if 'LoggedIn' in session:
        return render_template('About.html')
    return render_template('About.html')

if __name__ == '__main__':
    web.run(debug=True)

# 9-3-21 :- Total Lines of Code = 1572 Till Date