from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
from sys import maxint as MAX_INT

#GLOBAL VARIABLES
WINDOW_HEIGTH = 480
WINDOW_WIDGTH = 640
points = []
lines = []
buildingPolygon = []
Poligonos = []
Nails = []
firstClick = True
linesTemporario =[]
poligonosTemporario = []
repetedNails = []
clickInsidePolygon = False
margemDeErro = 2 #Margem de erro para a montagem do poligono e clique para remover o prego

   
#####################################################



##  Uma Classe para representar uma coordenada no plano. 
 #  Reprensenta os pontos x e y de um plano com um metodo 
 #  para acessar as coordenadas como um array. 

class Coordinate(object):
    _x = 0
    _y = 0

    ##  Um Construtor da classe
     #  @param xx Coordenada X
     #  @param yy Coordenada Y
    def __init__(self, xx, yy):
        self._x = xx
        self._y = yy
    
    ##  Um membro para acessar as variaveis da classe.
     #  @param self objeto possuidor das coordenadas
     #  @return  
    def getCoordinate(self):
        coordinates = [self._x, self._y]
        return coordinates

    def TranslateCoordinate(self, x, y):
        self._x += x
        self._y += y

    def RotateCoordinate(self, angle, nailX, nailY):

        translatedPointX = self._x - nailX  
        translatedPointY = self._y - nailY 

        self._x = ((math.cos(angle) * translatedPointX) - (math.sin(angle)*translatedPointY) + nailX)     
        self._y = ((math.sin(angle) * translatedPointX) + (math.cos(angle)*translatedPointY) + nailY)

    def setCoordinate(self, x, y):
        self._x = x
        self._y = y      

    def SameCoordinates(self, x, y):
        if ((x) >= (self._x - margemDeErro) and x <= (self._x+ margemDeErro) ) and (y >= (self._y - margemDeErro) and y <= (self._y + margemDeErro)):
            return True
        else:
            return False        

##  Uma Classe para representar um segmento de reta no plano. 
 #  Reprensenta os pontos x e y de inicio, x e y do final do segmento 

class LineCoordinate(object):
    ## Variaveis que representam o inicio do segmento de reta

    _coordinateBegin = Coordinate(0,0)
    _coordinateEnd = Coordinate(0,0) 

    ##  Um Construtor da classe
     #  @param xBeg Coordenada X inicial do segmento de reta
     #  @param yBeg Coordenada Y inicial do segmento de reta
     #  @param xEn Coordenada X final do segmento de reta
     #  @param yEn Coordenada Y final do segmento de reta
    def __init__(self, xBeg, yBeg, xEnd, yEnd):
        self._coordinateBegin = Coordinate(xBeg,yBeg)
        self._coordinateEnd = Coordinate(xEnd, yEnd)

    ##  Um membro para acessar as variaveis da classe.
     #  @param self objeto possuidor das coordenadas
     #  @return Coordenadas iniciais do segmento de reta
    def getCoordinateBegin(self):
        return self._coordinateBegin.getCoordinate()

    def TranslateLine(self, x, y):
        self._coordinateBegin.TranslateCoordinate(x,y)
        self._coordinateEnd.TranslateCoordinate(x,y)

    def RotateLine(self, angle, nailX, nailY):
        self._coordinateBegin.RotateCoordinate(angle,nailX,nailY)
        self._coordinateEnd.RotateCoordinate(angle,nailX,nailY)

    ##  Um membro para acessar as variaveis da classe.
     #  @param self objeto possuidor das coordenadas
     #  @return Coordenadas finais do segmento de reta
    def getCoordinateEnd(self):
        return self._coordinateEnd.getCoordinate()

    ##  Um membro para editar as variaveis da classe.
     #  @param self objeto possuidor das coordenadas
    def setCoordinateBegin(self, x, y):
        self._coordinateBegin.setCoordinate(x,y)
    
    ##  Um membro para editar as variaveis da classe.
     #  @param self objeto possuidor das coordenadas            
    def setCoordinateEnd(self, x, y):
        self._coordinateEnd.setCoordinate(x,y)

    ##  metodo que calcula o ponto de interseccao, se existir,
     #  da objeto atual com o segmento de reta recebido como parametro
     #  @brief O metodo monta a equacao parametrica para descrever todos os pontos dos segmentos de reta, igual as equacoes
     #  das duas retas, resolve o sistema para uma das variaveis parametrizados, o que ira gerar um denominador.
     #  E calculado se existe interseccao entre as retas, se houver entao o denominador gerado pelo solucao do sistema e testado,
     #  pois de esse denominados for 0, entao as retas sao collineares. Caso elas possuam apenas um ponto de interseccao, esse ponto e retornado
     #  @param self objeto atual
     #  @param Line segmento de reta no qual se deve calcular o ponto de interseccao
     #  @param PointOfIntersection coodenadas da intersecao das retas, se existir
     #  @return True se os segmento se intersecptam e False caso contrario    
        
    def intersect(self, Line, Colinear):
        cordinateBegin = self._coordinateBegin.getCoordinate()
        XBegin = cordinateBegin[0]
        YBegin = cordinateBegin[1]

        cordinateEnd = self._coordinateEnd.getCoordinate()
        XEnd = cordinateEnd[0]
        YEnd = cordinateEnd[1]

        LineAx = XBegin - XEnd
        LineAy = YEnd - YBegin
        LineA = (XEnd * YBegin) - (XBegin * YEnd) 
        
        LineBCoordinateBegin = Line.getCoordinateBegin()
        LineBCoordinateEnd = Line.getCoordinateEnd()
        P = ((LineAy * LineBCoordinateBegin[0]) + (LineAx * LineBCoordinateBegin[1]) + LineA)
        R = ((LineAy * LineBCoordinateEnd[0]) + (LineAx * LineBCoordinateEnd[1]) + LineA)
        
        if ((P != 0) and (R != 0) and ((P * R) >= 0)) :
            return False
  
        LineBx = LineBCoordinateBegin[0] - LineBCoordinateEnd[0]
        LineBy = LineBCoordinateEnd[1] - LineBCoordinateBegin[1]
        LineB = (LineBCoordinateEnd[0] * LineBCoordinateBegin[1]) - (LineBCoordinateBegin[0] * LineBCoordinateEnd[1]) 
        
        Q = ((LineBy * XBegin) + (LineBx * YBegin) + LineB)
        S = ((LineBy * XEnd) + (LineBx * YEnd) + LineB)
        
        if ((Q != 0) and (S != 0) and ((Q * S) >= 0)) :
            return False        

        Denom = (LineAy * LineBx) - (LineBy * LineAx)
        if Denom == 0:
            Colinear = True
            return True
        return True

