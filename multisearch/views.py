from django.shortcuts import render
from django.http import HttpResponse
import re
from django.shortcuts import render,redirect ,get_object_or_404
from .forms import SearchForm
import requests
import bs4
import  urllib,urllib3
# Create your views here.


def customsearch(request,*args,**kwargs):
    # res = requests.get('https://google.com/search?q=django')
    # res1 = requests.get('https://in.search.yahoo.com/search?p=hotstar')
    # res.raise_for_status()
    # res1.raise_for_status()
    # soup = bs4.BeautifulSoup(res.text,"html.parser")
    # soup1 = bs4.BeautifulSoup(res.text,"html.parser")
    # # linkElements = soup.select('.r a')
    # linkElements = soup.select("div.g")
    # linkElements1 = soup1.select("div.g")
    # linkToOpen = min(5,len(linkElements))
    # text1 = ''
    # for i in range(linkToOpen):
    #     text = '<div>'+str(linkElements[i])+'</div>'
    #     text1 = text1 + text
    #     print(i)
    # var3 =''
    form = SearchForm()
    if request.method == 'GET':
        return render(request,'search.html',{'form':form})
    if request.method == 'POST':
        form = SearchForm(request.POST)
        # return render(request,'searchresult.html')
        if form.is_valid():
            # print('form is valid')
            a = form.cleaned_data['Search_String']
            # print(a)
            var1 = scrapingFunction('https://google.com/search?q='+a)
            var2 = scrapingFunctionyahoo('https://in.search.yahoo.com/search?p='+a)
            var3 = testsearch(a)
            # print(var1)
            # var3 = var1 + var2
            # return HttpResponse('{% csrf_token %}<div>%s</div><div>%s</div'%(var1,var2))
            return render(request,'searchresult.html',{'var1': var1 , 'var2': var2,'var3':var3,'form':form})
    return render(request,'search.html',{'form':form})

def scrapingFunction(requesturl):
    print(requesturl)
    res = requests.get(requesturl)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    # linkElements = soup.select('.r a')
    linkElements = soup.select("h3.r")
    linkToOpen = min(5, len(linkElements))
    text1 = ''
    for i in range(linkToOpen):
        strvar = str(linkElements[i])
        x = strvar.find('href=')
        outstrvar = strvar[:x+5]+ "https://www.google.com/" + strvar[x+7:]
        # x=linkElements[i].find('<h3')
        # print(outstrvar)
        # text = '<div>' + str(linkElements[i]) + '</div>'
        text = '<div>' + outstrvar + '</div>'

        text1 = text1 + text
        # print(i)
    res.close()
    return text1


def scrapingFunctionyahoo(requestyahoo):
    print(requestyahoo)
    yahoovar = requests.get(requestyahoo)
    yahoovar.raise_for_status()
    yahooSoup = bs4.BeautifulSoup(yahoovar.text,"html.parser")
    yahooElements = yahooSoup.findAll("div",{"class":"compTitle options-toggle"})
    yahoolinkTOOpen = min(5,len(yahooElements))
    text1 = ''
    for i in range(yahoolinkTOOpen):
        text = '<div>' + str(yahooElements[i]) + '</div>'
        text1 = text1 + text
        # print(i)
    # yahoovar.close()
    return text1


def testsearch(requesturlbing):
    requestbing = "http://www.bing.com/search?q=%s" % (urllib.quote_plus(requesturlbing))
    # getRequest = urllib3.request(requestbing, None, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'})
    # urlfile = urllib3.urlopen(getRequest)
    # htmlResult = urlfile.read(200000)
    # urlfile.close()
    user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) ..'}
    http = urllib3.PoolManager(1, headers=user_agent)
    r1 = http.urlopen('GET',requestbing)
    # print(r1.data)
    bingsoup = bs4.BeautifulSoup(r1.data,"html.parser")
    # print(requestbing)
    # bingvar = requests.get(requestbing)
    # bingvar.raise_for_status()
    # bingSoup = bs4.BeautifulSoup(bingvar.text,"html.parser")
    if bingsoup.find('div',{"class":'b_overlay'}) == 0:
        bingsoup.find('div',{"class":'b_overlay'}).decompose()
    bingElements = bingsoup.findAll(['li','div'],{"class":["b_algo","irphead"]})
    # bingElemtssecond = bingElements.s
    binglinkTOOpen = min(5,len(bingElements))
    text1 = ''
    for i in range(binglinkTOOpen):
        text = '<div>' + str(bingElements[i]) + '</div>'
        text1 = text1 + text
        # print(i)
    # yahoovar.close()
    return HttpResponse(text1)