from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

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

class Polygon(object):
    Points = []
    Lines = []
    BeginCoordinate = Coordinate(0, 0)
    finished = False
    draw = False
    _Nails = [] #Pregos do qual sou pai
    _redComponent = 0
    _greenComponent = 0
    _blueComponent = 0
    _xTranslation = 0
    _yTranslation = 0
    _insideAGroup = False
    _children = []
    _index = -1
    _rotationTranslation = Coordinate(0,0)
    _hasFather = False
    _rotationBaseCoordinates = Coordinate(0,0)

    def RemoveNail(self, nail):
        self._Nails.remove(nail)

    def setRotationCoordinates(self, coordinate):
        self._rotationBaseCoordinates = coordinate

    def getRotationCoordinates(self):
        return self._rotationBaseCoordinates    

    def HasFather(self, status):
        self._hasFather = status

    def RemoveChild(self, child):
        self._children.remove(child)    

    def DoesHasFather(self):
        return self._hasFather            

    def setNailPosition(self, x, y):
        self._nail = Coordinate(x,y)

    def AddChild(self, polygonToAdd):
        self._children.append(polygonToAdd)           

    def AddNail(self, nail):
        self._Nails.append(nail)

    def DeleteNail(self, nail):
        self._Nails[i].remove(x)

    def IsInsideAGroup(self):
        return self._insideAGroup

    def insideAGroup(self, status):
        self._insideAGroup = status

    def rotateGroup(self, rotationAngle, nailX, nailY):
        for point in self.Points:
            point.RotateCoordinate(rotationAngle, nailX, nailY)

        for line in self.Lines:
            line.RotateLine(rotationAngle, nailX, nailY)

        for child in self._children:
            child.rotateGroup(rotationAngle, nailX, nailY)

        for nail in self._Nails:
            nail.RotateNail(rotationAngle, nailX, nailY)            
     


    def rotatePolygon(self, x, y, baseX, baseY):

        rotationBaseCoordinates = self._rotationBaseCoordinates.getCoordinate()
        nailX = rotationBaseCoordinates[0]
        nailY = rotationBaseCoordinates[1]

        rotationAngle =  getRotateAngle(x,y,baseX,baseY, nailX, nailY)
        for point in self.Points:
            point.RotateCoordinate(rotationAngle, nailX, nailY)

        for line in self.Lines:
            line.RotateLine(rotationAngle, nailX, nailY)

        for child in self._children:
            child.rotateGroup(rotationAngle, nailX, nailY)

        for nail in self._Nails:
            nail.RotateNail(rotationAngle, nailX, nailY)            
     
    def setTranslation(self, x, y):
        for point in self.Points:
            point.TranslateCoordinate(x,y)

        for line in self.Lines:
            line.TranslateLine(x,y)

        for pol in self._children:
            pol.setTranslation(x,y)

        for nail in self._Nails:
            nail.TranslateNail(x,y)            

    def getXTranslation(self):
        return self._xTranslation

    def getYTranslation(self):
        return self._yTranslation    

    def addLine(self, L):
        self.Lines.append(L)

    def addPoint(self, P):
        self.Points.append(P)

    def insidePolygon(self, x,y):
        Colinear = False
        intersectionCount = 0
        infinityLine = LineCoordinate(x, y, WINDOW_WIDGTH, y)
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
                
    def setRandomColor(self):
        self.setRedComponent(random.uniform(0, 1))
        self.setGreenComponent(random.uniform(0, 1))
        self.setBlueComponent(random.uniform(0, 1))    

    def __init__(self, xBeg, yBeg):
       self.BeginCoordinate = Coordinate(xBeg, yBeg)
       self.Points = []
       self.Points.append(self.BeginCoordinate)
       self.Lines = []
       self._xTranslation = 0
       self._yTranslation = 0
       self.setRandomColor()
       self._insideAGroup = False
       self._children = []
       self._Nails = []