##  Uma Classe para representar um grupo de poligonos (um poligono sozinho e um grupo, poligonos ligados por pregos e um grupo)
 #  Reprensenta os pregos, a raiz e os filhos do grupo.
class Group(object):

    _Nails = []
    _Children = []
    _Father = None

    def __init__(self, polygon):
        self._Nails = []
        self._Children = []
        self._Father = polygon

    ##  Procura se existe um prego que prega o pai desse grupo em um poligono recebido como parametro
     #  @param polygon poligono a ser procurado
     #  @return True se existe, False se nao existe
    def HasNailWith(self, polygon):
        return (polygon in self._Children)
    
    ##  Procura se existe um prego recebido como parametro
     #  @param nail prego a ser procurado
     #  @return True se existe, False se nao existe    
    def ContainNail(self, nail):
        return (nail in self._Nails)         

    ##  pega o prego que prega o pai desse grupo com um um poligono especifico
     #  @param polygon poligono a ser procurado
     #  @return retorna o prego se existir e none caso contrario    
    def getNailWith(self, polygon):
        for nail in self._Nails:
            if nail.getChild() == polygon:
                return nail
        return None


    ##  Recursivamente busca a raiz desse grupo, o pai de todos
     #  @return A raiz do grupo, o pai de todos
    def getRootGroup(self):
        Father = self._Father
        while Father != Father.getFather(): #Buscado a raiz do meu grupo
            Father = Father.getFather()
        return Father      

    ##  Pega o indice, ordem que foi desenhado, da raiz do grupo
     #  @return retorna o indice da raiz do grupo        
    def getGroupIndex(self):
        return self.getRootGroup().getIndex()

    ##  Testa se um determinado poligono e pai desse grupo
     #  @param father pai a ser testado
     #  @return True se for, nao caso contrario

    def IsFather(self, father):
        return (self.getFather() == father)

    def RemoveFather(self, father):
        self._Father = father       

    def getFather(self):
        return self._Father

    def GetNails(self):
        return self._Nails

    def GetChildren(self):
        return self._Children

    def RemoveNail(self, nail):
        self._Nails.remove(nail)

    def RemoveChild(self, child):
        self._Children.remove(child)


    ##  Recursivamente calcula o numeros de descendentes do pai desse grupo
     #  @return numero de descendentes do pai desse grupo
    def getNumberOfDescendant(self):
        numberOfDescendant = 1
        for child in self._Children:
            numberOfDescendant += child.getNumberOfDescendant()
        return numberOfDescendant    

    def AddNail(self, nail):
        if (nail not in self._Nails):
            self._Nails.append(nail)


    ##  CAlcula o numero de descendentes da raiz do grupo, ou seja o numero de elementos nesse grupo
     #  @return numero de elementos no grupo    
            
    def getNumberOfElements(self):
        return self.getRootGroup().getNumberOfDescendant()       

    def AddChild(self, child):
        self._Children.append(child)

    def setFather(self, father):
        self._Father = father              

    def TranslateGroup(self, x, y):
        for poligono in self._Children:
            poligono.setTranslation(x,y)

        for nail in self._Nails:
            nail.TranslateNail(x,y)

    def RotateGroup(self, angle, nailX, nailY):
        for poligono in self._Children:
            poligono.rotateGroup(angle, nailX, nailY)

        for nail in self._Nails:
            nail.RotateNail(angle, nailX, nailY)        

