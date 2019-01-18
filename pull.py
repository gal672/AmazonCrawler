# -*- coding:utf-8 -*-
import requests
import re
import os
from bs4 import BeautifulSoup
from xlrd import open_workbook
import dictionary
import urllib.request
import time
import sys
import importlib
import math
import xlwt
from collections import Counter
from bs4.element import Comment
importlib.reload(sys)

URL_CONST = "https://www.amazon.com"
pageList = []
proudcatLink = set()
final_proudcatLink = set()
links = []
user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36")
headers = {'User-Agent': user_agent}

def downWeb():
    try:
        realUrl = pageList.pop(0)
        time.sleep(10)
        thepage = urllib.request.urlopen(realUrl)
        if (thepage.code != 200):
            thepage = requests.get(realUrl, headers={'User-Agent': 'MyAgent'})
            soup = BeautifulSoup(thepage.text, "html.parser")
        else:
            soup = BeautifulSoup(thepage, "html.parser")
        links2 = soup.find_all("a")
        for link in links2:
            res = link.find('h2', class_='s-inline')
            if type(res) != type(None):
                proudcatLink.add(link)
                print(link.text+' '+link.get('href'))
        nextPage = soup.find('a',{'class': 'pagnNext'})
        if (type(nextPage) != type(None)):
            fullPatch = URL_CONST+""+nextPage.get('href')
            print(fullPatch)
            pageList.append(fullPatch)
    except requests.exceptions.RequestException as e:
        print_page("test")
        print (e)

def saveToExcelSmartTv(comment):
    title,price,rate,reviews,details,urlString= (comment["title"],
            comment["price"],comment["rate"],comment["reviews"],
            comment["details"],comment["urlString"])
    import xlwt
    efile = xlwt.Workbook()
    table = efile.add_sheet('Sheet1')
    table.write(0,0,'title')
    table.write(0,1,'price')
    table.write(0,2,'rate')
    table.write(0,3,'review')
    table.write(0,4,'description')
    table.write(0,5,'url')
    for num,each in enumerate(rate):
        index = num +1
        try:
            table.write(index,0,title[num])
            table.write(index,1,price[num])
            table.write(index,2,rate[num])
            table.write(index,3,reviews[num])
            table.write(index,4,details[num])
            table.write(index,5,urlString[num])
        except:
            print ("len error or ascii error")

    efile.save('SmartTv.xls')
    print ("Save data successful...")

def saveToExcelSmartTvReview(comment):
    title,price,rate,reviews,details,urlString= (comment["title"],
            comment["price"],comment["rate"],comment["reviews"],
            comment["details"],comment["urlString"])
    efile = xlwt.Workbook()
    table = efile.add_sheet('Sheet1')
    table.write(0,0,'title')
    table.write(0,1,'price')
    table.write(0,2,'rate')
    table.write(0,3,'review')
    table.write(0,4,'description')
    table.write(0,5,'url')
    for num,each in enumerate(rate):
        index = num +1
        try:
            table.write(index,0,title[num])
            table.write(index,1,price[num])
            table.write(index,2,rate[num])
            table.write(index,3,reviews[num])
            table.write(index,4,details[num])
            table.write(index,5,urlString[num])
        except:
            print ("len error or ascii error")

    efile.save('SmartTvReview.xls')
    print ("Save data successful...")

def saveToExcelSmartTvRate(comment):
    title,price,rate,reviews,details,urlString= (comment["title"],
            comment["price"],comment["rate"],comment["reviews"],
            comment["details"],comment["urlString"])
    efile = xlwt.Workbook()
    table = efile.add_sheet('Sheet1')
    table.write(0,0,'title')
    table.write(0,1,'price')
    table.write(0,2,'rate')
    table.write(0,3,'review')
    table.write(0,4,'description')
    table.write(0,5,'url')
    for num,each in enumerate(rate):
        index = num +1
        try:
            table.write(index,0,title[num])
            table.write(index,1,price[num])
            table.write(index,2,rate[num])
            table.write(index,3,reviews[num])
            table.write(index,4,details[num])
            table.write(index,5,urlString[num])
        except:
            print ("len error or ascii error")

    efile.save('SmartTvRate.xls')
    print ("Save data successful...")

