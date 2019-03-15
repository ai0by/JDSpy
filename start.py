# -*- coding: utf-8 -*-
import ssl
import urllib,urllib2
from selenium import webdriver
from bs4 import BeautifulSoup
from config import tjurl,password,apikey,pre,dbname,dbpasswd,dbuser,cat
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
# 大商创系统模拟登陆
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

# 文件读取入库
def readFile():
    f = open("list.txt")  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    while line:
        try:
            catchData(line.strip())  # 后面跟 ',' 将忽略换行符
            line = f.readline()
        except Exception, e:
            line = f.readline()
            print "错误："+e.message+" 即将自动执行下一个商品"
            continue
    f.close()

# 图片下载
def downImg(soup):
    print "开始下载商品图片..."
    str = ""
    m = 0
    try:
        for i in soup.find_all('ul',{"class":"lh"}):
            for j in i.find_all('li'):
                # print "http://img14.360buyimg.com/n1/"+i.find('img').get('data-url').strip()
                imgUrl = "http://img14.360buyimg.com/n1/"+j.find('img').get('data-url').strip()
                imgUrl = imgUrl.replace("/jfs/","/s800x800_jfs/")
                str = str + imgUrl + ","
                print ("正在下载第%s张图片"%(m+1))
                # browser.get(imgUrl)
                # browser.save_screenshot('./imgDL/good%s.jpg'%(m+1))
                r = requests.get(imgUrl)
                with open('./imgDL/good%s.jpg'%(m+1), 'wb') as f:
                    f.write(r.content)
                m = m + 1
    except Exception,e:
        # print "错误:"+e.message
        return str
    print ("图片下载完毕,一共下载了%s张图片"%(m))
    return str

# 获取京东商品详情
def getDetile(soup):
    print "变更商品详情中..."
    str = ""
    m = 0
    for i in soup.find("div", id="J-detail-content").find_all("p"):
        for res in i.find_all("img"):
            res = res.get("data-lazyload").strip()
            if res[0:4] == "http":
                str = str + '<img src = '+res+' " alt="JDSPY" align=\"absmiddle\" /><br/>'
            else:
                str = str + '<img src = "http:' + res + ' " alt="JDSPY" align=\"absmiddle\" /><br/>'
            m = m+1
            print "正在爬取第%s张详情图片"%m
    if m == 0:
        for i in soup.find("div", id="J-detail-content").find_all("img"):
            str = str + "<img src=\"" + i.get("data-lazyload") + "\" alt = \"JDSPY\" align=\"absmiddle\" /><br />"
            m = m + 1
            print "正在爬取第%s张详情图片" % m
    if m == 0:
        try:
            print "正在解析CSS样式"
            style = soup.find("div",id = "J-detail-content").find("style").contents
            content = soup.find("div",{"class":"ssd-module-wrap"})
            style = style[0].strip()
            str = "<style>%s</style><div class=\"ssd-module-wrap\">%s</div>"%(style,content)
            # str = "<style>"+style+"</style>"+"<div class=\"ssd-module-wrap\">"+content+"</div>"
            str = str.encode("utf-8")
            # str = str.replace("u\'","").replace("\\n\'","").replace("[","")
        except:
            print "商品详情加载失败，请手动删除！"
    return str