##  Uma Classe para representar um poligono
 #  Reprensenta os pontos e retas que o formam, o grupo do qual e pai, suas cores, seu indice, se pode rodar ou transladar e as coordenadas base de rotacao
class Polygon(object):
    Points = []
    Lines = []
    _BeginCoordinate = Coordinate(0, 0)
    _Group = None
    _redComponent = 0
    _greenComponent = 0
    _blueComponent = 0
    _index = -1
    _hasFather = False
    _canRotate = False
    _canTranslate = False
    _rotationBaseCoordinates = Coordinate(0,0)

    def getBeginCoordinate(self):
        return self._BeginCoordinate

    ##  Testa se um esse poligono e pai do prego que recebe como parametro
     #  @param nail prego a ser testado
     #  @return True se sim, False caso contratio   
    def ContainNail(self, nail):
        return self._Group.ContainNail(nail)

    def HasNailWith(self, polygon):
        return self._Group.HasNailWith(polygon)


    def CanRotate(self):
        return self._canRotate

    ##  Define o status de rotacao do poligono, se ele pode rodar
     #  @param status True caso o poligono possa rodar, False caso contrario
    def Rotate(self, status):
        self._canRotate = status    


    def CanTranslate(self):
        return self._canTranslate    

    ##  Define o status de rotacao do poligono, se ele pode transladas
     #  @param status True caso o poligono possa transladar, False caso contrario
        
    def Translate(self, status):
        self._canTranslate = status
            
    def getNailWith(self, polygon):
        return self._Group.getNailWith(polygon)

    def getIndex(self):
        return self._index

    ##  PEga o indice da raiz do grupo do qual esse poligno faz parte
     #  @return indice da raiz
        
    def getGroupIndex(self):
        return self._Group.getGroupIndex()    

    
    def setIndex(self, index):
        self._index = index


    def RemoveFather(self, dad):
        if self.IsFather(dad):
            self._Group.RemoveFather(self)
            self._hasFather = False
            self._canTranslate = True
            self._canRotate = False


    def IsFather(self, dad):
        return self._Group.IsFather(dad)            

    def SetGroup(self, group):
        self._Group = group

    def GetNails(self):
        return self._Group.GetNails()


    ##  troca o pai o meu pai por um poligono que recebi como parametro
     #  @param father novo pai
        
    def setFather(self, father):
        formerFather = self.getFather()
        nailWithFormerFather = formerFather.getNailWith(self)
        if formerFather != self:
            formerFather.RemoveNail(nailWithFormerFather)
            formerFather.setFather(self)
            formerFather.setRotationCoordinates(nailWithFormerFather)
            formerFather.RemoveChild(self)

            self.AddChild(formerFather)
            self.AddNail(nailWithFormerFather)

            nailWithFormerFather.setFather(self)
            nailWithFormerFather.setChild(formerFather)
        else:
            self._Group.setFather(father)
        self.Translate(False)
        self.Rotate(True)

    def getNumberOfElements(self):
        return self._Group.getNumberOfElements()        

    def GetChildren(self):
        return self._Group.GetChildren()    

    def getNumberOfDescendant(self):
        return self._Group.getNumberOfDescendant()

    def getFather(self):
        return self._Group.getFather()    
         
    def RemoveNail(self, nail):
        self._Group.RemoveNail(nail)

    def setRotationCoordinates(self, coordinate):
        self._rotationBaseCoordinates = coordinate

    def getRotationCoordinates(self):
        return self._rotationBaseCoordinates    

    def HasFather(self, status):
        self._hasFather = status

    def RemoveChild(self, child):
        self._Group.RemoveChild(child)    

    def DoesHasFather(self):
        return self._hasFather            

    def AddChild(self, polygonToAdd):
        self._Group.AddChild(polygonToAdd)

    ##  Adiciona um prego em qual sou pai
     #  @param nail prego a ser adicionado
        
    def AddNail(self, nail):
        nailPartnerChild = nail.getChild()

        #Casos onde ja exite um prego entre esses dois
        if self.HasNailWith(nailPartnerChild):
            nailPartnerChild.Translate(False)
            nailPartnerChild.Rotate(False)
            if nailPartnerChild.ContainNail(nail):
                nailPartnerChild.RemoveNail(nail)
            self._Group.AddNail(nail)
            nailPartnerChild.Translate(False)
            nailPartnerChild.Rotate(False)
            return False
        elif nailPartnerChild.HasNailWith(self):
            nail.setFather(nailPartnerChild)
            nail.setChild(self)
            if self.ContainNail(nail):
                self.RemoveNail(nail)
            nailPartnerChild._Group.AddNail(nail)
            self.Translate(False)
            self.Rotate(False)
            return False
        
        self._Group.AddNail(nail)
        return True
       
        
    ##  rotaciona o meu grupo dado um angulo recebifo
     #  @param rotationAngle angulo de rotacao
     #  @param coordenadas do eixo de rotacao
        
    def rotateGroup(self, rotationAngle, nailX, nailY):
        for point in self.Points:
            point.RotateCoordinate(rotationAngle, nailX, nailY)

        for line in self.Lines:
            line.RotateLine(rotationAngle, nailX, nailY)

        self._Group.RotateGroup(rotationAngle, nailX, nailY)    
     
    ##  Roda esse poligono dado a base de rotacao dele
     #  @param x coordenadas da posicao do mouse
     #  @param y coordenadas da posicao do mouse
     #  @param baseX coordenadas do inicio do movimento
     #  @param basey coordenadas do inicio do movimento
     
    def rotatePolygon(self, x, y, baseX, baseY):

        rotationBaseCoordinates = self._rotationBaseCoordinates.getCoordinate()
        nailX = rotationBaseCoordinates[0]
        nailY = rotationBaseCoordinates[1]

        rotationAngle =  getRotateAngle(x,y,baseX,baseY, nailX, nailY)
        for point in self.Points:
            point.RotateCoordinate(rotationAngle, nailX, nailY)

        for line in self.Lines:
            line.RotateLine(rotationAngle, nailX, nailY)

        self._Group.RotateGroup(rotationAngle, nailX, nailY)            
     
    ##  translada o meu grupo dado as coordenadas do mouse
     #  @param x coordenadas da posicao do mouse
     #  @param y coordenadas da posicao do mouse   

    def setTranslation(self, x, y):
        for point in self.Points:
            point.TranslateCoordinate(x,y)

        for line in self.Lines:
            line.TranslateLine(x,y)    

        self._Group.TranslateGroup(x,y)      

    def addLine(self, L):
        self.Lines.append(L)

    def addPoint(self, P):
        self.Points.append(P)


    ##  Testa se uma coordenda esta dentro do poligono
     #  @param x coordenda a ser testada
     #  @param y coordenada a ser testada
     #  @return True se esta dentro, False caso contrario    
        

    def insidePolygon(self, x,y):
        Colinear = False
        intersectionCount = 0
        infinityLine = LineCoordinate(x, y, MAX_INT, y)
        for line in self.Lines:
            if line.intersect(infinityLine, Colinear):
                intersectionCount += 1
                if Colinear:
                    return True

        if (intersectionCount%2) == 0: #EVEN
            return False
        else:#ODD
            return True            
                    
    def setRedComponent(self, R):
        self._redComponent= R   

    def setGreenComponent(self, G):
        self._greenComponent = G
        
    def setBlueComponent(self, B):
        self._blueComponent = B

    def getRedComponent(self):
        return self._redComponent
   
    def getGreenComponent(self):
        return self._greenComponent
   
    def getBlueComponent(self):
        return self._blueComponent    
                
    ##  Gera um cor aleatoria para o poligono            
    def setRandomColor(self):
        self.setRedComponent(random.uniform(0, 1))
        self.setGreenComponent(random.uniform(0, 1))
        self.setBlueComponent(random.uniform(0, 1))    

    def __init__(self, xBeg, yBeg):
       self._BeginCoordinate = Coordinate(xBeg, yBeg)
       self.Points = []
       self.Points.append(self._BeginCoordinate)
       self.Lines = []
       self.setRandomColor()
       self._children = []
       self._Group = Group(self)
       self._index = -1
       self._canTranslate = True
       self._canRotate = False

