<h1 align='center'>TwComp</h1>
<p align='center'>Utiliza técnicas de Processamento de Linguagem Natural (PLN) e machine learning em dados coletados do twitter (tweets) para analisar emoções sobre determinada busca escolhida pelo usuário. A ferramenta é capaz de gerar gráficos dos resultados, Word Cloud com as palavras que mais apareceram nos tweets e mapas com as posições geográficas dos autores dos tweets. Induzindo insights sobre determinada busca feita pelo usuário.</p>
<p><a href='https://twcomp.xyz/'>Clique aqui para ver a aplicação funcionando</a></p>

<p align='center'>
<a href='#feature'>Features</a> |
<a href='#pré-requisito'>Pré Requisitos</a> |
<a href='#pré-requisito'>Rodando a Aplicação</a> |
<a href='#pré-requisito'>Tecnologias</a> |
<a href='#pré-requisito'>Autor</a> |
</p>
<hr>
<br>
<a href='https://twcomp.xyz/'>
<img src='./static/images/twcomp.gif'>
</a>
<br>
<br>
<hr>

 ## Feature

- [x] Coleta tweets utilizando Web Scraping.
- [x] Coleta tweets utilizando a API do Twitter (é necessario se cadastrar com as chaves da API).
- [x] Analisa o sentimento dos tweets.
- [x] Cria um WordCloud com as palavas que mais apareceram nos tweets.
- [x] Gera gráficos representando os sentimentos dos tweets.
- [x] Gera CSV com todos os tweets.
- [x] Gera um PDF com resumo da análise.


## Pré-Requisito

Você precisar instalar em sua máquina as seguintes ferramentas: <a href='https://git-scm.com/'>Git</a>, <a href='https://www.python.org/'>Python</a>.

Você também vai precisar de um editor de codigo como o <a href='https://code.visualstudio.com/'>VSCode</a>

## Rodando a Aplicação
```bash
# Clone este repositório
$ git clone https://github.com/danielares/TwComp
# Acesse a pasta do projeto no terminal/cmd
$ cd TwComp
# Instale as dependências
$ pip install -r requirements.txt
# Crie um arquivo chamado 'django_key.py' e insira sua chave nele (SECRET_KEY='SUA CHAVA AQUI')
# Execute a aplicação
python manage.py runserver
#Acesse a aplicação no endereço http://localhost:3000/
```

## Tecnologias
As seguintes tecnologias abaixo foi usada na construção do projeto:

- <a href='https://www.python.org/'>Python</a>
- <a href='https://www.djangoproject.com/'>Django</a>
- <a href='https://getbootstrap.com/'>Bootstrap</a>

<hr>

## Autor
Made by Daniel Ares 👋