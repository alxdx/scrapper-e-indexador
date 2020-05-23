from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from unicodedata import normalize
from .match import Match

class Indexer:
    stopWords=set(stopwords.words('spanish'))
    stopWordsEngl=set(stopwords.words('english'))

    def __init__(self,docs_to_index):
        self.headIndexer={}
        self.numeroPalabrasPorDoc=[]
        self.hbuffer=[]
        self.documentos_indexados=[]
        self.update_indexer(docs_to_index)

    def __normal(self,string):
        string=re.sub('_',' ',string)
        string=re.sub(r'[^\w\s]+',' ',string) #elimina simbolos
        string=re.sub(r"^\d+\s|\s\d+\s|\s\d+$",' ',string) ##elimina numeros solos
        string=re.sub(r"^\d+\s|\s\d+\s|\s\d+$",' ',string) ##elimina numeros solos
        string=string.lower()#↓↓ RETIRA DIACRITICOS MENOS ñ
        return string

#rutina para indexador
# recibe una lista de nombres de documentos 
#retorna un diccionario (la estructura del indexador)
    def makeIndex(self,docs:list):
        numDoc=len(self.documentos_indexados)
        for x in docs:
            if(x not in self.documentos_indexados):
                #print("indexado ->:{}".format(x))
                self.numeroPalabrasPorDoc.append([])
                tokens=[]
                doc=open(x,encoding='utf8')
                data=doc.readlines()
                ##para cada linea en el documento
                for i in range(len(data)):
                    data[i]=self.__normal(data[i])
                    lineTokenized=word_tokenize(data[i])
                    self.numeroPalabrasPorDoc[numDoc].append(len(lineTokenized))
                    if len(lineTokenized) > 0:
                        lineTokenized.insert(0,i) ##almacena el numero de linea al que pertenece en la cabeza de la lista
                        tokens.append(lineTokenized)
                        
                for linea in tokens:
                    numpalabra=0
                    numlinea=linea[0]
                    for palabra in linea:
                        if type(palabra) is not int:
                            if palabra not in self.stopWords and palabra not in self.stopWordsEngl:
                                if palabra not in self.headIndexer:
                                    match=Match(numlinea,[numpalabra])
                                    self.headIndexer.update({palabra:{numDoc:[1,match]}})## psible bug
                                else:
                                    #si el documento no esta en elindexador
                                    dicDocs= self.headIndexer.get(palabra)
                                    if numDoc not in dicDocs:
                                        match=Match(numlinea,[numpalabra])
                                        dicDocs.update({numDoc:[1,match]})
                                    #si el documento ya esta en el indexador
                                    else:
                                        self.headIndexer.get(palabra).get(numDoc)[0]+=1 ##actualiza a cantidad de ocurrencias
                                        matchAnterior=self.headIndexer.get(palabra).get(numDoc)[-1]
                                        if matchAnterior.getLinea() == numlinea:
                                            matchAnterior.addOcurrencias([numpalabra])
                                        else:
                                            match=Match(numlinea,[numpalabra])
                                            self.headIndexer.get(palabra).get(numDoc).append(match)
                            numpalabra+=1
                    numlinea+=1
                numDoc+=1
                self.documentos_indexados.append(x)

    def update_indexer(self,docs:list):
        self.makeIndex(docs)

    def __update_hbuffer(self):
        self.hbuffer=[]
        for x in range(len(self.documentos_indexados)):
            self.hbuffer.append(None)

    def searchIndex(self,word):
        if(len(self.documentos_indexados)>len(self.hbuffer)):
            self.__update_hbuffer()
        #print(len(self.documentos_indexados),len(self.hbuffer))
        index=self.headIndexer
        if word in index:
            resultados=0
            dicDoc=index.get(word)
            for doc in dicDoc:
                #buffer.insert(doc,open(txt[doc],encoding='utf8'))
                #print(self.hbuffer[doc])
                #print(dicDoc[doc][1].getLinea())
                #print(dicDoc[doc][1].getOcurrencias())
                self.hbuffer[doc]=open(self.documentos_indexados[doc],encoding='utf8').readlines()
                for value in dicDoc[doc]:
                    if type(value) is int:
                        print("\n    {} ocurrencias en {}".format(value,self.documentos_indexados[doc]))
                        resultados+=value
                    else:
                        lst=list(map(lambda x: x+1,value.getOcurrencias())) #le suma uno a cada elemento de las ocurrencias
                        print("\t\tEn linea {} \n\t\t\tpalabra {}".format(value.getLinea()+1,lst))
                        print("\n\t\t{}".format(self.hbuffer[doc][value.getLinea()]))
            print("\n\tTotal: {} resultados\n".format(resultados))
        else:
             print("la palabra no se encuentra en la base de datos\n")