##  Uma Classe para representar um poligono
 #  Reprensenta as coordenadas do prego, o poligo base e o poligono filho, o indice da base e se esta pregado ao chao        
class Nail(object):
    _coordinate = Coordinate(0,0)
    _PolygonFather = Polygon(0,0)
    _polygonChild = Polygon(0,0)
    _indexFather = -1
    _NailedToGround = True

    def __init__(self, x, y):
        self._coordinate = Coordinate(x,y)
        _PolygonFather = Polygon(0,0)
        _polygonChild = Polygon(0,0)
        _indexFather = -1
        _NailedToGround = True

    def IsNailToGround(self):
        return self._NailedToGround

    ## Configura um poligono que foi pregado ao chao    
    def ConfigureToGround(self):
        self._PolygonFather.setRotationCoordinates(self)
        self._PolygonFather.Rotate(True)
        self._PolygonFather.Translate(False)    

    def setFather(self, father):
        self._PolygonFather = father

    def setChild(self, child):
        self._polygonChild = child    

    def getChild(self):
        return self._polygonChild

    def getFather(self):
        return self._PolygonFather 



    ##  Considerando a margem de erro testa se um coordenada foi em cima do prego
     #  @param x coordenada a testar
     #  @param y coordenada a testar   
    def ClickIn(self, x, y):
        return self._coordinate.SameCoordinates(x,y)    

    def getCoordinate(self):
        return self._coordinate.getCoordinate()


    ## Remove esse prego, trantando casos especiais de estar pregado ao chao ou de ter dois pregos entre dois poligonos    
    def Remove(self):
        self._PolygonFather.RemoveNail(self)
        Nails.remove(self)
        
        #Trata o caso especial de um poligono esta pregado no chao
        if self._NailedToGround:
            self._PolygonFather.Rotate(False)
            self._PolygonFather.Translate(True)
        else:   
            if (not self._polygonChild.CanTranslate()) and (not self._polygonChild.CanRotate()): # se um poligono estiver preso e porque tem mais de um prego com o mesmo poligono
                self._polygonChild.Rotate(True)
                self._polygonChild.Translate(False)
                self._polygonChild.setRotationCoordinates(self._PolygonFather.getNailWith(self._polygonChild))
            else:    
                self._PolygonFather.RemoveChild(self._polygonChild)
                self._polygonChild.RemoveFather(self._PolygonFather)
                self._polygonChild.Rotate(False)
                self._polygonChild.Translate(True)

            
    ##  Adiciona um poligono ao prego, testando se esse poligono deve ser base ou nao dado os criterios
     #  Que sao: maior numero de elementos no grupo > grupo de menor indice da raiz            
    def AddPolygon(self, polygon, index):
        if self._indexFather < 0: #Nao possui um poligono base
            self._indexFather = index
            self._PolygonFather = polygon   
            polygon.AddNail(self)
            self._NailedToGround = True
        else:
            self._NailedToGround = False
            if self._PolygonFather.getNumberOfElements() < polygon.getNumberOfElements():
                self._indexFather = index
                self._polygonChild = self._PolygonFather
                self._PolygonFather = polygon
                if self._PolygonFather.AddNail(self): 
                    self._polygonChild.RemoveNail(self)
                    self._PolygonFather.AddChild(self._polygonChild)
                    self._polygonChild.setFather(self._PolygonFather)
                    self._polygonChild.setRotationCoordinates(self)    

            else:
                if self._PolygonFather.getGroupIndex() < polygon.getGroupIndex(): 
                    self._PolygonFather.AddChild(polygon)
                    self._polygonChild = polygon
                    self._polygonChild.setFather(self._PolygonFather)
                    self._polygonChild.setRotationCoordinates(self)
                else:

                    self._indexFather = index
                    self._polygonChild = self._PolygonFather
                    self._PolygonFather = polygon
                    if self._PolygonFather.AddNail(self): 
                        self._polygonChild.RemoveNail(self)
                        self._PolygonFather.AddChild(self._polygonChild)
                        self._polygonChild.setFather(self._PolygonFather)
                        self._polygonChild.setRotationCoordinates(self)
                    

                        
        
    def TranslateNail(self, x, y):
        self._coordinate.TranslateCoordinate(x,y)

    def RotateNail(self, angle, nailX, nailY):
        self._coordinate.RotateCoordinate(angle, nailX, nailY)
    
