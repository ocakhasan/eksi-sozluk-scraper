from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas

class EksıSozlukScraper:
    url = "https://eksisozluk.com/"
    uClient = urlopen(url)
    page_html = uClient.read()
    uClient.close()
    page_soup = BeautifulSoup(page_html, "html.parser")
    
    
        
    
    def getPopularHeadLines(self):

        

        """

        It returns a List Object
        containing all the Popular
        Titles of Ekşi Sözlük

        """
        result = []
        containers = self.page_soup.find("ul", {"class": "topic-list partial"}).find_all("li")

        for a in containers:
            text = a.get_text(strip=True)
            if text != "":
                result.append(text)

        df = pandas.DataFrame()

        df['title'] = result

        df.to_csv("PopularHeadLines.csv")

        return df

    
    def getDataFromURL(self, url):

        """

        It returns a DataFrame 
        and print the whole dataframe to a csv file
         so it can be used

        """
        
        
        raw_url = url
        text = []
        author = []
        date = []
        
        uClient = urlopen(url)
        page_html = uClient.read()
        uClient.close()
        page_soup = BeautifulSoup(page_html, "html.parser")
        containers = page_soup.find("ul", id="entry-item-list").find_all("li")
        page_number = page_soup.find("div",{"class": "pager"}).get("data-pagecount")
        title = page_soup.find("div", id="topic").find("h1", id="title").get("data-title")
        
        
        for i in range(1, int(page_number)+1):
            url = raw_url + "?p=" + str(i)
            uClient = urlopen(url)
            page_html = uClient.read()
            uClient.close()
            page_soup = BeautifulSoup(page_html, "html.parser")
            containers = page_soup.find("ul", id="entry-item-list").find_all("li")

            
            
            for item in containers:
                text.append(item.find(class_='content').get_text(strip=True))
                author.append(item.find(class_="entry-author").get_text(strip=True))
                date.append(item.find(class_="entry-date").get_text(strip=True))


        df = pandas.DataFrame()
        df['text'] = text
        df['author'] = author
        df['date'] = date
        df['title'] = title
        filename = raw_url[23:-9] + ".csv"

        df.to_csv(filename, index=False, encoding="utf-8")

        return df

    
    


    
    


def main():
    eksıWrapper = EksıSozlukScraper()
    titles = eksıWrapper.getPopularHeadLines()
    df = eksıWrapper.getDataFromURL("https://eksisozluk.com/besiktas-covid-19-testlerinin-negatif-cikmasi--6433522")
    #print(df.head())
    #print(titles.head())

if __name__ == "__main__":
    main()
    
    

