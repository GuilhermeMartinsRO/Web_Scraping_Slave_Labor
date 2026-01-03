from bs4 import BeautifulSoup as bs
import requests
from urllib.parse import urljoin as uj
import pandas as pd
from io import StringIO

#nessa função eu pego todos os links que me interessa e filtro para pegar apenas os documentos .csv
def is_file_link(href):
    if not href:
        return False
    href = href.lower()
    return href.endswith('.csv')


#literalmente o site do governo brasileiro sobre combate ao trabalho escravo
url = 'https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho/areas-de-atuacao/combate-ao-trabalho-escravo-e-analogo-ao-de-escravo'

#faz a requisição HTTP para obter o conteúdo da página
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}

#obtém o conteúdo HTML da página porém em string
page = requests.get(url,headers=headers).text

#transforma o conteúdo HTML em um objeto BeautifulSoup(o que permite a edição e extração de dados)
soup = bs(page,'html.parser')

#encontra todos os links internos na página (classe 'internal-link') e seleciona o 11 e 12º links
links = soup.find_all('a',class_='internal-link')
file_links = [a for a in links if is_file_link(a.get('href'))]
df=[]
nomes=[]
for link in file_links:

    href = link.get('href')

    #monta URL absoluta caso seja relativa
    arquivo_url = uj(url, href)

    nomes.append('a'+arquivo_url.split('/')[-1].replace('.csv','').lower()) 

    #obtém o conteúdo do arquivo
    r = requests.get(arquivo_url, headers=headers)

    # converte o conteúdo binário em texto
    csv_text = r.content.decode("latin1")  # ajuste encoding se necessário

    data = pd.read_csv(StringIO(csv_text), sep=";")

    # cria o DataFrame diretamente
    df.append(data)


