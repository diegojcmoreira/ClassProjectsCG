from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random






##  Uma Classe para representar uma coordenada no plano. 
 #  Reprensenta os pontos x e y de um plano com um metodo 
 #  para acessar as coordenadas como um array. 

class Coordinate(object):
    x = 0
    y = 0

    ##  Um Construtor da classe
     #  @param xx Coordenada X
     #  @param yy Coordenada Y
    def __init__(self, xx, yy):
        self.x = xx
        self.y = yy
    
    ##  Um membro para acessar as variaveis da classe.
     #  @param self objeto possuidor das coordenadas
     #  @return  
    def getCoordinate(self):
        coordinates = [self.x, self.y]
        return coordinates    

##  Uma Classe para representar um segmento de reta no plano. 
 #  Reprensenta os pontos x e y de inicio, x e y do final do segmento 
 #  

class LineCoordinate(object):
    ## Variaveis que representam o inicio do segmento de reta
     #

    XBegin = 0
    YBegin = 0
    
    ## Variaveis que representam o inicio do segmento de reta
     # 
    XEnd = 0
    YEnd = 0


    ##  Um Construtor da classe
     #  @param xBeg Coordenada X inicial do segmento de reta
     #  @param yBeg Coordenada Y inicial do segmento de reta
     #  @param xEn Coordenada X final do segmento de reta
     #  @param yEn Coordenada Y final do segmento de reta
    def __init__(self, xBeg, yBeg, xEn, yEn):
        self.XBegin = xBeg
        self.YBegin = yBeg
        self.XEnd = xEn
        self.YEnd = yEn

    ##  Um membro para acessar as variaveis da classe.
     #  @param self objeto possuidor das coordenadas
     #  @return Coordenadas iniciais do segmento de reta
    def getCoordinateBegin(self):
        coordinatesBegin = [self.XBegin, self.YBegin]
        return coordinatesBegin


    ##  Um membro para acessar as variaveis da classe.
     #  @param self objeto possuidor das coordenadas
     #  @return Coordenadas finais do segmento de reta
    def getCoordinateEnd(self):
        coordinatesEnd = [self.XEnd, self.YEnd]            
        return coordinatesEnd

    ##  Um membro para editar as variaveis da classe.
     #  @param self objeto possuidor das coordenadas
    def setCoordinateBegin(self):
        self.XBegin = coordinates[0]
        self.YBegin = coordinates[1]
    
    ##  Um membro para editar as variaveis da classe.
     #  @param self objeto possuidor das coordenadas            
    def setCoordinateEnd(self):
        self.XEnd = coordinates[0]
        self.YEnd = coordinates[1]

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
        
    def intersect(self, Line, PointOfIntersection):
        LineAx = self.XBegin - self.XEnd
        LineAy = self.YEnd - self.YBegin
        LineA = (self.XEnd * self.YBegin) - (self.XBegin * self.YEnd) 
        
        LineBCoordinateBegin = Line.getCoordinateBegin()
        LineBCoordinateEnd = Line.getCoordinateEnd()
        P = ((LineAy * LineBCoordinateBegin[0]) + (LineAx * LineBCoordinateBegin[1]) + LineA)
        R = ((LineAy * LineBCoordinateEnd[0]) + (LineAx * LineBCoordinateEnd[1]) + LineA)
        
        if ((P != 0) and (R != 0) and ((P * R) >= 0)) :
            return False
  
        LineBx = LineBCoordinateBegin[0] - LineBCoordinateEnd[0]
        LineBy = LineBCoordinateEnd[1] - LineBCoordinateBegin[1]
        LineB = (LineBCoordinateEnd[0] * LineBCoordinateBegin[1]) - (LineBCoordinateBegin[0] * LineBCoordinateEnd[1]) 
        
        Q = ((LineBy * self.XBegin) + (LineBx * self.YBegin) + LineB)
        S = ((LineBy * self.XEnd) + (LineBx * self.YEnd) + LineB)
        
        if ((Q != 0) and (S != 0) and ((Q * S) >= 0)) :
            return False        

        Denom = (LineAy * LineBx) - (LineBy * LineAx)
        if Denom == 0:
            print 'COLLINEAR'
            return False

        if Denom < 0:
            offset = -Denom / 2
        else:
            offset = Denom / 2      

        aux = (LineAx * LineB) - (LineBx * LineA)
        if aux < 0:
            PointOfIntersection.x = (aux - offset)/Denom
        else:
            PointOfIntersection.x = (aux + offset)/Denom

        aux = (LineBy * LineA) - (LineAy * LineB)
        if aux < 0:
            PointOfIntersection.y = (aux - offset)/Denom
        else:
            PointOfIntersection.y = (aux + offset)/Denom        

        return True

