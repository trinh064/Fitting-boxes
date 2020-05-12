import copy
import pygame
import random

X=14
Y=12
def cprec(reca,recb):
    return reca.lx==recb.lx and reca.ly==recb.ly
def display(reclist):
    screen = [[0 for x in range(40)] for y in range(40)]
    for i in reclist:
        for dy in range(i.ly+1):
            y=i.origin[1]+dy
            for dx in range(i.lx+1):
                x=i.origin[0]+dx
                if(x==i.origin[0]+i.lx) or (y==i.origin[1]+i.ly) or(x==i.origin[0]) or (y==i.origin[1]) :
                    screen[x][y]=1
    for y in range(40):
        print("\n")
        for x in range(40):
                print(screen[x][y],end='')
                print("  ",end='')
    print("\n")
    return

def fancydisplay(reclist):
    win.fill((0,0,0))
    for rec in reclist:
        pygame.draw.rect(win, rec.color, (rec.origin[0]*30,rec.origin[1]*30, rec.lx*30, rec.ly*30))
    pygame.display.update()
    return

def compare(a,b):
    return a[0]==b[0] and a[1]==b[1]

def removerecpair(reclist,index):

    if index%2==0:
        reclist[:]=reclist[:index]+reclist[index+2:]
    else:
        reclist[:]=reclist[:index-1]+reclist[index+1:]

    return
def recpoint(rec):
        a,b,c,d=[[0,0],[0,0],[0,0],[0,0]]
        a[0]=rec.origin[0]
        a[1]=rec.origin[1]
        b[0]=rec.origin[0]+rec.lx
        b[1]=rec.origin[1]
        c[0]=rec.origin[0]
        c[1]=rec.origin[1]+rec.ly
        d[0]=rec.origin[0]+rec.lx
        d[1]=rec.origin[1]+rec.ly
        return [a,b,d,c]

def recpointin(rec):
        A=[]
        d=0.1
        for i in range(rec.ly):
            A+=[[rec.origin[0]+d,rec.origin[1]+i+d]]
        for i in range(rec.ly):
            A+=[[rec.origin[0]+rec.lx-d,rec.origin[1]+i+d]]
        for i in range(rec.lx):
            A+=[[rec.origin[0]+i+d,rec.origin[1]+d]]
        for i in range(rec.lx):
            A+=[[rec.origin[0]+i+d,rec.origin[1]+rec.ly-d]]
        return A

class rec:
    def __init__(self,origin,lx,ly):
        self.origin=origin
        self.lx=lx
        self.ly=ly
        self.color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    def area(self):
        return self.lx*self.ly
    def haspoint(self,point):
        '''
        for corner in recpoint(self):
            if compare(corner, point):
                return False
        '''

        return ((point[0]>self.origin[0]) and (point[0]<self.origin[0]+self.lx)) and ((point[1]>self.origin[1]) and (point[1]<self.origin[1]+self.ly))




class group:
    def __init__(self):
        self.frontier=[[0,0]]
        self.xmax=0
        self.ymax=0
        self.reclist=[]
#    def addhorizontal(self,rec):
#        for i in len(self.ymax):
    def check(self,rec):
        points=recpointin(rec)
        for rect in self.reclist:
        #    f=0
            for point in points:

                if rect.haspoint(point):
                    '''
                    f+=0
                    if f==0:
                    '''
                    #print("KAMEME ", point)
                    return False
        return True
    def add(self,rec):
        if rec.lx==0 and rec.ly==0:
            return False
        nx=rec.origin[0]+rec.lx
        ny=rec.origin[1]+rec.ly

        if self.check(rec) and (nx<=X) and (ny<=Y):

            if nx>self.xmax:
                self.xmax=nx
            if ny>self.ymax:
                self.ymax=ny
            self.reclist+=[rec]
            points=recpoint(rec)
            flag=[0,0,0,0]
            newfrontier=[]
            index=0
            for frontpoint in self.frontier:
                fl=0
                for i in range(4):
                    if not compare(frontpoint, points[i]):
                        fl+=1
                    else:
                        flag[i]+=1
                if fl==4:
                    newfrontier+=[frontpoint]
            for i in range(4):
                if flag[i]==0:
                    newfrontier+=[points[i]]
            self.frontier=newfrontier
            return True
        return False
    def realA(self):
        A=0
        for rec in self.reclist:
            A+=rec.area()
        return A
    def occA(self):
        A=self.xmax*self.ymax
        if A==0:
            A=1
        return A
    def value(self):
        rA=self.realA()
        oA=self.occA()
        numrec=len(self.reclist)/2
        return (int)(100* (X*Y -rA* ( (rA/oA)**(1) )))
    def printscreen(self,reclist):
        screen = [[0 for x in range(X+5)] for y in range(Y+5)]
        for i in reclist:
            for dy in range(i.ly+1):
                y=i.origin[1]+dy
                for dx in range(i.lx+1):
                    x=i.origin[0]+dx
                    if(x==i.origin[0]+i.lx) or (y==i.origin[1]+i.ly) or(x==i.origin[0]) or (y==i.origin[1]) :
                        screen[x][y]=1
        for y in range(Y+2):
            print("\n")
            for x in range(X+2):
                    print(screen[x][y],end='')
                    print("  ",end='')
        print("\n")
        return

