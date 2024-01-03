from bs4 import BeautifulSoup
import requests
import re

def tradeSpider( maxPages):
    expresii = ["(pat|masa|scaun|dulap|birou|scari)", "(sipca|tigla|roaba|nisip|lemn|geam|caramida|piatra)",
                "(bec|intrerupator|lustra|lampa|cablu|wc baterie|dus|centrala|soba|calorifer)",
                "(sudura|drujba|ciocan|fierastrau|cric)",
                "(ciaun|tacamuri|pahare|scrumbiera|cesti|detergent|butoi)",
                "(rafturi|hale|container|)",
                "(oglinda|chiuveta|wc|bideu|dus|prosop)",
                "ceas|birou|masa|scaun|organizator|raft|veioza",
                "blat|scaun|set|masa|coltar|chiuveta|farfurie|mixer|halba|cutit"
                ]
    categorii = ["Mobila-Decoratiuni", "Gradina", "Materiale constructii si amenajari", "Termice-Electrice-Sanitare",
                 "Unelte-Scule-Feronerie", "Articole menaj", "Hale metalice, structuri metalice si containere",
                 "Baie", "Birou", "Bucatarie"]
    legatura = [0]*len (expresii)
    n = len(expresii)
    page = 1
    while page <= maxPages:
        url = "https://www.olx.ro/d/casa-gradina/?currency=RON&page=" + str(page)

        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, "lxml")

        results = soup.find_all("h6")
        for result in results:
            result=str(result)
            result = result.lower()
            #print (result)
            for i in range (n):
                if (re.search(expresii[i], result) is not None):
                    legatura[i] += 1
                    print(result[36:-5])
        page += 1
tradeSpider(25)