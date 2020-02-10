# # -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import time
import sys
import io
import os
import json

def mkdir(path):
    # 引入模块
    import os
 
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
 
    # 判断结果
    if not isExists:
        os.makedirs(path) 
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False

def parse_html(html):
    # soup = BeautifulSoup(html,from_encoding="utf-8",features="lxml")
    soup = BeautifulSoup(html, 'html.parser')
    namelist = soup.find_all(name="div", attrs={"class":"pi"})
    # replylist = soup.find_all(name="td", attrs={"class":"t_f"})
    replylist = soup.find_all(name='div', attrs={"class":"pcb"})
    # next_page = soup.find('a', attrs={'class': 'nxt'})
    # if next_page:
    #     return soupname, souptime, next_page['herf']
    title = soup.find_all(name='span',attrs={"id":"thread_subject"})
    total_page = int((re.findall(r'<span title="共 (\d+) 页">', str(soup)) + [1])[0])
    return namelist,replylist,total_page,title
# \d{4}-\d{1}-\d{1}\s\d{2}\:\d{2}

def addtimestamp(filedir,lasttimestamp):
    with open(filedir, 'r+',encoding='UTF-8') as f:
        content = f.read()        
        f.seek(0, 0)
        f.write('> ## **本文件最后更新于'+lasttimestamp+'** \n\n'+content)

def get_FileSize(filePath):
 
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024 * 1024)
 
    return round(fsize, 2)