def print_page(fileName):
    f = open(fileName+'.txt','w',encoding='utf-8')
    for proudcat in final_proudcatLink:
        f.write(proudcat.get('href')+" "+proudcat.text)
        f.write("\n")
    f.close()

def check_page ():
    for proudcat in proudcatLink:
        if (dictionary.check_link(proudcat.text) == True):
            final_proudcatLink.add(proudcat)

def proudcat_Details_SmartTv():
    title = []
    rate = []
    price = []
    urlString = []
    reviews = []
    details = []
    file = open("SmartTv.txt", "r")

    index = 0

    for line in file:
        print (index)
        index = index +1
        values = line.split(" ",1)
        time.sleep(10)
        thepage = requests.get(values[0], headers={'User-Agent': 'MyAgent'})
        soup = BeautifulSoup(thepage.text, "html.parser")
        #soup = BeautifulSoup(thepage.text, "lxml")
        #thepage = urllib.request.urlopen(values[0])
        #soup = BeautifulSoup(thepage, "html.parser")

        urlString.append(values[0])
        title.append(values[1])

        comment = soup.find(id = "acrPopover")
        if (type(comment) != type(None)):
            info = comment.text.strip(' \n\t')
            rate.append(info)
        else:
            rate.append("none")

        comment = soup.find(id = "acrCustomerReviewText")
        if (type(comment) != type(None)):
            info = comment.text.strip(' \n\t')
            reviews.append(info)
        else:
            reviews.append("0")




        comment = soup.find(id = "price_inside_buybox")
        if (type(comment) != type(None)):
            info = comment.text.strip(' \n\t')
            price.append(info)
        else:
            comment = soup.find(id="comparison_price_row")
            if (type(comment) != type(None)):
                info = comment.find("span", class_="a-price")
                info2 = info.text
                price.append(info2)
            else:
                comment = soup.find(id="olp-upd-new-used")
                if (type(comment) != type(None)):
                    info2 = comment.text
                    price.append(info2)
                else:
                    comment = soup.find(id="olp-upd-new")
                    if (type(comment) != type(None)):
                        info2 = comment.text
                        price.append(info2)
                    else:
                        comment = soup.find(id="buyNew_noncbb")
                        if (type(comment) != type(None)):
                            info2 = comment.text
                            price.append(info2)
                        else:
                            comment = soup.find(id="priceblock_ourprice")
                            if (type(comment) != type(None)):
                                info2 = comment.text
                                price.append(info2)
                            else:
                                comment = soup.find(class_="a-section a-spacing-small a-spacing-top-small")
                                if (type(comment) != type(None)):
                                    info2 = comment.text
                                    price.append(info2)
                                else:
                                    comment = soup.find(id="olp-upd-cr")
                                    if (type(comment) != type(None)):
                                        info2 = comment.text
                                        price.append(info2)
                                    else:
                                        comment = soup.find(id="olp_feature_div")
                                        if (type(comment) != type(None)):
                                            info = soup.find("span")
                                            info2 = info.text
                                            price.append(info2)
                                        else:
                                            price.append("none")


        comment = soup.find( id = "feature-bullets")
        if (type(comment) != type(None)):
            info = comment.text.strip(' \n\t')
            info =  re.sub('\s+', ' ', info)
            details.append(info)
        else:
            details.append("none")
    commentDict =  dict(title=title,price=price,rate=rate,
                        reviews=reviews,details=details,urlString=urlString)
    file.close()
    return commentDict