class Group(object):

    _Nails = []

    def __init__(self, nail):
        self._Nails = []
        self._Nails.append(nail)

    def AddNail(self, nail):
        self._Nails.append(nail)    

    def TranslateGroup(self, x, y):
        for nail in self._Nails:
            nail.TranslateNail(x,y)                    
        
class Nail(object):
    _coordinate = Coordinate(0,0)
    _PolygonFather = Polygon(0,0)
    _polygonChild = Polygon(0,0)
    _indexFather = -1

    def __init__(self, x, y):
        self._coordinate = Coordinate(x,y)
        self._polygonChild = []

    def ClickIn(self, x, y):
        return self._coordinate.SameCoordinates(x,y)    

    def getCoordinate(self):
        return self._coordinate.getCoordinate()   

    def Remove(self):
        self._PolygonFather.RemoveChild(self._polygonChild)
        self._polygonChild.HasFather(False)
        self._PolygonFather.RemoveNail(self)
        Nails.remove(self)

    def AddPolygon(self, polygon, index):
        if self._indexFather < 0: #Nao possui um poligono base
            self._indexFather = index
            self._PolygonFather = polygon   
            polygon.AddNail(self)

        else:    
            if index < self._indexFather:
                self._indexFather = index
                self._polygonChild = self._PolygonFather
                self._PolygonFather = polygon
                self._polygonChild.DeleteNail(self)

                polygon.AddNail(self)
                Polygon.AddChild(self._polygonChild)
                self._polygonChild.HasFather(True)
                self._polygonChild.setRotationCoordinates(self)


            else:
                self._PolygonFather.AddChild(polygon)
                self._polygonChild = polygon
                self._polygonChild.HasFather(True)
                self._polygonChild.setRotationCoordinates(self)
        
    def TranslateNail(self, x, y):
        self._coordinate.TranslateCoordinate(x,y)

    def RotateNail(self, angle, nailX, nailY):
        self._coordinate.RotateCoordinate(angle, nailX, nailY)

    
def determinate(P, Q, R):
    pPoints = P.getCoordinate()
    qPoints = Q.getCoordinate()
    rPoints = R.getCoordinate()

    positiveDiagonal = (qPoints[0] * rPoints[1]) + (rPoints[0] * pPoints[1]) + (pPoints[0] * qPoints[1])
    negativeDiagonal = (qPoints[0] * pPoints[1]) + (rPoints[0] * qPoints[1]) + (pPoints[0] * rPoints[1])

    return positiveDiagonal - negativeDiagonal

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

##  Um metodo que desenha as linhas e os pontos
 #  @brief desenha as retas que foram adicionadas a lista lines e depois as adicionam a lista drawedLines.
 #  utilizando o algoritmo contido na funcao LineCoordinate.intersect e calculado o ponto de interseccao, se existir,
 #  entre a reta sendo desenhada e todas as retas que ja foram desenhadas, retas contidas em drawedLines. Esse pontos de
 #  interseccao sao desenhados na tela
