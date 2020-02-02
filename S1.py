# # -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import time
import sys
import io
import os


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


def get_FileSize(filePath):
 
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024 * 1024)
 
    return round(fsize, 2)

if __name__ == '__main__':
    # url = 'https://bbs.saraba1st.com/2b/thread-1808327-812-1.html'

    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    # }

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

    #登录后才能访问的网页
    # url = 'https://bbs.saraba1st.com/2b/thread-1822440-1-1.html'

    # # 浏览器登录后得到的cookie，也就是刚才复制的字符串
    # cookie_str = r'_uab_collina=155477530039882998306669; unadblock=unadblock; __cfduid=dbd9e91983f1006c21f9b52cf37acb8b11554775298; UM_distinctid=169ffd45b2d286-073a4d25f4b92d-50343a5f-e1000-169ffd45b2e42c; _ga=GA1.2.902980739.1557052203; CNZZDATA1260281688=1437865748-1554770314-%7C1561100744; B7Y9_2132_smile=1465D1; B7Y9_2132_saltkey=D3GhbOZZ; B7Y9_2132_lastvisit=1561765113; B7Y9_2132_auth=1619AbWnQbtlJXBLZ0zuyUz0UKMjttG9Pf0kwh5s0%2ByxuNPtJoS4aPS%2FWl2C5A5W1qUQB%2F4%2FICiR0GZ7HJW8WIH3WCg; B7Y9_2132_lastcheckfeed=516449%7C1561781389; B7Y9_2132_atlist=516449%2C464256%2C155015%2C103359; B7Y9_2132_pc_size_c=0; B7Y9_2132_myrepeat_rr=R0; B7Y9_2132_yfe_in=1; B7Y9_2132_home_diymode=1; B7Y9_2132_sid=Q93K9v; B7Y9_2132_lip=122.225.220.132%2C1562057066; B7Y9_2132_visitedfid=75D6D51D4D48D74D115D83D135D140; B7Y9_2132_ulastactivity=d47fmAvt1i0%2Bb3i9vYV4yq%2Fln3eNvBgiMDs4EKhxNqnZZH2WOWC%2F; B7Y9_2132_viewid=tid_1298078; B7Y9_2132_sendmail=1; B7Y9_2132_st_p=516449%7C1562059958%7C7e01de1252f7bb996db04ad86fbf8a90; B7Y9_2132_st_t=516449%7C1562060149%7C7155932698e9a43f85f1c156d2b0c90d; B7Y9_2132_forum_lastvisit=D_27_1560306880D_140_1561288600D_48_1561513979D_115_1561800443D_74_1561806905D_4_1562042418D_51_1562049201D_6_1562055798D_75_1562060149; B7Y9_2132_checkpm=1; B7Y9_2132_lastact=1562060150%09forum.php%09ajax'
    # # #把cookie字符串处理成字典，以便接下来使用
    # cookies = {}
    # for line in cookie_str.split(';'):
    #     key, value = line.split('=', 1)
    #     cookies[key] = value

    # 设置请求头
    headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

    #在发送get请求时带上请求头和cookies
    # resp = requests.get(url, headers = headers, cookies = cookies)
    # for thread in range(1,3):
    page = '1911848'


    RURL = 'https://bbs.saraba1st.com/2b/thread-'+page+'-1-1.html'
    time.sleep(0.1)
    # s1 = requests.get(RURL, headers=headers,  cookies = cookies)
    s1 = requests.get(RURL, headers=headers)
    # s1.encoding='utf-8'
    data = s1.content
    namelist, replylist,totalpage,title= parse_html(data)
    startpage = 1
    count = 1
    while(count <= totalpage):
        for thread in range(startpage,totalpage+1):
    # thread = 1
            RURL = 'https://bbs.saraba1st.com/2b/thread-'+page+'-'+str(thread)+'-1.html'
            time.sleep(0.1)
            s1 = requests.get(RURL, headers=headers)
            data = s1.content
            namelist, replylist,totalpage,title= parse_html(data) 
            nametime = []
            replys = []
            times = []
            level = []
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
                i = re.sub(r'<blockquote>|</blockquote>','\n```\n',i)
                # i = re.sub(r'</blockquote>','\n',i)
                i = re.sub(r'<span class=\"icon_ring vm\">','﹍﹍﹍\n\n',str(i))
                # i = re.sub(r'068.png','>[香菜捂脸]<',i)
                # i = re.sub(r'049.png','>[尖嘴嘲讽]<',i)
                # i = re.sub(r'048.png','>[呲牙嘲讽]<',i)
                # i = re.sub(r'037.png','>[盲人]<',i)
                # i = re.sub(r'067.png','>[香菜脸]<',i)
                # i = re.sub(r'001.png','>[吃惊无语]<',i)
                # i = re.sub(r'125.png','>[扭曲]<',i)
                # i = re.sub(r'072.png|13.gif','>[比心]<',i)
                # i = re.sub(r'12.gif','>[吐舌]<',i)
                # i = re.sub(r'034.png','>[眼镜喝茶]<',i)
                # i = re.sub(r'066.png','>[XD]<',i)
                # i = re.sub(r'065.png','>[斜眼大笑]<',i)
                # i = re.sub(r'033.png','>[喝茶]<',i)
                # i = re.sub(r'075.png','>[温暖可爱]<',i)
                # i = re.sub(r'217.gif','>[粪海先辈大叫]<',i)
                # i = re.sub(r'34.gif|077.png','>[喷鼻血]<',i)

                
                # i = re.sub(r'(\d+.[jgp][pin][fg])','>[\\1]<',i)
                i = re.sub(r'<td class="x.1">','|',i)
                i = re.sub(r'\n</td>','',i)
                i = re.sub(r'</td>\n','',i)
                i = re.sub(r'<img alt=\".*?\" border=\"\d+?\" smilieid=\"\d+?\" src=\"','![](',i)
                i = re.sub(r'"/>',')',i)
                i = re.sub(r'<.+?>','',i)
                i = re.sub(r'\n(.*?)\|(.*?)\|(.*?)\n','\n|\\1|\\2|\\3|\n',i)
                i = re.sub(r'收起\n理由','|昵称|战斗力|理由|\n|----|---|---|',i)
                i = re.sub(r'\|\n+?\|','|\n|',i)
            #     i = re.sub(r'\[blockquote\](.+)$\n(.*)\[/blockquote\]','>\\1\n>\\2\n\n',i)
            #     i = re.sub(r'\[blockquote\](.+)$\n(.*)$\n(.*)\[/blockquote\]','>\\1\n>\\2\n>\\3\n\n',i)
            #     i = re.sub(r'\[blockquote\](.+)$\n(.*)$\n(.*)$\n(.*)\[/blockquote\]','>\\1\n>\\2\n>\\3\n>\\4\n\n',i)
            #     # i = re.sub(r'\[blockquote\](.+?)\n(.+?)\[/blockquote\]','>\\1\n>\n>\\2\n\n',i)
            #     # i = re.sub(r'\[blockquote\](.*?)\n(.*?)\n(.+?)\[/blockquote\]','>\\1\n>\\2\n>\\3\n\n',i)
            #     i = re.sub(r'\[blockquote\](.+)$\n(.*)$\n(.*)$\n(.*)$\n(.*)\[/blockquote\]','>\\1\n>\\2\n>\\3\n>\\4\n>\\5\n\n',i)
            #     i = re.sub(r'\[blockquote\](.+)$\n(.*)$\n(.*)$\n(.*)$\n(.*)$\n(.*)\[/blockquote\]','>\\1\n>\\2\n>\\3\n>\\4\n>\\5\n>\\6\n\n',i)
                replys.append(i)
            for i in range(len(replylist)):
                output = output + '\n\n-----\n\n' +'#### '+str(names[i]) + '\n##### '+str(times[i]) + '\n'+str(replys[i] ) +'\n'
            output = re.sub(r'\r','\n',output)
            # output = re.sub(r'\n\n\n','\n',output)
            # output = re.sub(r'\n\n\n','\n',output)
            titles = re.sub(r'<.+?>','',str(title))
            titles = re.sub(r'[\]\[]','',titles)
            titles = re.sub(r'【','[',titles)
            titles = re.sub(r'】',']',titles)
            # currenttime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
            # with open("C:/Users/riko/Desktop/test.md",'w',encoding='utf-8') as f:
                # 
                    # f.write(str(i)+'\n')
            with open("C:/Users/riko/Desktop/"+str(page)+titles+str(startpage)+'-'+str(totalpage)+'页.md',"a",encoding='utf-8') as f:
                f.write(output)
            if(thread == totalpage):
                count = totalpage +1
                break
            if(get_FileSize("C:/Users/riko/Desktop/"+str(page)+titles+str(startpage)+'-'+str(totalpage)+'页.md') >= 1):
                os.rename("C:/Users/riko/Desktop/"+str(page)+titles+str(startpage)+'-'+str(totalpage)+'页.md',"C:/Users/riko/Desktop/"+str(page)+titles+str(startpage)+'-'+str(thread)+'页.txt')
                startpage = thread+1
                break