def reviewFilter():
    title = []
    rate = []
    price = []
    urlString = []
    reviews = []
    details = []
    titleRow =""
    rateRow = ""
    priceRow = ""
    urlStringRow = ""
    reviewsRow = ""
    detailsRow = ""

    wb = open_workbook('SmartTv.xls')
    for sheet in wb.sheets():
        number_of_rows = sheet.nrows
        for row in range(1, number_of_rows):
            titleRow = (sheet.cell(row, 0).value)
            priceRow = (sheet.cell(row, 1).value)
            rateRow = (sheet.cell(row, 2).value)
            reviewsRow = (sheet.cell(row, 3).value)
            detailsRow = (sheet.cell(row, 4).value)
            urlStringRow = (sheet.cell(row, 5).value)
            if (reviewsRow == "0"):
                continue
            else:
                title.append(titleRow)
                rate.append(rateRow)
                price.append(priceRow)
                urlString.append(urlStringRow)
                reviews.append(reviewsRow)
                details.append(detailsRow)
        commentDict = dict(title=title, price=price, rate=rate,
                           reviews=reviews, details=details, urlString=urlString)
        return commentDict

def rateFilter():
    title = []
    rate = []
    price = []
    urlString = []
    reviews = []
    details = []
    titleRow =""
    rateRow = ""
    priceRow = ""
    urlStringRow = ""
    reviewsRow = ""
    detailsRow = ""

    wb = open_workbook('SmartTv.xls')
    for sheet in wb.sheets():
        number_of_rows = sheet.nrows
        for row in range(1, number_of_rows):
            titleRow = (sheet.cell(row, 0).value)
            priceRow = (sheet.cell(row, 1).value)
            rateRow = (sheet.cell(row, 2).value)
            reviewsRow = (sheet.cell(row, 3).value)
            detailsRow = (sheet.cell(row, 4).value)
            urlStringRow = (sheet.cell(row, 5).value)
            if (rateRow == "none"):
                continue
            else:
                rate_value = (float)(rateRow.split(" ")[0])
                if (rate_value > 3):
                    title.append(titleRow)
                    rate.append(rateRow)
                    price.append(priceRow)
                    urlString.append(urlStringRow)
                    reviews.append(reviewsRow)
                    details.append(detailsRow)
        commentDict = dict(title=title, price=price, rate=rate,
                           reviews=reviews, details=details, urlString=urlString)
        return commentDict

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def findMostCommonWord():
    file = open("SmartTv.txt", "r")
    file2 = open("SmartTvMostCommon.txt", "w")
    index = 0
    CommonWord = []
    for line in file:
        print(index)
        index = index + 1
        values = line.split(" ", 1)
        time.sleep(10)
        thepage = requests.get(values[0], headers={'User-Agent': 'MyAgent'})
        soup = BeautifulSoup(thepage.text, "html.parser")
        # soup = BeautifulSoup(thepage.text, "lxml")
        # thepage = urllib.request.urlopen(values[0])
        # soup = BeautifulSoup(thepage, "html.parser")
        texts = soup.findAll(text=True)
        visible_texts = filter(tag_visible, texts)
        visible_texts_string = " ".join(t.strip() for t in visible_texts)
        lst = re.findall(r'\b\w+', visible_texts_string)
        lst = [x.lower() for x in lst]
        counter = Counter(lst)
        occs = [(word, count) for word, count in counter.items() if count > 3]
        occs.sort(key=lambda x: x[1])
        occs = dictionary.filterStopWord(occs)
        dictionary.appendWord(occs)