## Monta a matriz com os tres pontos recebidos por parametro e calcula a determinante dessa matriz    
def determinate(P, Q, R):
    pPoints = P.getCoordinate()
    qPoints = Q.getCoordinate()
    rPoints = R.getCoordinate()

    positiveDiagonal = (qPoints[0] * rPoints[1]) + (rPoints[0] * pPoints[1]) + (pPoints[0] * qPoints[1])
    negativeDiagonal = (qPoints[0] * pPoints[1]) + (rPoints[0] * qPoints[1]) + (pPoints[0] * rPoints[1])

    return positiveDiagonal - negativeDiagonal

##  Calcula o angulo de rotacao dado a posicao do mouse, vetor base do movimento(posicao do clique) e eixo de rotacao(posicao do prego)
def getRotateAngle(x, y, baseX, baseY, nailX, nailY):

    baseXOrigin = baseX - nailX 
    baseYOrigin = baseY - nailY

    newPointXOrigin = x - nailX
    newPointYOrigin = y - nailY

    numerador = float((newPointXOrigin * baseXOrigin) + (newPointYOrigin * baseYOrigin))

    normaVectorBase = float(math.sqrt(float(newPointXOrigin*newPointXOrigin) + float(newPointYOrigin*newPointYOrigin))) # (x**2 + y**2)**(1/2)
    normaVectorNewPoint = float(math.sqrt(float(baseXOrigin*baseXOrigin) + float(baseYOrigin*baseYOrigin))) # (baseX**2 + baseY**2)**(1/2)

    
    # Erro de arredondamento faz com que essa formula faz com que a 5 casa decima nao seja 0
    if float(numerador/(normaVectorNewPoint*normaVectorBase)) > 1:
        rotationAngle = float(math.acos(1))
    else:
        rotationAngle = float(math.acos(numerador/(normaVectorNewPoint*normaVectorBase)))
    

    #Descobrindo orientacao do movimento
    det = determinate(Coordinate(nailX,nailY), Coordinate(x,y), Coordinate(baseX,baseY))

    if det < 0:
        return rotationAngle
    else:
        return - rotationAngle    