# 获取商品信息入库
def catchData(goodsId):
    if goodsId[0:4]!="http":
        url = "https://item.jd.com/%s.html"%goodsId
    else:
        url = goodsId
        goodsId = goodsId.replace("https://item.jd.com/","").replace(".html","")
    # req = urllib2.Request("https://item.jd.com/8762779.html")
    # req = urllib2.urlopen(req)
    # req.headers = headers
    # HtmlPage = req.read()
    # HtmlPage = unicode(HtmlPage, "gbk").encode("utf8")
    #
    #  = BeautifulSoup(HtmlPage)
    # content = soup.find("div",id = "J-detail-content").contents
    # return content
    # print "请设置分类ID,例:858 ，\n分类ID获取方式：后台将鼠标放到分类名上可以在左下角看到cat_id=858 后面的数字就是id号"
    # catId = raw_input()
    catId = cat
    print "商品地址设置成功，%s，3秒后开始抓取页面"%url
    # browser.implicitly_wait(300)
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
    try:
        price = soup.find('span', {'class': priceid}).contents[0]
    except Exception,e:
        price = soup.find('span', {'class': "price J-presale-price"}).contents[0]
    hoverimg = "http://"+soup.find('img',id = "spec-img").get('src').replace("450x450","800x800")
    content = {
        'detile':getDetile(soup),
        'title' :soup.find('img', id = "spec-img").get('alt'),
        'price': price,
        'hoverimg':hoverimg,
        'cat':catId,
        'key': apikey,
        'tjurl':tjurl,
        'pre' : pre,
        'dbname':dbname,
        'dbuser':dbuser,
        'dbpasswd':dbpasswd,
        'imglist':downImg(soup),
        'weight':soup.find('div',id = "summary-weight").find('div',{'class':'dd'})
        # 'imglist':soup.find('ul',{"class":"lh"}).find('li').find('img')['data-url']
    }
    # print "元素获取完毕，详细数据如下：\n  "
    # for key, value in content.items():
    #     print "%s : %s"%(key,value)
    # print tags
    # print content
    doPost(content)

# 大商创入库对接函数
def doPost(dd,fa=[0],tr=[0]):
    url = tjurl + "/post.php"
    response = requests.post(url, dd)
    print response.text
    if response.status_code == 200 and response.text == "success":
        t = tr[0] + 1
        tr[0] = t
        print "成功上传%s个商品！"%t
    else:
        f = fa[0] + 1
        fa[0] = f
        print "失败%s个商品！"%f

# 判定函数
def storage():
    print "请输入爬虫方式 1.从list.txt文件读取 2.手动输入ID"
    method = raw_input()
    if method == "2":
        print "请设置商品ID,例:8762779"  # https://item.jd.com/8762779.html
        goodsId = raw_input()
        catchData(goodsId)
    else:
        print "从文件中读取..."
        readFile()

# 采集京东商品url
def spy():
    print "请输入需要采集的关键词"
    keywords = raw_input()
    print "当前采集关键词：%s  开始采集"%keywords
    print "请输入需要采集的页数，每页56个商品"
    page = raw_input()
    page = int(page)*2
    f = open("list.txt","w")  # 返回一个文件对象
    for i in range(1,page,2):
        pages = int((i+1)/2)
        print "正在采集第%s页商品信息"%pages
        keyword = urllib.quote(keywords)
        url = "https://search.jd.com/Search?keyword=%s&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&stock=1&page=%s&s=56&click=0" % (
        keyword, i)
        print url
        req = urllib2.Request(url)
        req = urllib2.urlopen(req)
        HtmlPage = req.read()
        soup = BeautifulSoup(HtmlPage, 'html.parser')
        item = soup.find("div",id = "J_goodsList").find_all("li",{"class":"gl-item"})
        for i in item:
            items = i.find_all("a")
            reurl = ""
            for j in items:
                goodsUrl = j.get("href")
                if goodsUrl[0:6] != "//item":
                    continue
                if goodsUrl[-4:-1]!="html":
                    goodsUrl = "https:"+goodsUrl.replace("#comment","")
                    if goodsUrl == reurl:
                        continue
                f.writelines(goodsUrl+"\n")
                reurl = goodsUrl
    f.close()

if __name__ == "__main__":
    ssl._create_default_https_context = ssl._create_unverified_context
    print "JDSPY开始执行任务,正在绑定浏览器"
    browser = webdriver.PhantomJS('d:/phantomjs-2.1.1-windows/bin/phantomjs.exe')
    print "1.采集 2.入库 3.采集+入库  默认3"
    print "Tips:当有采集任务时，会覆盖当前 list.txt 的内容"
    do = raw_input()
    if do == "2":
        storage()
    elif do == "1":
        spy()
    else:
        spy()
        storage()
    # login()