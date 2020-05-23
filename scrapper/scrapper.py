import requests as rq
import bs4
import textwrap
import re

class Scrapper:
	
	def search(self,tema):
		self.getWebPages(self.getUrls(tema))

	def getUrls(self,tema):
		headers={
		'user-agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0",
		"Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"
		}
		googleStringSearch='https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.format(tema)
		search=rq.get(googleStringSearch+rq.utils.quote(tema),headers=headers)
		search.raise_for_status()
		html=bs4.BeautifulSoup(search.text,features="html.parser")
		results = self.parseResults(html.select(".r a"))
		return (results)

	def parseResults(self,results):
		searchResults = []
		for result in results:
			url = result["href"]
			title = result.text
			searchResults.append([title, url])
		return searchResults

	def getWebPages(self,res):
		blacklist=["[document]","script","header","html","meta","head","input","noscript","style","link"]
		page=''
		for x in res:
		    if (len(x[0])!=0) and ("cache" not in x[1]) and ("youtube" not in x[1]) and ("google" not in x[1]):
		        content_validator=rq.head(x[1])
		        if "text/html" in content_validator.headers["content-type"]:
		            html = rq.get(x[1]).text
		            html_parsed=bs4.BeautifulSoup(html,features="html.parser")
		            nombreArchivo=html_parsed.find("title").string
		            if(nombreArchivo is None):
		                nombreArchivo=x[0]
		            notCleanText=html_parsed.find_all(text=True)
		            for z in notCleanText :
		                if z.parent.name not in blacklist and not isinstance(z,bs4.element.Comment):
		                    page+="{}".format(z)
		            nombreArchivo=re.sub(":",'',nombreArchivo)
		            print(nombreArchivo,x[1])
		            html_to_page=open("crawled_web_pages/"+nombreArchivo+".html","w+",encoding="utf8")
		            html_to_page.write(str(html_parsed))
		            txt_to_page=open("docs_web/"+nombreArchivo+".txt","w+",encoding="utf8")
		            lines=page.splitlines()
		            clean_text=[]
		            for line in  lines:
		                if(len(line)>0):
		                    if(len(line)>100):
		                        clean_text.extend(textwrap.wrap(line,width=80,replace_whitespace=False))
		                    else:
		                        clean_text.append(line)
		            for x in clean_text:
		                txt_to_page.write(x+"\n")
		    page=''
		    txt_to_page.close()
		    html_to_page.close()