##  Um metodo que desenha um ponto na tela nas coordenadas recebidas como parametro
 #  @param x Ponto x da coordenada onde sera desenhado o ponto
 #  @param y Ponto y da coordenada onde sera desenhado o ponto                        
def drawPoint(x, y):
    glPointSize(10)
    glBegin(GL_POINTS)
    glVertex2f(x,y)
    glEnd()

##  Um Metodo que inicializa a janela
def initFun():
    glClearColor(1.0,1.0,1.0,0.0)
    glColor3f(0.0,0.0, 0.0)
    glPointSize(4.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0,640.0,0.0,480.0)


## metodo de resize da janela
def myReshape(widgth, heigth):
    global WINDOW_HEIGTH, WINDOW_WIDGTH
    WINDOW_HEIGTH = heigth
    WINDOW_WIDGTH = widgth

    glViewport (0, 0, WINDOW_WIDGTH, WINDOW_HEIGTH); 
    glMatrixMode (GL_PROJECTION);
    glLoadIdentity ();
    gluOrtho2D(0.0,WINDOW_WIDGTH,0.0,WINDOW_HEIGTH)

    
    glutPostRedisplay()

##  Um metodo que desenha as linhas e os pontos
 #  @brief desenha as retas que foram adicionadas a lista lines e depois as adicionam a lista drawedLines.
 #  utilizando o algoritmo contido na funcao LineCoordinate.intersect e calculado o ponto de interseccao, se existir,
 #  entre a reta sendo desenhada e todas as retas que ja foram desenhadas, retas contidas em drawedLines. Esse pontos de
 #  interseccao sao desenhados na tela