def Df():
    file = open("SmartTv.txt", "r")
    efile = xlwt.Workbook()
    table = efile.add_sheet('Sheet1')
    table.write(0, 0, 'title')
    table.write(0, 1, 'smart')
    table.write(0, 2, 'tv')
    table.write(0, 3, '55')
    table.write(0, 4, 'inch')
    table.write(0, 5, 'Out')
    table.write(0, 6, '4k')
    table.write(0, 7, 'Starts')
    table.write(0, 8, 'Led')
    table.write(0, 9, 'Product')
    table.write(0, 10, '2018')
    table.write(0, 11, 'Hd')
    table.write(0, 12, 'Model')
    table.write(0, 13, 'Electronics')
    table.write(0, 14, 'Ultra')
    table.write(0, 15, '65')
    D = 0
    query_word = ["smart","tv","55","inch","out","4k","starts","led","product","2018","hd","model","electronics","ultra","65"]
    df = dict()
    try:
        for line in file:
            print(D)
            D = D + 1
            values = line.split(" ", 1)
            time.sleep(10)
            thepage = requests.get(values[0], headers={'User-Agent': 'MyAgent'})
            soup = BeautifulSoup(thepage.text, "html.parser")
            texts = soup.findAll(text=True)
            visible_texts = filter(tag_visible, texts)
            visible_texts_string = " ".join(t.strip() for t in visible_texts)
            lst = re.findall(r'\b\w+', visible_texts_string)
            lst = [x.lower() for x in lst]
            counter = Counter(lst)
            tf = dict()
            df = calculateTf(counter,query_word,df,tf)
            table.write(D,0,values[1])
            table.write(D,1,tf.get("smart",0))
            table.write(D,2,tf.get("tv",0))
            table.write(D,3,tf.get("55",0))
            table.write(D,4,tf.get("inch",0))
            table.write(D, 5, tf.get('out',0))
            table.write(D, 6, tf.get('4k',0))
            table.write(D, 7, tf.get('starts',0))
            table.write(D, 8, tf.get('led',0))
            table.write(D, 9, tf.get('product',0))
            table.write(D, 10, tf.get('2018',0))
            table.write(D, 11, tf.get('hd',0))
            table.write(D, 12, tf.get('model',0))
            table.write(D, 13, tf.get('electronics',0))
            table.write(D, 14, tf.get('ultra',0))
            table.write(D, 15, tf.get('65',0))
            print(df)
        efile.save('SmartTvDf.xls')
        print("Save data successful...")
    except requests.exceptions.RequestException as e:
        efile.save('SmartTvDf.xls')
        print(e)