def FormatStr(namelist, replylist,totalpage,title):
    nametime = []
    replys = []
    times = []
    output= ''
    for i in namelist:
        i = i = re.sub(r'[\r\n]',' ',str(i))
        nametime.append(re.sub(r'<.+?>','',i))
    names = nametime[::2]
    timestamp = nametime[1::2]
    for i in timestamp:
        i = re.sub(r'[\r\n]',' ',str(i))
        i = re.sub(r'电梯直达','1#',i)
        i = re.search(r'\d+[\S\s]+发表于\s\d+-\d+-\d+\s\d+:\d+',i)
        times.append(i.group(0))
    for i in replylist:
        i = re.sub(r'\r','\n',str(i))
        # i = re.sub(r'\n\n','\n',i)
        
        i = re.sub(r'<blockquote>','[[[[blockquote]]]]',i)
        i = re.sub(r'</blockquote>','[[[[/blockquote]]]]',i)
        # i = re.sub(r'</blockquote>','\n',i)
        i = re.sub(r'<strong>','[[[[strong]]]]',i)
        i = re.sub(r'</strong>','[[[[/strong]]]]',i)
        # i = re.sub(r'</strong>','** ',i)
        i = re.sub(r'<span class=\"icon_ring vm\">','﹍﹍﹍\n\n',str(i))
        i = re.sub(r'<td class="x.1">','|',i)
        i = re.sub(r'\n</td>','',i)
        i = re.sub(r'</td>\n','',i)
        i = re.sub(r'<div class="modact">(.+?)</div>','\n\n *\\1* \n\n',i)
        i = re.sub(r'<a href="http(.+?)" target="_blank">(.+?)</a>','[\\2](http\\1)',i)
        i = re.sub(r'<img alt=\".*?\" border=\"\d+?\" smilieid=\"\d+?\" src=\"','[[[[img src="',i)
        i = re.sub(r'"/>','"/)',i)
        i = re.sub(r'<img .*?file="','[[[[img src="',i)
        i = re.sub(r'jpg".+\)','jpg" referrerpolicy="no-referrer"]]]]',i)
        i = re.sub(r'png".+\)','png" referrerpolicy="no-referrer"]]]]',i)
        i = re.sub(r'gif".+\)','gif" referrerpolicy="no-referrer"]]]]',i)
        i = re.sub(r'jpeg".+\)','jpeg" referrerpolicy="no-referrer"]]]]',i)
        i = re.sub(r'webp".+\)','webp" referrerpolicy="no-referrer"]]]]',i)
        i = re.sub(r'tif".+\)','tif" referrerpolicy="no-referrer"]]]]',i)
        i = re.sub(r'<.+?>','',i)
        i = re.sub(r'\n(.*?)\|(.*?)\|(.*?)\n','\n|\\1|\\2|\\3|\n',i)
        i = re.sub(r'收起\n理由','|昵称|战斗力|理由|\n|----|---|---|',i)
        i = re.sub(r'\|\n+?\|','|\n|',i)
        i = re.sub(r'\[\[\[\[','<',i)
        i = re.sub(r'\]\]\]\]','>',i)
        i = re.sub(r'\[(.+?发表于.+?\d)\]\((http.+?)\)','<a href="http\\2" target="_blank">\\1</a>',i)
        replys.append(i)
    for i in range(len(replylist)):
        output = output + '\n\n-----\n\n' +'#### '+str(names[i]) + '\n##### '+str(times[i]) + '\n'+str(replys[i] ) +'\n'
    output = re.sub(r'\r','\n',output)
    return output

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
    # # 浏览器登录后得到的cookie，也就是刚才复制的字符串
    cookie_str = r'YourCookie'
    # #把cookie字符串处理成字典，以便接下来使用
    cookies = {}
    for line in cookie_str.split(';'):
        key, value = line.split('=', 1)
        cookies[key] = value
    # 设置请求头
    headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    '''
    下面的page为帖子号，默认从第一页开始下载
    '''
    rootdir="C:/Users/riko/Documents/S1/S1PlainTextBackup/"

    with open(rootdir+'RefreshingData.json',"r",encoding='utf-8') as f:
        thdata=json.load(f)

    for i in range(len(thdata)):
        page = thdata[i]['id']
        RURL = 'https://bbs.saraba1st.com/2b/thread-'+page+'-1-1.html'
        s1 = requests.get(RURL, headers=headers,  cookies=cookies, timeout=10)
        # s1 = requests.get(RURL, headers=headers)
        # s1.encoding='utf-8'
        data = s1.content
        namelist, replylist,totalpage,title= parse_html(data)
        titles = re.sub(r'<.+?>','',str(title))
        titles = re.sub(r'[\]\[]','',titles)
        titles = re.sub(r'\|','｜',titles)
        titles = re.sub(r'/','／',titles)
        titles = re.sub(r'\\','＼',titles)
        titles = re.sub(r':','：',titles)
        titles = re.sub(r'\*','＊',titles)
        titles = re.sub(r'\?','？',titles)
        titles = re.sub(r'"','＂',titles)
        titles = re.sub(r'<','＜',titles)
        titles = re.sub(r'>','＞',titles)
        titles = re.sub(r'\.\.\.','…',titles)
        thdata[i]['title'] = titles
        deletepage = int(thdata[i]['totalpage'])
        if(totalpage > int(thdata[i]['totalpage'])):
            thdata[i]['totalpage'] = str(totalpage)
            if(int(thdata[i]['lastpage']) > 1):
                mkdir(rootdir+str(page)+'-'+titles+'/')
            startpage = int(thdata[i]['lastpage'])
            count = 1
            while(count <= totalpage):
                for thread in range(startpage,totalpage+1):
            # thread = 1
                    RURL = 'https://bbs.saraba1st.com/2b/thread-'+page+'-'+str(thread)+'-1.html'
                    # s1 = requests.get(RURL, headers=headers)
                    s1 = requests.get(RURL, headers=headers,  cookies=cookies, timeout=10)
                    data = s1.content
                    namelist, replylist,totalpage,title= parse_html(data) 
                    output = FormatStr(namelist, replylist,totalpage,title)                
                    # titles = re.sub(r'】',']',titles)
                    # currenttime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
                    # with open("C:/Users/riko/Desktop/test.md",'w',encoding='utf-8') as f:
                        # 
                            # f.write(str(i)+'\n')
                    # with open(rootdir+str(page)+'-'+titles+'/'+str(page)+'-'+titles+'-'+str(startpage)+'-'+str(totalpage)+'页.md',"a",encoding='utf-8') as f:
                    lastsave=time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
                    if(int(thdata[i]['lastpage']) > 1):
                        with open(rootdir+str(page)+'-'+titles+'/'+str(page)+'-'+titles+'-'+str(startpage)+'-'+str(totalpage)+'页.md',"a",encoding='utf-8') as f:
                            f.write(output)
                        if(thread == totalpage):
                            count = totalpage +1
                            addtimestamp(rootdir+str(page)+'-'+titles+'/'+str(page)+'-'+titles+'-'+str(startpage)+'-'+str(totalpage)+'页.md',lastsave)
                            if(os.path.exists(rootdir+str(page)+'-'+titles+'/'+str(page)+'-'+titles+'-'+str(startpage)+'-'+str(deletepage)+'页.md')):
                                os.remove(rootdir+str(page)+'-'+titles+'/'+str(page)+'-'+titles+'-'+str(startpage)+'-'+str(deletepage)+'页.md')
                            thdata[i]['lastedit'] = str(int(time.time()))
                            # os.rename(rootdir+str(page)+'-'+titles+'/'+str(page)+'-'+titles+'-'+str(startpage)+'-'+str(totalpage)+'页.md',rootdir+str(page)+'-'+titles+'/'+str(page)+'-'+titles+'-'+str(startpage)+'-'+str(thread)+'页@'+lastsave+'.md')
                            break
                        if(get_FileSize(rootdir+str(page)+'-'+titles+'/'+str(page)+'-'+titles+'-'+str(startpage)+'-'+str(totalpage)+'页.md') >= 0.9):
                            os.rename(rootdir+str(page)+'-'+titles+'/'+str(page)+'-'+titles+'-'+str(startpage)+'-'+str(totalpage)+'页.md',rootdir+str(page)+'-'+titles+'/'+str(page)+'-'+titles+'-'+str(startpage)+'-'+str(thread)+'页.md')
                            addtimestamp(rootdir+str(page)+'-'+titles+'/'+str(page)+'-'+titles+'-'+str(startpage)+'-'+str(thread)+'页.md',lastsave)
                            startpage = thread+1
                            thdata[i]['lastpage'] = str(startpage)
                            break
                    else:
                        with open(rootdir+str(page)+'-'+titles+'-'+str(startpage)+'-'+str(totalpage)+'页.md',"a",encoding='utf-8') as f:
                            f.write(output)
                        if(get_FileSize(rootdir+str(page)+'-'+titles+'-'+str(startpage)+'-'+str(totalpage)+'页.md') >= 0.9):
                            os.rename(rootdir+str(page)+'-'+titles+'-'+str(startpage)+'-'+str(totalpage)+'页.md',rootdir+str(page)+'-'+titles+'-'+str(startpage)+'-'+str(thread)+'页.md')
                            addtimestamp(rootdir+str(page)+'-'+titles+'-'+str(startpage)+'-'+str(thread)+'页.md',lastsave)
                            startpage = thread+1
                            thdata[i]['lastpage'] = str(startpage)
                            mkdir(rootdir+str(page)+'-'+titles+'/')
                            break
                        if(thread == totalpage):
                            count = totalpage +1
                            addtimestamp(rootdir+str(page)+'-'+titles+'-'+str(startpage)+'-'+str(totalpage)+'页.md',lastsave)
                            if(os.path.exists(rootdir+str(page)+'-'+titles+'/'+str(page)+'-'+titles+'-'+str(startpage)+'-'+str(deletepage)+'页.md')):
                                os.remove(rootdir+str(page)+'-'+titles+'/'+str(page)+'-'+titles+'-'+str(startpage)+'-'+str(deletepage)+'页.md')
                            thdata[i]['lastedit'] = str(int(time.time()))
                            break
        if(int(time.time()) - int(thdata[i]['lastedit']) > 15552000):
            thdata.pop(i)
    with open(rootdir+'RefreshingData.json',"w",encoding='utf-8') as f:
        f.write(json.dumps(thdata,indent=2,ensure_ascii=False))





