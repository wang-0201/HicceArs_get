import requests,re,os,time,random
from retrying import retry
from bs4 import BeautifulSoup
#from fake_useragent import UserAgent
#ua = UserAgent(verify_ssl=False)
#print(ua.chrome)
#请手动创建文件夹，将地址复制在targetDir引号内，且将 \改为 \\
targetDir = ''
#请手动浏览器F12查看cookie，复制在cookie引号内
cookie = ''
#可自行切换其他HicceArs网址
URL = 'https://www.hiccears.com/gallery.php?gid=4885'
header = {'Connection':'keep-alive',
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.10 Safari/537.36 Edg/77.0.235.5',
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
           'Cookie':cookie}
#中断后请从接下来的图片页数开始手动修改。例 看到260 写入成功后不继续或者报错，将num改为261再接着进行。
#大陆地区请使用VPN SS SSR并选择全局代理
num = 0
@retry(stop_max_attempt_number=5, stop_max_delay=20000,wait_fixed=30000)
def select_html():
    url = URL
    resultdata = requests.get(url, headers = header)
    soup = BeautifulSoup(resultdata.content,'lxml', from_encoding='utf-8')
    print('加载完成')
    a = soup.select('.panel-body>.row-margin-top>.col-md-3>a')
    select_href = []
    for i in range(len(a)):

        print(a[i]['href'])
        select_href.append('https://www.hiccears.com'+a[i]['href'][1:])
    print('共有',len(select_href))
    time.sleep(2)
    for x in range(num,len(select_href)):
    # for x in range(1):
        read_detail(select_href[x],x)
    print('执行完成')

@retry(stop_max_attempt_number=5, stop_max_delay=20000,wait_fixed=30000)
def read_detail(detail_path,x):
    detail_html = requests.get(detail_path, headers=header)
    soup = BeautifulSoup(detail_html.content, 'lxml', from_encoding='utf-8')
    div = soup.select('.panel-body>.row')
    a = div[1].select('a')
    href = 'https://www.hiccears.com'+a[0]['href'][1:]
    read_in(href,x)


@retry(stop_max_attempt_number=5, stop_max_delay=20000,wait_fixed=30000)
def read_in(img_path,x):

    print(img_path)
    if img_path.endswith('.png'):
        print('png',x)
        imgdata = requests.get(img_path, headers = header,timeout = 500)
        t = os.path.join(targetDir, str(x) + '.png')
    elif img_path.endswith('.jpg'):
        print('jpg',x)
        imgdata = requests.get(img_path, headers = header,timeout = 500)
        t = os.path.join(targetDir, str(x) + '.jpg')
    fw = open(t,'wb')  # 指定绝对路径
    fw.write(imgdata.content)
    fw.close()
    print(x,'写入成功')
    time.sleep(random.uniform(1.0,1.8))


if __name__ == "__main__":
    select_html()



