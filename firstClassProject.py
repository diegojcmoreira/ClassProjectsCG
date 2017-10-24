from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

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
    glBegin(GL_LINES)
    drawedLines = []
    for i in range(0,len(lines)):
        coordinatesBegin = lines[i].getCoordinateBegin()
        coordinatesEnd = lines[i].getCoordinateEnd()
        glVertex2f(coordinatesBegin[0],WINDOW_HEIGTH - coordinatesBegin[1])
        glVertex2f(coordinatesEnd[0],WINDOW_HEIGTH - coordinatesEnd[1])        
        for j in range(0, len(drawedLines)):
            PointOfIntersection = Coordinate(0, 0)
            if lines[i].intersect(drawedLines[j], PointOfIntersection):
                glEnd()
                drawPoint(PointOfIntersection.x, WINDOW_HEIGTH - PointOfIntersection.y)    
                glBegin(GL_LINES)    
        drawedLines.append(lines[i])
    glEnd()
    glFlush()

##  Metodo que e executado em alguma acao com o mouse
 #  @param b botao que foi clicado
 #  @param s status do botao
 #  @param x coordenada x do curso do mouse no momento do clique
 #  @param y coordenada y do curso do mouse no momento do clique
def myMouse(b, s, x, y):
    if b == GLUT_LEFT_BUTTON:
        if s == GLUT_DOWN:
            coordinates = Coordinate(x, y)
            points.append(coordinates)
            
            
        else:
            if s == GLUT_UP:
                coordinatesBegin = points.pop().getCoordinate()
                line = LineCoordinate(coordinatesBegin[0], coordinatesBegin[1], x, y)    
                lines.append(line)
                glutPostRedisplay()

if __name__ == '__main__':
    points = []
    lines = []
    WINDOW_HEIGTH = 480
    WINDOW_WIDGTH = 640
    glutInit()
    glutInitWindowSize(WINDOW_WIDGTH,WINDOW_HEIGTH)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("Draw Lines")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutDisplayFunc(displayFun)
    glutMouseFunc(myMouse)

    initFun()
    glutMainLoop()