def Idf():
    wb = open_workbook('SmartTvDf.xls')
    smartTf = 0
    tvTf = 0
    fivefiveTf = 0
    inchTf = 0
    outTf = 0
    fourKTf = 0
    startsTf = 0
    ledTf = 0
    productTf = 0
    A2018Tf = 0
    hdTf = 0
    modelTf = 0
    electronicsTf = 0
    ultraTf = 0
    B65Tf = 0

    for sheet in wb.sheets():
        number_of_rows = sheet.nrows
        D =  number_of_rows -1
        for row in range(1, number_of_rows):
            title = (sheet.cell(row, 0).value)
            smart = (int)(sheet.cell(row, 1).value)
            tv = (int)(sheet.cell(row, 2).value)
            fivefive = (int)(sheet.cell(row, 3).value)
            inch = (int)(sheet.cell(row, 4).value)
            out = (int)(sheet.cell(row, 5).value)
            fourK = (int)(sheet.cell(row, 6).value)
            starts = (int)(sheet.cell(row, 7).value)
            led = (int)(sheet.cell(row, 8).value)
            product = (int)(sheet.cell(row, 9).value)
            A2018 = (int)(sheet.cell(row, 10).value)
            hd = (int)(sheet.cell(row, 11).value)
            model = (int)(sheet.cell(row, 12).value)
            electronics = (int)(sheet.cell(row, 13).value)
            ultra = (int)(sheet.cell(row, 14).value)
            B65 = (int)(sheet.cell(row, 15).value)
            if ( smart > 0):
                smartTf = smartTf + 1
            if ( tv > 0):
                tvTf = tvTf + 1
            if ( fivefive > 0):
                fivefiveTf = fivefiveTf + 1
            if ( inch > 0):
                inchTf = inchTf + 1
            if (out> 0):
                outTf = outTf + 1
            if (fourK > 0):
                fourKTf = fourKTf + 1
            if (starts > 0):
                startsTf = startsTf + 1
            if (led > 0):
                ledTf = ledTf + 1
            if (B65> 0):
                B65Tf =B65Tf + 1
            if (ultra> 0):
                ultraTf =ultraTf + 1
            if ( product > 0):
                productTf = productTf + 1
            if (A2018> 0):
                A2018Tf = A2018Tf + 1
            if (hd > 0):
                hdTf = hdTf + 1
            if (model > 0):
                modelTf = modelTf + 1
            if (electronics> 0):
                electronicsTf = electronicsTf + 1
        D_divide_df = dict()
        idf = dict ()
        D_divide_df["smart"] = D_divide_df.get("smart", 0) + (D / smartTf)
        D_divide_df["tv"] = D_divide_df.get("tv", 0) + (D / tvTf)
        D_divide_df["55"] = D_divide_df.get("55", 0) + (D / fivefiveTf)
        D_divide_df["inch"] = D_divide_df.get("inch", 0) + (D / inchTf)
        D_divide_df["out"] = D_divide_df.get("out", 0) + (D / outTf)
        D_divide_df["4k"] = D_divide_df.get("4k", 0) + (D / fourKTf)
        D_divide_df["starts"] = D_divide_df.get("starts", 0) + (D / startsTf)
        D_divide_df["led"] = D_divide_df.get("led", 0) + (D / ledTf)
        D_divide_df["65"] = D_divide_df.get("65", 0) + (D / B65Tf)
        D_divide_df["ultra"] = D_divide_df.get("ultra", 0) + (D / ultraTf)
        D_divide_df["product"] = D_divide_df.get("product", 0) + (D / productTf)
        D_divide_df["A2018"] = D_divide_df.get("A2018", 0) + (D / A2018Tf)
        D_divide_df["hd"] = D_divide_df.get("hd", 0) + (D / hdTf)
        D_divide_df["model"] = D_divide_df.get("model", 0) + (D / modelTf)
        D_divide_df["electronics"] = D_divide_df.get("electronics", 0) + (D / electronicsTf)
        for word in D_divide_df:
            idf_value = math.log(D_divide_df.get(word,0),10)
            idf[word] = idf.get(word, 0) + idf_value
        print("smart ="+str(smartTf))
        print("tv =" +str(tvTf))
        print("55 =" +str(fivefiveTf))
        print("inch =" +str(inchTf))
        print("out =" +str(outTf))
        print("4k =" +str(fourKTf))
        print("starts =" +str(startsTf))
        print("led =" +str(ledTf))
        print("65 =" +str(B65Tf))
        print("ultra =" +str(ultraTf))
        print("product ="  +str(productTf))
        print("A2018 =" +str(A2018Tf))
        print("hd =" +str(hdTf))
        print("model =" +str(modelTf))
        print("electronics =" +str(electronicsTf))
        print(D)
        print(D_divide_df)
        print(idf)
        return idf