def displayFun():
    glClear(GL_COLOR_BUFFER_BIT)
    
    #Desenha poligonos ja criados    
    for i in range(0,len(Poligonos)):
        Polygon = Poligonos[i]
        glColor3f(Polygon.getRedComponent(), Polygon.getGreenComponent(), Polygon.getBlueComponent())
        gluTessBeginPolygon(tess, 0)
        gluTessBeginContour(tess)
        polygonPoints = Polygon.Points
        for j in range(0, len(polygonPoints)):
            pointCoordinate = polygonPoints[j].getCoordinate()
            pointCoordinate.append(0)
            gluTessVertex(tess, pointCoordinate, pointCoordinate)
        gluTessEndContour(tess)
        gluTessEndPolygon(tess)    

    gluTessEndContour(tess)

    #Desenha poligonos temporarios    
    for i in range(0,len(poligonosTemporario)):
        glColor3f(poligonosTemporario[i].getRedComponent(), poligonosTemporario[i].getGreenComponent(), poligonosTemporario[i].getBlueComponent())
        gluTessBeginPolygon(tess, 0)
        gluTessBeginContour(tess)
        polygonPoints = poligonosTemporario.pop().Points
        for j in range(0, len(polygonPoints)):
            pointCoordinate = polygonPoints[j].getCoordinate()
            pointCoordinate.append(0)
            gluTessVertex(tess, pointCoordinate, pointCoordinate)

        gluTessEndContour(tess)
        gluTessEndPolygon(tess)

    glPointSize(10.0)
    glBegin(GL_POINTS)    
    glColor3f(0.7, 0.7, 0.7)

    for nail in Nails:
        nailPoint = nail.getCoordinate()
        glVertex2f(nailPoint[0],WINDOW_HEIGTH - nailPoint[1])
    glEnd()        

    glLineWidth(1)        
    glBegin(GL_LINES)

    
    glColor3f(0.0, 0.0, 0.0)

    

    #Desenha reta no processo de criacao de um poligono
    for i in range(0,len(linesTemporario)):
        linhaTemporario = linesTemporario.pop()
        coordenadasBeginLinesTemporario = linhaTemporario.getCoordinateBegin()
        coordenadasEndLinesTemporario = linhaTemporario.getCoordinateEnd()
        glVertex2f(coordenadasBeginLinesTemporario[0],WINDOW_HEIGTH - coordenadasBeginLinesTemporario[1])
        glVertex2f(coordenadasEndLinesTemporario[0],WINDOW_HEIGTH - coordenadasEndLinesTemporario[1])
       
    glEnd()
    glLineWidth(1)
    glBegin(GL_LINES)

    for i in range(0, len(lines)):        
        coordinatesBegin = lines[i].getCoordinateBegin()
        coordinatesEnd = lines[i].getCoordinateEnd()
        glVertex2f(coordinatesBegin[0],WINDOW_HEIGTH - coordinatesBegin[1])
        glVertex2f(coordinatesEnd[0],WINDOW_HEIGTH - coordinatesEnd[1])         
    glEnd()
    glFlush()

##  Metodo que e executado em alguma acao com o mouse
 #  @param b botao que foi clicado
 #  @param s status do botao
 #  @param x coordenada x do curso do mouse no momento do clique
 #  @param y coordenada y do curso do mouse no momento do clique
def myMouse(b, s, x, y):
    global firstClick
    global firstClickCoordinates
    global clickInsidePolygon
    global movingPolygon
    if b == GLUT_LEFT_BUTTON:
        if s == GLUT_DOWN:
            #Test if the click was inside a polygon if the drawing wasnt started
            if firstClick:
                for i in range(0 , (len(Poligonos))):
                    poligono = Poligonos[i]
                    if poligono.insidePolygon(x,y):
                        polygonTranslateBaseCoordination.setCoordinate(x,y)
                        movingPolygon = poligono
                        clickInsidePolygon = True

            #Se um poligono nao esta sendo movido eu posso desenhar livremente
            if not clickInsidePolygon:
                if firstClick: #Primeiro clique
                    poligonoAtual = Polygon(x, y)
                    buildingPolygon.append(poligonoAtual)
                    coordinates = Coordinate(x, y)
                    points.append(coordinates)
                    firstClick = False
                    
                    
                else: # nao Primeiro Clique
                    poligonoAtual = buildingPolygon.pop()  
                    
                    if poligonoAtual.getBeginCoordinate().SameCoordinates(x,y):
                        coordinatesBegin = points.pop().getCoordinate()
                        beginCoordinatesActivePolygon = poligonoAtual.getBeginCoordinate().getCoordinate()
                        poligonoAtual.addLine(LineCoordinate(coordinatesBegin[0], coordinatesBegin[1], beginCoordinatesActivePolygon[0], beginCoordinatesActivePolygon[1]))
                        Poligonos.append(poligonoAtual)
                        poligonoAtual.setIndex(Poligonos.index(poligonoAtual))
                        del lines[:]
                        firstClick = True
                    else:
                        coordinatesBegin = points.pop().getCoordinate()
                        line = LineCoordinate(coordinatesBegin[0], coordinatesBegin[1], x, y)    
                        lines.append(line)
                        poligonoAtual.Points.append(Coordinate(x,y))
                        poligonoAtual.addLine(LineCoordinate(coordinatesBegin[0], coordinatesBegin[1], x, y))
                        coordinates = Coordinate(x, y)
                        points.append(coordinates)
                        buildingPolygon.append(poligonoAtual)
                        for j in range(0, len(Poligonos)):
                            poligonoCriado = Poligonos[j]
                    
            
        if s == GLUT_UP:
           
            ##  SE estava movendo um poligono finalizo o movimento 
            if clickInsidePolygon:
                inicialCoordinates = polygonTranslateBaseCoordination.getCoordinate()
                yTranslation = y - inicialCoordinates[1]
                xTranslation = x - inicialCoordinates[0]
                polygonTranslateBaseCoordination.setCoordinate(x,y)
                clickInsidePolygon = False
    
    ##  Adiciona e retira pregos            
    if b == GLUT_RIGHT_BUTTON:
        if s == GLUT_DOWN:
            clickInsideNail = False
            for nail in Nails:
                if nail.ClickIn(x,y):
                    nail.Remove()
                    clickInsideNail = True
            if not clickInsideNail:        
                nail = Nail(x,y)
                activeNail = False
                for i in range(0, len(Poligonos)):
                    poligono = Poligonos[i]
                    if poligono.insidePolygon(x,y):
                        nail.AddPolygon(poligono, i)
                        activeNail = True
                if activeNail:
                    if nail.IsNailToGround():
                        nail.ConfigureToGround() #se esse prego estiver pregado em um poligono e no chao, entao cofigura esse poligono para girar em torno do prego e nao se mover        
                    Nails.append(nail)        
                        
    glutPostRedisplay()        