class Node:
    def __init__(self,group,leftrecs):
        self.leftrecs=leftrecs
        self.group=group
class searchtree:
    def __init__(self,originalrecs):

        self.root=Node(group(),genreclist(originalrecs))
        self.searchfrontier={X*Y*100:[self.root]}
        self.goal=self.root
        self.best=X*Y*100
        self.c=0

    def expandnode(self,node):
        fl=False
        currentnodevalue=node.group.value()
        for i,rec in enumerate(node.leftrecs):
            f=False
            for j in range(i):
                f= f or cprec(rec,node.leftrecs[j])
            if not f:
                #print("#################################### New rec #############################")
                newleftrecs=copy.deepcopy(node.leftrecs)
                removerecpair(newleftrecs,i)
                for point in node.group.frontier:
                    #print("/////////////////////// New point //////////////////////////")
                    newrec=copy.deepcopy(rec)
                    newrec.origin[0]=point[0]
                    newrec.origin[1]=point[1]
                    newgroup=copy.deepcopy(node.group)
                    newnode=Node(newgroup,newleftrecs)
                    #print(len(newleftrecs))
                    ck=True
                    '''
                    for i,group in enumerate(self.trash):
                        for grec in group.reclist:
                            if(compare(newrec.origin,grec.origin) and newrec.lx==grec.lx and newrec.ly==grec.ly):
                                ck=False
                                #print(ck)
                    '''
                    if ck:
                        checkadd=newnode.group.add(newrec)
                        fl=fl or checkadd
                        #print("checkadd ",checkadd )
                        if checkadd:
                            key=newnode.group.value()
                            #print("Value ",key)
                            if (self.searchfrontier.get(key)==None):
                            #    print("Cant find")
                                self.searchfrontier[key]=[newnode]
                            else:
                            #    print("Found")
                                self.searchfrontier[key]+=[newnode]
                            #    print(self.searchfrontier[key])
                            #fancydisplay(newnode.group.reclist)
                            #pygame.time.delay(500)

                        #print (newnode.group.reclist)
                            #display(newnode.group.reclist)
                            #display(self.searchfrontier[key][0].group.reclist)
                            #newnode.group.printscreen(self.searchfrontier[key][0].group.reclist)
        self.searchfrontier[currentnodevalue]=self.searchfrontier[currentnodevalue][1:]
        if  len(self.searchfrontier[currentnodevalue])==0 :
            del self.searchfrontier[currentnodevalue]
        if not fl:
        #    print("CAT")
        #    self.trash+=[node.group]
            self.c=self.c+1
            print("Terminate ",self.c)
        return

    def search(self):

        while True:
            self.best=min(self.searchfrontier)
            #print("check1 ",self.best)
            while not (not self.searchfrontier[self.best][0].leftrecs):
                #print("check2",self.best)
                #print(len(self.searchfrontier[self.best][0].leftrecs))
                fancydisplay(self.searchfrontier[self.best][0].group.reclist)
                #pygame.time.delay(500)
                self.expandnode(self.searchfrontier[self.best][0])
                self.best=min(self.searchfrontier)

            if self.searchfrontier[self.best][0].group.realA()==self.searchfrontier[self.best][0].group.occA():
                self.goal=self.searchfrontier[self.best][0].group
                #print(self.searchfrontier[self.best][0].group.realA())
                #print(self.searchfrontier[self.best][0].group.occA())
                break;

            #self.trash+=[self.searchfrontier[self.best][0].group]
            #fancydisplay(self.trash[0].reclist)
            #pygame.time.delay(1000)
            '''
            if (self.goals.get(self.best)==None):
                self.goals[self.best]=[self.searchfrontier[self.best][0]]
            else:
                self.goals[self.best]+=[self.searchfrontier[self.best][0]]
            if self.searchfrontier[self.best][0].group.realA()==self.searchfrontier[self.best][0].group.occA():
                #print(self.searchfrontier[self.best][0].group.realA())
                #print(self.searchfrontier[self.best][0].group.occA())
                break;
            '''
            self.searchfrontier[self.best]=self.searchfrontier[self.best][1:]
            if  len(self.searchfrontier[self.best])==0 :
                del self.searchfrontier[self.best]


        return
        '''
        best=min(self.searchfrontier)
        print ("Best: ",best)
        if not self.searchfrontier[best][0].leftrecs:
            #insert goal node
            if (self.goals.get(best)==None):
                self.goals[best]=[self.searchfrontier[best][0]]
            else:
                self.goals[best]+=[self.searchfrontier[best][0]]
            #delete searchfrontier node
            self.searchfrontier[best]=self.searchfrontier[best][1:]
            if len(self.searchfrontier[best])==0 :
                del self.searchfrontier[best]
            if best%100 != 0 :
                self.search()
            return
        self.expandnode(self.searchfrontier[best][0])
        self.search()
        return
        '''
