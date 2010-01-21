# -*- coding: utf-8 -*- 

#######################################
# Última modificação : 25/07/2009
# Autor : Andre Fonseca
#  Código baseado no código do livro : "Programando a Inteligencia Coletiva" 
# 
# Codigo para a geração da taxionomia dos dados
# para poder agrupar as fotos em grupos de semelhantes
#
#######################################
from math  import sqrt
from PIL  import Image,ImageDraw

def le_arquivo_resultado_csv (arquivo):
    linhas  = [linha for linha in file(arquivo)]
    
    colunas = linhas[0].strip().split(';')[1:]
    linhas_lidas = []
    dados = []
    for linha in linhas[1:]:
        texto = linha.strip().split(';')
        linhas_lidas.append(texto[0])
        dados.append([float(x) for x in texto[1:]])

    return linhas_lidas,colunas,dados


def pearson(v1,v2):
    sum1 = sum(v1)
    sum2 = sum(v2)
    sum1Qd = sum([pow(v,2) for v in v1])
    sum2Qd = sum([pow(v,2) for v in v2])

    pSum = sum ([v1[i]*v2[i] for i in range(len(v1))] )
    num = pSum - (sum1*sum2/len(v1))
    den = sqrt( (sum1Qd-pow(sum1,2)/len(v1) )*(sum2Qd-pow(sum2,2)/len(v1)) )
    if den ==0 : return 0

    return 1.0-num/den


class bicluster:
    def __init__(self,vec,left=None,right=None,distance=0.0,id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance

def hcluster(rows,distance=pearson):
    distances = {}
    currentclustid =-1
    
    clust = [bicluster(rows[i],id=i) for i in range(len(rows))]
    while len(clust) > 1:
        lowestpair = (0,1)
        closest = distance(clust[0].vec,clust[1].vec)

        for i in range(len(clust)):
            for j in range (i+1,len(clust)):
                if(clust[i].id,clust[j].id) not in distances:
                    distances[(clust[i].id,clust[j].id) ] = distance(clust[i].vec,clust[j].vec)
                
                d = distances[(clust[i].id,clust[j].id)]
                
                if d< closest:
                    closest = d
                    lowestpair(i,j)
        
        mergevec = [ (clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i] )/2.0 for i in range(len(clust[0].vec)) ]
        newcluster = bicluster(mergevec,left=clust[lowestpair[0]],right=clust[lowestpair[1]],distance=closest,id=currentclustid)
        currentclustid-=1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

    return clust[0]

def obtem_altura(clust):
    if clust.left ==None and clust.right==None:
        return 1
    return obtem_altura(clust.left) + obtem_altura(clust.right)

def obtem_profundidade(clust):
    if clust.left ==None and clust.right==None:
        return 0
    return  max(obtem_profundidade(clust.left),obtem_profundidade(clust.right)) + clust.distance

def desenha_dendograma(clust,labels,jpeg='grupos.jpg'):
    altura = obtem_altura(clust) *20
    largura = 1200
    profundidade = obtem_profundidade(clust)

    escala = float(largura-150)/profundidade
    img = Image.new('RGB',(largura,altura),(255,255,255))
    draw = ImageDraw.Draw(img)
    draw.line( (0,altura/2,10,altura/2),fill=(255,0,0))
    
    desenha_no(draw,clust,10,(altura/2),escala,labels)
    img.save(jpeg,'JPEG')

def desenha_no(draw,clust,x,y,escala,labels):
    if clust.id < 0:
        h1 = obtem_altura(clust.left)*20
        h2 = obtem_altura(clust.right)*20
        top = y - (h1+h2)/2
        bottow = y + (h1+h2)/2
        l1 = clust.distance*escala
        draw.line( (x,top+h1/2,x,bottow-h2/2),fill=(255,0,0))
        draw.line( (x,top+h1/2,x+11,top+h1/2),fill=(255,0,0))
        draw.line( (x,bottow-h2/2,x+11,bottow-h2/2),fill=(255,0,0))
        desenha_no(draw,clust.left,x+11,(top+h1/2),escala,labels)
        desenha_no(draw,clust.right,x+11,(bottow-h2/2),escala,labels)
    else:
        draw.text((x+5,y-7),labels[clust.id],(0,0,0))



