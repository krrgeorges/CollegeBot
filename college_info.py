from bs4 import BeautifulSoup as bs
import urllib.request
import telegram



def log(string):
    from datetime import datetime
    i = datetime.now()
    print(i.strftime('%Y/%m/%d %H:%M:%S')+" : "+string)
    
class College_Information:
    url = "http://www.siesascs.edu.in"

    def get_parsed_html(self):
        urlparse = urllib.request.urlopen(self.url)
        soup = bs(urlparse,"html.parser")
        return soup
    
    def send_contact(self,bot,update):
        try:
            bot.send_message(chat_id=update.message.chat_id,text="Providing you our contact information...")
            address = "\nSIES Lane, Jain Society,\nSion West,\nJain Society,\nSion, Mumbai,\nMaharashtra 400022\n\n"
            telephone = "\n(022) 24 072 729 (Office)\n\n"
            fax = "\n(022) 24 096 633\n\n"
            mail = "\nsiesascs@siesascs.net"
            location = [19.0411339,72.8613285]
            contactinfo = "<b>Address : </b>"+address+"<b>Telephone : </b>"+telephone+"<b>Fax : </b>"+fax+"<b>Mail : </b>"+mail
            bot.send_message(chat_id=update.message.chat_id,text=contactinfo,parse_mode=telegram.ParseMode.HTML)
            bot.sendLocation(chat_id=update.message.chat_id,latitude=location[0],longitude=location[1])
            log("Sent contact information to "+update.message.from_user.first_name)
        except Exception as e:
            log("Contact information cannot be sent : "+str(e))

    def send_news(self,bot,update):
        try:
            bot.send_message(chat_id=update.message.chat_id,text="Providing you news of the college...")
            soup = self.get_parsed_html()
            urlparse = urllib.request.urlopen(self.url)
            soup = bs(urlparse,"html.parser")
            uls = soup.find_all("ul")
            news=[];links=[]
            for ul in uls:
                if ul.get("class")!=None and "li-underline" in ul.get("class") and "margin-sm" in ul.get("class") and "remove-padding" in ul.get("class"):
                    for li in ul.find_all("li"):
                        news.append(" ".join(li.text.split()))
                        href = li.find_all("a")[0].get("href")
                        if "http" in href:
                            links.append(href.replace(" ","%20"))
                        else:
                            links.append(self.url+href.replace(" ","%20"))
            for i in range(len(news)):
                newstext = "<a href='"+links[i]+"'>"+news[i]+"</a>"
                print(newstext)
                bot.send_message(chat_id=update.message.chat_id,text=newstext,parse_mode=telegram.ParseMode.HTML)
                        
        except Exception as e:
            log("Cannot retrieve news.News not sent : "+str(e))

