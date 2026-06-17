import pygame as py
from math import *
py.init()
R,Y=1365,765
screen=py.display.set_mode((R,Y),py.FULLSCREEN)
clock=py.time.Clock()
running=True
gravityY=0.01
py.display.set_caption("Tissu")
gravityX=0
Z=0
font=py.font.SysFont("Calibri",20,bold=True)
Bal=[];RES=[]
Rplace=[]
contrainte="R"
F=1;ADD=1
fps=120
Iteration=0
Espacement=20
def getgrid():
    grid=[[[]for i in range(ceil(R/Espacement))]for w in range(ceil(Y/Espacement))]
    for k,(i1,i2,d) in enumerate(RES):
        for b in [Bal[i1],Bal[i2]]:
            Px,Py=int(b.x//Espacement),int(b.y//Espacement)
            grid[Py][Px]+=[k]
    return grid
grid=getgrid()
class particle():
    def __init__(self,x,y,c,Z,move):
        self.x=x;self.y=y;self.c=c;self.Z=Z
        self.x1,self.y1=x,y
        self.immobile=move
    def depla(self):
        if self.immobile:
            self.x,self.y=self.x1,self.y1
            return
        self.x,self.y,self.x1,self.y1=(1+F)*self.x-F*self.x1+gravityX,self.y*(1+F)-F*self.y1+gravityY,self.x,self.y
    def contrainteR(self):
        if self.immobile:return
        self.x=min(max(0,self.x),R)
        self.y=min(max(0,self.y),Y-20)
def suppr(x,y,r):
    Px,Py=int(x//Espacement),int(y//Espacement)
    Rt=[]
    for dx in[-1,0,1]:
        for dy in[-1,0,1]:
            if 0<=Px+dx<R//Espacement and 0<=Py+dy<Y//Espacement:
                Rt+=grid[Py+dy][Px+dx]
    Rt=list(set(Rt))
    Rt=sorted(Rt,key=lambda i:0-i)
    for i in Rt:
        i1,i2,dd=RES[i]
        x1,y1=Bal[i1].x,Bal[i1].y
        x2,y2=Bal[i2].x,Bal[i2].y
        miX,maX,miY,maY=min(x1,x2)-r,max(x1,x2)+r,min(y1,y2)-r,max(y1,y2)+r
        if miX<x<maX and miY<y<maY:#boite englobante
            le=sqrt((x1-x2)**2+(y1-y2)**2);Nor=(-(y1-y2)/le,(x1-x2)/le);V=(x-x1,y-y1);Dis=V[0]*Nor[0]+V[1]*Nor[1];Nor2=((x1-x2)/le,(y1-y2)/le);Dec=V[0]*Nor2[0]+V[1]*Nor2[1]
            if abs(Dis)<=r and -le<Dec+r<2*r:
                RES.pop(i)
    return RES
T=60
Dist=9.5
D=(R-(T-1)*Dist)/2
def init():
    RES,Bal=[],[]
    for j in range(T):
        for i in range(T):
            Bal+=[particle(D+i*Dist,20+Dist*j,(255,255,255),i*T+j, (j==0 and (i%5==0 or i==T-1)) )]
            if j!=T-1:
                RES.append([i+T*j,i+T*j+T,Dist])
            if i!=T-1:
                RES.append([i+T*j,i+T*j+1,Dist])
    return Bal,RES
Bal,RES=init()
def pr():
    py.draw.rect(screen,(150,150,150),(0,Y-18,R,20))
    for l in RES:
        b0,b1=Bal[l[0]],Bal[l[1]]
        py.draw.line(screen,(100,100,100),(b0.x,b0.y),(b1.x,b1.y),2)
    screen.blit(font.render("FPS "+str(fps),True,(255,255,255)),(5,5))
    screen.blit(font.render("Nb liens "+str(len(RES)),True,(255,255,255)),(5,20))
    screen.blit(font.render("Nb part "+str(len(Bal)),True,(255,255,255)),(5,35))
    screen.blit(font.render("ESCAPE to close",True,(255,255,255)),(5,55))
def simulate():
    for b in Bal:
        b.depla()
    for i in range(len(RES)-1,-1,-1):
        i1,i2,d=RES[i]
        b1,b2=Bal[i1],Bal[i2]
        dx,dy=b2.x-b1.x,b2.y-b1.y
        Ad=sqrt(dx**2+dy**2)
        if Ad>2.7*d:
            RES.pop(i)
        else:
            Dd=-(d-Ad)/(2*Ad)
            Dx=Dd*dx;Dy=Dd*dy
            b1.x+=Dx;b1.y+=Dy
            b2.x-=Dx;b2.y-=Dy
    for b in Bal:
        b.contrainteR()
while running:
    xs,ys=py.mouse.get_pos()
    for event in py.event.get():
        if event.type==py.QUIT:
            running=False
        elif event.type==py.KEYDOWN:
            if event.key==py.K_SPACE:Bal,RES=init()
            if event.key==py.K_ESCAPE:running=False
    screen.fill("black")
    pr()
    if py.mouse.get_pressed()[0]:
        grid=getgrid()
        RES=suppr(xs,ys,5)
        py.draw.circle(screen,(255,0,0),(xs,ys),10,2)
    py.display.flip()
    simulate()
    clock.tick(60)
    fps=round(clock.get_fps(),1)
py.quit()