# -*- coding: utf-8 -*-
import ssl
from selenium import webdriver
from bs4 import BeautifulSoup
from config import tjurl,password,apikey,pre
import requests

# c = cookielib.LWPCookieJar()
# # 生成一个存储cookie的对象
# cookie = urllib2.HTTPCookieProcessor(c)
# opener = urllib2.build_opener(cookie)
# # 把这个存储对象绑定到opener中
# urllib2.install_opener(opener)
#
# headers = {
#     "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
# }
ssl._create_default_https_context = ssl._create_unverified_context
print "正在绑定浏览器"
browser = webdriver.PhantomJS('d:/phantomjs-2.1.1-windows/bin/phantomjs.exe')
print "绑定完毕，开始执行任务"

def login():
    print "正在尝试登陆:"+tjurl
    browser.get(tjurl+"/admin/privilege.php?act=login")
    username = browser.find_element_by_name('username')
    username.send_keys("admin")
    username = browser.find_element_by_name('password')
    username.send_keys(password)
    login_button = browser.find_element_by_name('submit')
    login_button.submit()
    data = browser.page_source
    soup = BeautifulSoup(data,'html.parser')
    try:
        if(soup.find("form", id="fileForm").contents):
            print "登陆成功"
    except:
        print "登陆失败，请检查用户名密码"
    return

def downImg(soup):
    print "开始下载商品图片..."
    m = 0
    for i in soup.find('ul',{"class":"lh"}).find_all('li'):
        # print "http://img14.360buyimg.com/n1/"+i.find('img').get('data-url').strip()
        imgUrl = "http://img14.360buyimg.com/n1/"+i.find('img').get('data-url').strip()
        print ("正在下载第%s张图片"%(m+1))
        # browser.get(imgUrl)
        # browser.save_screenshot('./imgDL/good%s.jpg'%(m+1))
        r = requests.get(imgUrl)
        with open('./imgDL/good%s.jpg'%(m+1), 'wb') as f:
            f.write(r.content)
        m = m + 1
    print ("图片下载完毕,一共下载了%s张图片"%(m))
    return m

def catchData():
    # req = urllib2.Request("https://item.jd.com/8762779.html")
    # req = urllib2.urlopen(req)
    # req.headers = headers
    # HtmlPage = req.read()
    # HtmlPage = unicode(HtmlPage, "gbk").encode("utf8")
    #
    #  = BeautifulSoup(HtmlPage)
    # content = soup.find("div",id = "J-detail-content").contents
    # return content
    print "请设置商品ID,例:8762779"  #  https://item.jd.com/8762779.html
    goodsId = raw_input()
    print "请设置分类ID,例:858 ，\n分类ID获取方式：后台将鼠标放到分类名上可以在左下角看到cat_id=858 后面的数字就是id号"
    catId = raw_input()
    url = "https://item.jd.com/"+goodsId+".html"
    print "商品地址设置成功，3秒后开始抓取页面"
    browser.implicitly_wait(300)
    print "开始抓取页面"
    browser.get(url)
    # data = requests.get(url).content
    print "获取页内元素"
    data = browser.page_source
    print "页面抓取完毕，已获取页内元素"
    data = data.encode("utf-8")
    # print data
    # print type(data) # str
    priceid = "J-p-"+goodsId
    soup = BeautifulSoup(data,'html.parser')
    downImg(soup)
    content = {
        'detile':soup.find("div", id="J-detail-content").contents,
        'title' :soup.find('img', id = "spec-img").get('alt'),
        'price':soup.find('span',{'class': priceid}).contents[0],
        'hoverimg':"http://"+soup.find('img',id = "spec-img").get('src'),
        'cat':catId,
        'key': apikey,
        'tjurl':tjurl,
        'pre' : pre


        # 'imglist':soup.find('ul',{"class":"lh"}).find('li').find('img')['data-url']
    }
    print "元素获取完毕，详细数据如下：\n  "
    for key, value in content.items():
        print "%s : %s"%(key,value)
    # print tags
    # print content
    return content

if __name__ == "__main__":
    catchData()
    # login()