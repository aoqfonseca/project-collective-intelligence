# -*- coding: utf-8 -*- 

#######################################
# Última modificação : 25/07/2009
# Autor : Andre Fonseca
#  Código baseado no código do livro : "Programando a Inteligencia Coletiva" 
# 
# Codigo para realizar uma contagem de palavras de uma lista de blogs
# para depois aninhá-los em grupos
#
#######################################

import feedparser
import re

def conta_palavras_de_uma_url(endereco):
    dados = feedparser.parse(endereco)
    #dicionário para contar palavras
    conta_palavras_dic = {}
    
    #vou percorrer todas as entradas do parser para contar suas palavras
    for entrada in dados.entries:
        if 'sumary' in entrada:
            sumary = entrada.sumary
        else:
            sumary = entrada.description
        palavras = obtem_palavras(entrada.title + ' ' + sumary)
        for palavra in palavras:
            conta_palavras_dic.setdefault(palavra,0)        
            conta_palavras_dic[palavra] +=1

    titulo  = dados.channel.title

    return titulo,conta_palavras_dic

def obtem_palavras(html):
    txt = re.compile(r'<[^>]+>').sub('',html)
    palavras = re.compile(r'[^A-Z^a-z]+').split(txt)

    return [palavra.lower() for palavra in palavras if palavra != '']

blogs_por_palavra = {}
palavras_por_blog = {}
quantidade_feeds = 0 
listagem_blogs = ['http://metronus.com/blog/feed','http://feeds2.feedburner.com/GuilhermeChapiewski']
#,'http://feeds.feedburner.com/AkitaOnRails'
#for endereco in file('lista_blogs.txt'):
for endereco in listagem_blogs:
    quantidade_feeds += 1
    titulo,contagem = conta_palavras_de_uma_url(endereco)
    palavras_por_blog[titulo] = contagem
    for palavra,contador in contagem.items():
        blogs_por_palavra.setdefault(palavra,0)
        if (contador > 1):
            blogs_por_palavra[palavra] +=1

## Gerando um arquivos com os dados encontrados
# Usando uma filtragem de distribuição gaussiana... vou ficar com as palavras que estão entre 10 % e 63,7% (Fibonnacci)
lista_de_palavras = []
for palavra,conta_blog in blogs_por_palavra.items():
    perc = float(conta_blog) / quantidade_feeds
    if perc >0.10 and perc < 0.7854:
        lista_de_palavras.append(palavra)

# Escrevendo efetivamente a saida
saida  = file ('resultado.csv','w')
saida.write('Nome Blog')
for palavra in lista_de_palavras:
    saida.write(';%s' %palavra)

saida.write('\n')
for blog,cp in palavras_por_blog.items():
    saida.write(blog)
    for pal in lista_de_palavras:
        if pal in cp:
            saida.write (';%d' % cp[pal])
        else:
            saida.write (';0')

    saida.write('\n')