'''
A=group()
A.xmax=10
A.ymax=10
reclist=[]
reclist+=[rec([0,0],3,3),rec([3,3],4,2)]
#A.printscreen(reclist)
A.add(rec([0,0],3,3))
A.add(rec([0,3],3,2))
A.add(rec([3,3],3,2))
A.add(rec([3,0],2,3))
print(A.frontier)
#A.add(rec([6,0],1,5))
#print(A.add(rec([3,2],4,2)))
A.printscreen(A.reclist)

#a=rec([0,0],3,1)
#print(A.check(a))
#print(a.haspoint([2,3]))
#print(recpoint(a))
print(recpointin(rec([3,0],2,2)))
'''
def genreclist(ogrecs):
    list=[]
    for r in ogrecs:
        twin=rec([0,0],r.ly,r.lx)
        if twin.ly==twin.lx:
            twin.ly=0
            twin.lx=0
        twin.color=r.color
        list+=[r]
        list+=[twin]
    return list
pygame.init()
#print(recpointin(rec([1,2],4,5)))

#pygame.time.delay(10000)
#recs=[rec([0,0],3,4),rec([0,0],4,3),rec([0,0],5,2),rec([0,0],2,5),rec([0,0],2,2),rec([0,0],2,2),rec([0,0],1,7),rec([0,0],7,1),rec([0,0],3,6),rec([0,0],6,3),rec([0,0],2,1),rec([0,0],1,2),rec([0,0],3,1),rec([0,0],1,3),rec([0,0],3,3),rec([0,0],0,0),rec([0,0],2,3),rec([0,0],3,2),rec([0,0],1,5),rec([0,0],5,1),rec([0,0],1,5),rec([0,0],5,1)]
#recs=[rec([0,0],3,4),rec([0,0],5,2),rec([0,0],2,2),rec([0,0],1,7),rec([0,0],3,6),rec([0,0],2,1),rec([0,0],1,3),rec([0,0],3,3),rec([0,0],2,3),rec([0,0],1,5),rec([0,0],1,5)]
#recs=[rec([0,0],2,3),rec([0,0],3,3),rec([0,0],2,6),rec([0,0],1,4),rec([0,0],1,7),rec([0,0],4,4),rec([0,0],2,2),rec([0,0],1,3),rec([0,0],1,3),rec([0,0],2,4),rec([0,0],2,5),rec([0,0],1,7),rec([0,0],3,6),rec([0,0],2,3),rec([0,0],1,3),rec([0,0],1,2),rec([0,0],1,2),rec([0,0],1,3),rec([0,0],1,1),rec([0,0],1,2)]
recs=[rec([0,0],2,3),rec([0,0],3,3),rec([0,0],2,6),rec([0,0],1,4),rec([0,0],1,7),rec([0,0],4,4),rec([0,0],2,2),rec([0,0],1,3),rec([0,0],1,3),rec([0,0],2,4),rec([0,0],2,5),rec([0,0],1,7),rec([0,0],3,6),rec([0,0],2,3),rec([0,0],1,3),rec([0,0],1,2),rec([0,0],1,2),rec([0,0],1,3),rec([0,0],1,1),rec([0,0],1,2),rec([0,0],2,7),rec([0,0],2,6),rec([0,0],1,3),rec([0,0],1,9),rec([0,0],1,4)]
#recs=[rec([0,0],1,1),rec([0,0],1,1),rec([0,0],1,1),rec([0,0],1,1),rec([0,0],1,2),rec([0,0],1,2),rec([0,0],1,2),rec([0,0],1,2),rec([0,0],1,3),rec([0,0],1,3),rec([0,0],1,3),rec([0,0],1,3),rec([0,0],1,3),rec([0,0],1,4),rec([0,0],1,4),rec([0,0],2,3),rec([0,0],2,4),rec([0,0],2,4),rec([0,0],2,6),rec([0,0],3,3),rec([0,0],4,3)]
'''
1,1	4
1,2	4
1,3	5
1,4	2
2,3	1
2,4	2
2,6	1
3,3	1
3,4	1
'''
'''
2,3	3,3	2,6	1,4	1,7	4,4	2,2	1,3	1,3	2,6
2,5	1,7	3,6	2,3	1,3	1,2	1,2	1,3	1,1	1,2

2,7	2,6	1,3	1,9	1,4	1,3

'''
tree=searchtree(recs)

win = pygame.display.set_mode((1000,1000))
pygame.display.set_caption("Fitting boxes")
#print (tree.searchfrontier[100*X*Y][0].leftrecs[1].origin)
tree.search()
print ("FINALLY !!!!!")
#best=min(tree.goals)
#print(tree.searchfrontier)
#display( tree.goals[best][0].group.reclist)
#display( tree.goals[best][1].group.reclist)
random.seed()
#print(tree.goals[best])
run=True

#tree.goals[best][0].group.printscreen(tree.goals[best][0].group.reclist)
win.fill((0,0,0))
for rec in tree.goal.reclist:
    pygame.draw.rect(win, rec.color, (rec.origin[0]*30,rec.origin[1]*30, rec.lx*30, rec.ly*30))
pygame.display.update()
surface=pygame.display.get_surface()
pygame.image.save(surface,"abc.jpg")

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