class Polygon(object):
    Points = []
    Lines = []
    BeginCoordinate = Coordinate(0, 0)
    finished = False
    draw = False
    _redComponent = 0
    _greenComponent = 0
    _blueComponent = 0

    

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
       self.setRandomColor()    

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
        #glColor3f(Poligonos[i].getRedComponent(), Poligonos[i].getGreenComponent(), Poligonos[i].getBlueComponent()) 
        glBegin(GL_POLYGON)
        polygonPoints = Poligonos[i].Points
        for j in range(0, len(polygonPoints)):
            pointCoordinate = polygonPoints[j].getCoordinate()
            print 'Coordenada desenhada : ' + str(pointCoordinate)
            glVertex2f(pointCoordinate[0], WINDOW_HEIGTH - pointCoordinate[1])

        glEnd()

    #Desenha poligonos temporarios    
    for i in range(0,len(poligonosTemporario)):
        #glColor3f(poligonosTemporario[i].getRedComponent(), poligonosTemporario[i].getGreenComponent(), poligonosTemporario[i].getBlueComponent())
        glBegin(GL_POLYGON)
        polygonPoints = poligonosTemporario.pop().Points
        for j in range(0, len(polygonPoints)):
            pointCoordinate = polygonPoints[j].getCoordinate()
            #print 'Coordenada desenhada : ' + str(pointCoordinate)
            glVertex2f(pointCoordinate[0], WINDOW_HEIGTH - pointCoordinate[1])

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
    if b == GLUT_LEFT_BUTTON:
        if s == GLUT_DOWN:
            if firstClick: #Primeiro clique
                poligonoAtual = Polygon(x, y)
                buildingPolygon.append(poligonoAtual)

                coordinates = Coordinate(x, y)
                points.append(coordinates)
                firstClick = False
                
                
                print 'Ponto Inicial: ' + str(poligonoAtual.Points[0].getCoordinate())
            else: # nao Primeiro Clique
                poligonoAtual = buildingPolygon.pop()  
                
                if [x, y] == poligonoAtual.BeginCoordinate.getCoordinate():
                    Poligonos.append(poligonoAtual)
                    points.pop()
                    del lines[:]
                    print 'Ponto Final: ' + str([x,y])
                    print len(buildingPolygon)
                    firstClick = True
                else:
                    coordinatesBegin = points.pop().getCoordinate()
                    line = LineCoordinate(coordinatesBegin[0], coordinatesBegin[1], x, y)    
                    lines.append(line)
                    poligonoAtual.Points.append(Coordinate(x,y))
                    coordinates = Coordinate(x, y)
                    points.append(coordinates)
                    buildingPolygon.append(poligonoAtual)
                    for j in range(0, len(Poligonos)):
                        poligonoCriado = Poligonos[j]
                        for i in range(0, len(poligonoCriado.Points)):
                            print 'Pontos: - ' + str(j) + ' - ' +  str(poligonoCriado.Points[i].getCoordinate())
                    print 'Ponto Intermediario: ' + str([x,y])
                glutPostRedisplay()    
            
                

def mouseMotion(x, y):
    if not firstClick:
        #print str([x, y]) + ' e = ' +str([PolAtual.BeginCoordinate.getCoordinate[0], PolAtual.BeginCoordinate.getCoordinate[1]])
        poligonoAtual = buildingPolygon[0] 
        if [x, y] == poligonoAtual.BeginCoordinate.getCoordinate():
            poligonosTemporario.append(poligonoAtual)
        else:
            coordinates = points[0].getCoordinate()
            line = LineCoordinate(coordinates[0], coordinates[1], x, y)
            linesTemporario.append(line)



        glutPostRedisplay()


if __name__ == '__main__':
    points = []
    lines = []
    buildingPolygon = []
    Poligonos = []
    firstClick = True
    linesTemporario =[]
    poligonosTemporario = []
    WINDOW_HEIGTH = 480
    WINDOW_WIDGTH = 640
    glutInit()
    glutInitWindowSize(WINDOW_WIDGTH,WINDOW_HEIGTH)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("Draw Lines")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutDisplayFunc(displayFun)
    glutMouseFunc(myMouse)
    glutPassiveMotionFunc(mouseMotion)

    initFun()
    glutMainLoop()