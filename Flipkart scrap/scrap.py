from flask import Flask,render_template,request
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)


#header for flipkart
headers_flip = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}



options = Options()
options.add_argument('--headless')
options.add_argument('--profile-directory=Default') 
driver = webdriver.Chrome(options=options)



#to get flipkart product name for technologies
def flip_prize(product,Flag):
    url='https://www.flipkart.com/search?q=' + product + '&otracker=AS_Query_HistoryAutoSuggest_2_0&otracker1=AS_Query_HistoryAutoSuggest_2_0&marketplace=FLIPKART&as-show=on&as=off&as-pos=2&as-type=HISTORY'
    driver.get(url)
    html = driver.page_source
    page = BeautifulSoup(html)
    main_box= page.find_all('div',{"class":"_3O0U0u"})
    box=main_box[0]
    temp=[]
    try:
        if Flag==False:
            for box in main_box:
                s="https://www.flipkart.com"
                link=box.find("a",{"class":"_31qSD5"},href=True)
                l=s+link['href']
                #print(l)
                val=box.find("div",{"class":"_3wU53n"}).text.strip()
                product_img = box.find('img',{'class':'_1Nyybr'}).get('src')
                #print(val)
                if product.lower() in val.lower():
                    price=box.find("div",{"class":"_1vC4OE _2rQ-NK"}).text.strip()
                    temp.append([l,product_img,val,price])
                    #print(temp)
        else:
            for box in main_box:
                s="https://www.flipkart.com"
                link=box.find("a",{"class":"_31qSD5"},href=True)
                #print(link['href'])
                l=s+link['href']
                title=box.find("div",{"class":"_3wU53n"}).text.strip()
                price=box.find("div",{"class":"_1vC4OE _2rQ-NK"}).text.strip()
                product_img = box.find('img',{'class':'_1Nyybr'}).get('src')
                temp.append([l,product_img,title,price])
                #print(temp)
    except:
        i=1
    #print(temp)
    return temp



#to get flipkart product name for others
def flip_app_price(product):
    url='https://www.flipkart.com/search?q=' + product + '&otracker=AS_Query_HistoryAutoSuggest_2_0&otracker1=AS_Query_HistoryAutoSuggest_2_0&marketplace=FLIPKART&as-show=on&as=off&as-pos=2&as-type=HISTORY'
    driver.get(url)
    html = driver.page_source
    page = BeautifulSoup(html)
    main_box= page.find_all('div',{"class":"IIdQZO _1SSAGr"})
    box=main_box[0]
    temp=[]
    try:
        for box in main_box:
            s="https://www.flipkart.com"
            link=box.find("a",{"class":"_3dqZjq"},href=True)
            l=s+link['href']
            title= box.find("a",{"class":"_2mylT6"}).text.strip()
            price= box.find("div",{"class":"_1vC4OE"}).text.strip()
            product_img = box.find('img',{'class':'_3togXc'}).get('src')
            temp.append([l,product_img,title,price])
    except:
        i=1
    return temp



#main function
@app.route('/')
def main():
    return render_template('index.html')


# main template for having product name 
@app.route('/getValue', methods=['POST'])
def getValue():
    words=["under","below","above","new","phones","mobiles","laptops"]
    product_name= request.form['proName']
    choice=request.form['choice']
    #print(choice)
    
    if choice=="tech":
        Flag=False
        for i in range(len(words)):
            if words[i] in product_name:
                Flag = True
                break
        
        flip_list=flip_prize(product_name,Flag)
        amaz_list=amaz_price(product_name,Flag)
        
        return render_template('pass.html',p=product_name, li=flip_list, li_amaz=amaz_list)
    
    else:
        flip_list=flip_app_price(product_name)
        amaz_list=amaz_app_price(product_name)
        
        return render_template('passother.html',p=product_name, li=flip_list, li_amaz=amaz_list)
        

app.run() 