##  movimento do mouse com o botao clicado, administra o movimento dos poligonos(rotacao e translacao)
def mouseMotion(x, y):
    global polygonTranslateBaseCoordination
    ##  SE o clique foi dentro de um poligono tento rodar e depois mover
    if clickInsidePolygon:
        inicialCoordinates = polygonTranslateBaseCoordination.getCoordinate()
        if movingPolygon.CanRotate():
            movingPolygon.rotatePolygon(x,y,inicialCoordinates[0],inicialCoordinates[1])
        else:
            if movingPolygon.CanTranslate():    
                yTranslation = y - inicialCoordinates[1]
                xTranslation = x - inicialCoordinates[0]
                movingPolygon.setTranslation(xTranslation,yTranslation)
            
        polygonTranslateBaseCoordination = Coordinate(x, y)
        glutPostRedisplay()
    
    else:
        # se o clique nao foi dentro de um poligono eu traco a reta para o desenho de um poligono que sera finalizado com o clique no ponto inicial
        if not firstClick:
            poligonoAtual = buildingPolygon[0] 
            if poligonoAtual.getBeginCoordinate().SameCoordinates(x,y):
                poligonosTemporario.append(poligonoAtual)
            else:
                coordinates = points[0].getCoordinate()
                line = LineCoordinate(coordinates[0], coordinates[1], x, y)
                linesTemporario.append(line)
            glutPostRedisplay()    


##  movimento do mouse sem esta clicando em nada, cuida do desenho do poligono
def mousePassiveMotion(x, y):
    if not firstClick:
            
        poligonoAtual = buildingPolygon[0]
        coordinates = points[0].getCoordinate() 
        if poligonoAtual.getBeginCoordinate().SameCoordinates(x,y):
            poligonosTemporario.append(poligonoAtual)
            line = LineCoordinate(coordinates[0], coordinates[1], x, y)
            linesTemporario.append(line)
        else:
            line = LineCoordinate(coordinates[0], coordinates[1], x, y)
            linesTemporario.append(line)



        glutPostRedisplay()


##  Callback para diretivas do tess que permite o desenho de poligonos nao convexos        

def tessBeginCallback(style):
    glBegin(style)

def tessEndCallback():
    glEnd()

def tessVertexCallback(vertex):
    glVertex2f(vertex[0],WINDOW_HEIGTH - vertex[1])    


if __name__ == '__main__':
    
    polygonTranslateBaseCoordination = Coordinate(0,0)
    movingPolygon = Polygon(0,0)
    movingGroup = Group(Polygon(0,0))
    tess = gluNewTess()

    gluTessCallback(tess, GLU_TESS_BEGIN, tessBeginCallback)
    gluTessCallback(tess, GLU_TESS_VERTEX, tessVertexCallback)
    gluTessCallback(tess, GLU_TESS_END, tessEndCallback)

    glutInit()
    glutInitWindowSize(WINDOW_WIDGTH,WINDOW_HEIGTH)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("Polygons")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutDisplayFunc(displayFun)
    glutReshapeFunc(myReshape)
    glutMouseFunc(myMouse)
    glutMotionFunc(mouseMotion)
    glutPassiveMotionFunc(mousePassiveMotion)

    initFun()
    glutMainLoop()
    gluDeleteTess(tess)