def tfIdf(idf_value):
    title = ""
    smart = 0
    tv = 0
    fivefive = 0
    inch = 0
    import xlwt
    efile = xlwt.Workbook()
    table = efile.add_sheet('Sheet1')
    table.write(0, 0, 'title')
    table.write(0, 1, 'smart')
    table.write(0, 2, 'tv')
    table.write(0, 3, '55')
    table.write(0, 4, 'inch')
    table.write(0, 5, 'Out')
    table.write(0, 6, '4k')
    table.write(0, 7, 'Starts')
    table.write(0, 8, 'Led')
    table.write(0, 9, 'Product')
    table.write(0, 10, '2018')
    table.write(0, 11, 'Hd')
    table.write(0, 12, 'Model')
    table.write(0, 13, 'Electronics')
    table.write(0, 14, 'Ultra')
    table.write(0, 15, '65')
    wb = open_workbook('SmartTvDf.xls')
    for sheet in wb.sheets():
        number_of_rows = sheet.nrows
        for row in range(1, number_of_rows):
            title = (sheet.cell(row, 0).value)
            smart = (int)(sheet.cell(row, 1).value)
            tv = (int)(sheet.cell(row, 2).value)
            fivefive = (int)(sheet.cell(row, 3).value)
            inch = (int)(sheet.cell(row, 4).value)
            out = (int)(sheet.cell(row, 5).value)
            fourK = (int)(sheet.cell(row, 6).value)
            starts = (int)(sheet.cell(row, 7).value)
            led = (int)(sheet.cell(row, 8).value)
            product = (int)(sheet.cell(row, 9).value)
            A2018 = (int)(sheet.cell(row, 10).value)
            hd = (int)(sheet.cell(row, 11).value)
            model = (int)(sheet.cell(row, 12).value)
            electronics = (int)(sheet.cell(row, 13).value)
            ultra = (int)(sheet.cell(row, 14).value)
            B65 = (int)(sheet.cell(row, 15).value)
            smartIdfTf = smart * idf_value.get("smart",0)
            tvIdfTf = tv * idf_value.get("tv", 0)
            fivefiveIdfTf = fivefive * idf_value.get("55", 0)
            inchIdfTf = inch * idf_value.get("inch", 0)
            outTf = out * idf_value.get("out",0)
            fourKTf = fourK * idf_value.get("4k",0)
            startsTf = starts * idf_value.get("starts",0)
            ledTf = led * idf_value.get("led",0)
            productTf = product * idf_value.get("product",0)
            A2018Tf = A2018 * idf_value.get("2018",0)
            hdTf = hd * idf_value.get("hd",0)
            modelTf = model * idf_value.get("model",0)
            electronicsTf = electronics * idf_value.get("electronics",0)
            ultraTf = ultra * idf_value.get("ultra",0)
            B65Tf = B65 * idf_value.get("65",0)
            table.write(row,0,title)
            table.write(row,1,smartIdfTf)
            table.write(row,2,tvIdfTf)
            table.write(row,3,fivefiveIdfTf)
            table.write(row,4,inchIdfTf)
            table.write(row, 5, outTf)
            table.write(row, 6, fourKTf)
            table.write(row, 7, startsTf)
            table.write(row, 8, ledTf)
            table.write(row, 9, productTf)
            table.write(row, 10, A2018Tf)
            table.write(row, 11, hdTf)
            table.write(row, 12, modelTf)
            table.write(row, 13, electronicsTf)
            table.write(row, 14, ultraTf)
            table.write(row, 15, B65Tf)
        efile.save('SmartTvTfIdf.xls')
        print("Save data successful...")

def calculateTf(counter,query_word,df,tf):
    find_word_list = []
    for word,count in counter.items():
        if (word in query_word ):
            find_word_list.append(word)
            df[word] = df.get(word, 0) + 1
            tf[word] = tf.get(word,0) + count
            print(word+" "+str(count))
    for word in query_word:
        if (word not in find_word_list):
            print(word+" 0")
    return df


if __name__ == '__main__':
    ans = input('Enter your query: \n 1.smart tv between 55-65 inch \n 2.smart tv between 55-65 inch with review  \n 3.smart tv between 55-65 inch over rate 3 \n'
                ' 4.Find Most Common Words\n 5.calculate tf-idf \n')
    if (ans == '1'):
        if (os.path.isfile('./SmartTv.txt') == False):
            SmartTv ="https://www.amazon.com/s?keyword=smart+tv+55+inch"
            pageList.append(SmartTv)
            while pageList :
                downWeb()
            SmartTv = "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=smart+tv+60+inch&rh=i%3Aaps%2Ck%3Asmart+tv+60+inch"
            pageList.append(SmartTv)
            while pageList :
                downWeb()
            SmartTv ="https://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=smart+tv+65+inch&rh=i%3Aaps%2Ck%3Asmart+tv+65+inch"
            pageList.append(SmartTv)
            while pageList :
                downWeb()
            dictionary.init()
            check_page()
            print_page("SmartTv")
        comments = proudcat_Details_SmartTv()
        saveToExcelSmartTv(comments)
    elif (ans == '2'):
        comments = reviewFilter()
        saveToExcelSmartTvReview(comments)
    elif (ans == '3'):
        comments = rateFilter()
        saveToExcelSmartTvRate(comments)
    elif (ans == '4'):
        findMostCommonWord()
    elif (ans == '5'):
        #Df()
        idf_value =  Idf()
        tfIdf(idf_value)
    else:
        print("error")