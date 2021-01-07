## Biblioteca Catalogadora de Candles
Autor: Souza, Gustavo.

Objetivo: Desenvolver uma biblioteca (functions.py) para catalogação dos candles de ativos do mercado financeiro com a finalidade de contribuir para a previsão estatística. Até o momento está sendo utilizado uma API extra-oficial para a leitura dos candles. Projeto em fase inicial de desenvolvimento, mas já pode ser utilizado para exportação de dados. 

```
from functions import cataloguer
api = cataloguer(email,password)
api.connect()

# pandas dataframe
df = api.read_candles(goal, timeframe, start, end)
```

### Demonstração

Utilize o arquivo cataloguer.py.
```
  ____    _  _____  _    _     ___   ____ _   _ _____ ____  
 / ___|  / \|_   _|/ \  | |   / _ \ / ___| | | | ____|  _ \ 
| |     / _ \ | | / _ \ | |  | | | | |  _| | | |  _| | |_) |
| |___ / ___ \| |/ ___ \| |__| |_| | |_| | |_| | |___|  _ < 
 \____/_/   \_\_/_/   \_\_____\___/ \____|\___/|_____|_| \_\
                                                            

By Gustavo Souza
Repository: https://github.com/gdssouza/po_bot_with_telegram

Start your robot
Insert start date YYYY/MM/DD :/> 2020/01/08
Insert end date YYYY/MM/DD :/> 2021/01/06
Insert timeframe in minutes :/> 15
Insert the goal :/> EURUSD
24806 candles read in 35.11 seconds
Saved in EURUSD.csv
                                open     close       min       max  volume
goal   date                                                               
EURUSD 2020-01-08 00:00:00  1.114950  1.115420  1.114775  1.115450    2461
       2020-01-08 00:15:00  1.115415  1.116755  1.115270  1.116835    2957
       2020-01-08 00:30:00  1.116760  1.116260  1.116000  1.116760    3037
       2020-01-08 00:45:00  1.116255  1.116045  1.116035  1.116555    2750
       2020-01-08 01:00:00  1.116055  1.115875  1.115870  1.116250    2646
```

### Próximos Passos

* Função que analisa a tendência
* Função que faz a catalogação por horário, dia e período
* Leitura de multiplos ativos

### Contribuições

O projeto é Open Source, todos os interessados estão convidados a contribuir. Os envolvidos serão definidamente creditados.

### Referências
Alexander Skiridomov, criador da API. Visite https://github.com/n1nj4z33/iqoptionapi

Lu-Yi-Hsun, contribuidor da API (Fork utilizada no projeto). Visite https://github.com/Lu-Yi-Hsun/iqoptionapi
