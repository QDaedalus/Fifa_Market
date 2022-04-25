from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
import smtplib
import datetime
url = "https://www.futwiz.com/en/fifa22/player/gabriel-jesus/17894"
hdr = {'User-Agent': 'Mozilla/5.0'}


def read_txt(file_path):
    with open(file_path,"r") as f:
        urls = f.read().splitlines()
    return urls


def connect_to_web(url, hdr):
    req = urllib.request.Request(url,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page)
    return soup

def parse_data(soup):
    data={}
    liste=[]
    find_name = soup.find_all("div", attrs={"style": "display:block;"})
    find_price = soup.find_all("div", attrs={"class": "playerprofile-price text-center"})
    find_version = soup.find("div", attrs={"style": "display:block;font-size:14px;"})
    price = find_price[0].string
    price = price.strip("\n")
    name = find_name[0].string
    version = find_version.text
    version = version.split('|')[0].split("22")[1]
    data[name+" "+str(version)]=price
    return data
def mail_sender(subject,mail_body):
    gmail_user = 'bucanalbayrak@gmail.com'
    gmail_password = 'zayusxenldawrroq'

    sent_from = 'bucanalbayrak@gmail.com'
    to = ['brkcanalbayrak@gmail.com']


    message = 'Subject: {}\n\n{}'.format(subject, mail_body)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, message)
        server.close()

        print ('Email sent!')
    except:
        print ('Something went wrong. Mail could not be sent.')
def list_to_mail_body(mail_lines):
    mail_body=""
    mail_body = '\n'.join([str(elem) for elem in mail_lines])
    return mail_body
# parse_data(connect_to_web(url,hdr))
urls = read_txt("C:\\Users\\locix\\Desktop\\Library\\Projects\\Fifa_Market\\players_link.txt")
mail_lines = []
today = datetime.datetime.now()
run_date = today.strftime("%m_%d_%Y_%H_%M")
run_date
subject = str(run_date) + "FIFA 22 MARKET REPORT"
for url in urls:
    mail_lines.append(parse_data(connect_to_web(url,hdr)))
    print(parse_data(connect_to_web(url,hdr)))
body = list_to_mail_body(mail_lines)
mail_sender(subject, body)