def displayFun():
    glClear(GL_COLOR_BUFFER_BIT)
    
    drawedLines = []
    
    
    
    
    #Desenha poligonos ja criados    
    for i in range(0,len(Poligonos)):
        Polygon = Poligonos[i]
        glColor3f(Polygon.getRedComponent(), Polygon.getGreenComponent(), Polygon.getBlueComponent())
        #glTranslatef(Polygon.getXTranslation(), Polygon.getYTranslation(), 0)
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

            
    glBegin(GL_LINES)

    glColor3f(0.0, 0.0, 0.0)

    

    #Desenha reta no processo de criacao de um poligono
    for i in range(0,len(linesTemporario)):
        linhaTemporario = linesTemporario.pop()
        coordenadasBeginLinesTemporario = linhaTemporario.getCoordinateBegin()
        coordenadasEndLinesTemporario = linhaTemporario.getCoordinateEnd()
        glVertex2f(coordenadasBeginLinesTemporario[0],WINDOW_HEIGTH - coordenadasBeginLinesTemporario[1])
        glVertex2f(coordenadasEndLinesTemporario[0],WINDOW_HEIGTH - coordenadasEndLinesTemporario[1])
       
        #drawedLines.append(linhaTemporario)
    glEnd()
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
                    
                    if poligonoAtual.BeginCoordinate.SameCoordinates(x,y):
                        coordinatesBegin = points.pop().getCoordinate()
                        beginCoordinatesActivePolygon = poligonoAtual.BeginCoordinate.getCoordinate()
                        poligonoAtual.addLine(LineCoordinate(coordinatesBegin[0], coordinatesBegin[1], beginCoordinatesActivePolygon[0], beginCoordinatesActivePolygon[1]))
                        Poligonos.append(poligonoAtual)
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
            
            if clickInsidePolygon:
                inicialCoordinates = polygonTranslateBaseCoordination.getCoordinate()
                yTranslation = y - inicialCoordinates[1]
                xTranslation = x - inicialCoordinates[0]
                polygonTranslateBaseCoordination.setCoordinate(x,y)
                clickInsidePolygon = False
                
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
                    Nails.append(nail)        
                        
    glutPostRedisplay()        

def mouseMotion(x, y):
    global polygonTranslateBaseCoordination
    if clickInsidePolygon:
        inicialCoordinates = polygonTranslateBaseCoordination.getCoordinate()
        if movingPolygon.DoesHasFather():
            movingPolygon.rotatePolygon(x,y,inicialCoordinates[0],inicialCoordinates[1])
        else:    
            yTranslation = y - inicialCoordinates[1]
            xTranslation = x - inicialCoordinates[0]
            movingPolygon.setTranslation(xTranslation,yTranslation)
            
        polygonTranslateBaseCoordination = Coordinate(x, y)
        glutPostRedisplay()
    
    else:
        if not firstClick:
            poligonoAtual = buildingPolygon[0] 
            if poligonoAtual.BeginCoordinate.SameCoordinates(x,y):
                poligonosTemporario.append(poligonoAtual)
            else:
                coordinates = points[0].getCoordinate()
                line = LineCoordinate(coordinates[0], coordinates[1], x, y)
                linesTemporario.append(line)
            glutPostRedisplay()    

def mousePassiveMotion(x, y):
    if not firstClick:
            
        poligonoAtual = buildingPolygon[0] 
        if poligonoAtual.BeginCoordinate.SameCoordinates(x,y):
            poligonosTemporario.append(poligonoAtual)
        else:
            coordinates = points[0].getCoordinate()
            line = LineCoordinate(coordinates[0], coordinates[1], x, y)
            linesTemporario.append(line)



        glutPostRedisplay()

def tessBeginCallback(style):
    glBegin(style)

def tessEndCallback():
    glEnd()

def tessVertexCallback(vertex):
    glVertex2f(vertex[0],WINDOW_HEIGTH - vertex[1])    


if __name__ == '__main__':
    
    #GLOBAL VARIABLES
    points = []
    lines = []
    buildingPolygon = []
    Poligonos = []
    Groups = []
    Nails = []
    firstClick = True
    linesTemporario =[]
    poligonosTemporario = []
    polygonTranslateBaseCoordination = Coordinate(0,0)
    clickInsidePolygon = False
    WINDOW_HEIGTH = 480
    WINDOW_WIDGTH = 640
    movingPolygon = Polygon(0,0)
    movingGroup = Group(Nail(0,0))
    margemDeErro = 2   #Margem de erro para a montagem do poligono
    #####################################################
    
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
    glutMouseFunc(myMouse)
    glutMotionFunc(mouseMotion)
    glutPassiveMotionFunc(mousePassiveMotion)

    initFun()
    glutMainLoop()
    gluDeleteTess(tess)