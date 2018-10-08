import re
from enum import Enum
class EOFonCarret(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class tag():
    def __init__(self, tagType):
        self.tagType=tagType
        self.raw=""

class startTag(tag):
    def __init__(self, dat, name):
        self.name=name
        super().__init__(self)
        self.raw=dat
    def __str__(self):
        return "STAG: "+self.name

class endTag(tag):
    def __init__(self, dat, name):
        self.name=name
        super().__init__(self)
        self.raw=dat
    def __str__(self):
        return "ETAG: "+self.name

class selfClosingTag(tag):
    def __init__(self, dat, name):
        self.name=name
        super().__init__(self)
        self.raw=dat
    def __str__(self):
        return "SCTAG: "+self.name


class cdataTag(tag):
    def __init__(self, dat, contents):
        self.text=contents
        self.raw=dat
    def __str__(self):
        return "CDATA: "+self.text


class commentTag(tag):
    def __init__(self, dat):
        super().__init__(self)
        self.raw=dat
        self.comment=self.raw[4:-3]  #everything between <!-- and  -->  
    def __str__(self):
        return "COMMENT: "+self.comment

class processingInstructionTag(tag):
    def __init__(self, dat, target, instruc):
        self.target=target
        self.instruction=instruc
        super().__init__(self)
        self.raw=dat
    def __str__(self):
        return "PI: "+self.target+"  "+self.instruction

class doctypeTag(tag):
    def __init__(self, dat):
        super().__init__(self)
        self.raw=dat
    
class textTag(tag):
    def __init__(self, dat):
        super().__init__(self)
        self.raw=dat
    def __str__(self):
        return "TEXT: "+self.raw



class Tageater:
    def __init__(self, handler):
        self.dat=[]
        self.consumer=self.standard
        self.cur=""
        self.handler=handler
        self.stack=[]#for shared sub operations
        self.contin=False
        self.extradat=[""]
        self.extradatPos=0

    def extradatPushChar(self, char):
        if len(self.extradat)<=self.extradatPos:
            self.extradat.append("")
        self.extradat[self.extradatPos]+=char
        
    def extradatPush(self):
        self.extradatPushChar(self.dat[0])
    def extradatLim(self, length):
        return extradat[0:length]
    def append(self, dat):
        self.dat+=list(dat)

    
    def setConsumer(self, consumer):
        self.cur+=self.dat.pop(0)
        self.consumer=consumer
        self.contin=True
        
    def isEof(self):
        if len(self.dat)==0:
            self.stack.append(self.consumer)
            self.consumer=self.eof
            return True
        return False
    
    def eof(self):
        if len(self.dat)==0:
            return
        else:
            self.consumer=self.stack.pop()
            self.contin=True

    def eatws(self):
        
        if self.isEof():
            pass
        elif re.search(r"\s", self.dat[0])==None:
            self.consumer=self.stack.pop()
        else:
            self.cur+=self.dat.pop(0)
        self.contin=True

        
    def exclame(self):

        if self.isEof():
            return
        elif self.dat[0]=="-":
            self.setConsumer(self.commentStart)
        elif self.dat[0]=="[":
            self.setConsumer(self.cdataStartC)
        elif self.dat[0]=="D" or self.dat[0]=="d":
            self.setConsumer(self.doctypeO)

    def doctypeO(self):
        if self.isEof():
            return
        elif self.dat[0]=="O" or self.dat[0]=="o":
            self.setConsumer(self.doctypeC)
        
    def doctypeC(self):
        if self.isEof():
            return
        elif self.dat[0]=="C" or self.dat[0]=="c":
            self.setConsumer(self.doctypeT)
                
    def doctypeT(self):
        if self.isEof():
            return
        elif self.dat[0]=="T" or self.dat[0]=="t":
            self.setConsumer(self.doctypeY)

    def doctypeY(self):
        if self.isEof():
            return
        elif self.dat[0]=="Y" or self.dat[0]=="y":
            self.setConsumer(self.doctypeP)
        
    def doctypeP(self):
        if self.isEof():
            return
        elif self.dat[0]=="P" or self.dat[0]=="p":
            self.setConsumer(self.doctypeE)

    def doctypeE(self):
        if self.isEof():
            return
        elif self.dat[0]=="E" or self.dat[0]=="e":
            self.setConsumer(self.doctypeSPACE)

    def doctypeSPACE(self):
        if self.isEof():
            return
        elif self.dat[0]==" ":
            self.setConsumer(self.doctypeConsume)

        
    def doctypeConsume(self):
        if self.isEof():
            return
        elif self.dat[0]!=">":
            self.setConsumer(self.doctypeConsume)
        else:
            self.cur+=self.dat.pop(0)
            self.out(doctypeTag(self.cur))
            self.consumer=self.standard

    

    def cdataStartC(self):
        if self.isEof():
            return
        elif self.dat[0]=="C":

            self.setConsumer(self.cdataStartD)
    def cdataStartD(self):
        if self.isEof():
            return
        elif self.dat[0]=="D":
            self.setConsumer(self.cdataStartA1)
    def cdataStartA1(self):
        if self.isEof():
            return
        elif self.dat[0]=="A":
            self.setConsumer(self.cdataStartT)

    def cdataStartT(self):
        if self.isEof():
            return
        elif self.dat[0]=="T":
            self.setConsumer(self.cdataStartA2)
    def cdataStartA2(self):
        if self.isEof():
            return
        elif self.dat[0]=="A":
            self.setConsumer(self.cdataStartBRAK)

    def cdataStartBRAK(self):
        if self.isEof():
            return
        elif self.dat[0]=="[":
            self.setConsumer(self.cdataConsume)
   
    def cdataConsume(self):
        if self.isEof():
            return
        elif self.dat[0]!="]":
            self.extradatPush()
            self.setConsumer(self.cdataConsume)
        else:
            self.setConsumer(self.cdataEndBRAK)
    def cdataEndBRAK(self):
        if self.isEof():
            return
        elif self.dat[0]!="]":
            
            self.extradatPushChar("]")
            self.extradatPush()
            self.setConsumer(self.cdataConsume)
        else:
            self.setConsumer(self.cdataEnd)

    def cdataEnd(self):
        if self.isEof():
            return
        elif self.dat[0]!=">":
            self.extradatPushChar("]")
            self.extradatPushChar("]")
            self.extradatPush()
            self.setConsumer(self.cdataConsume)
        else:
            self.cur+=self.dat.pop(0)
            self.out(cdataTag(self.cur, *self.extradat))
            self.consumer=self.standard






    def endBracketTest(self):
        if self.isEof():
            return
        elif self.dat[0]==">":
            self.cur+=self.dat.pop(0)
            self.out(processingInstructionTag(self.cur, *self.extradat))
            self.consumer=self.standard
        else:
            self.extradatPushChar("?")
            self.extradatPush()
            self.setConsumer(self.pi)

    def pi(self):
        if self.isEof():
            return
        elif self.dat[0]=="?":
            
            self.setConsumer(self.endBracketTest)
        
        else:
            if self.extradatPos==0 and (re.search(r"\s", self.dat[0])==None):
                self.extradatPush()
            elif self.extradatPos==1:
                self.extradatPush()
            elif self.extradatPos==0:
                self.extradatPos+=1
                self.stack.append(self.consumer)
                self.consumer=self.eatws
                self.contin=True
                return
            else:
                self.extradatPos+=1
                
            self.cur+=self.dat.pop(0)
            self.contin=True
            
    def selfClosingTag(self):
        
        if self.isEof():
            return
        elif self.dat[0]==">":
            self.cur+=self.dat.pop(0)
            self.out(selfClosingTag(self.cur, *self.extradat))
            self.consumer=self.standard
        else:#not actually a self closing tag. return to default tag state
            self.setConsumer(self.tag)
        
    def tag(self):
        """
        state for regular and self closing tags
        """
        if self.isEof():
            return
        elif self.dat[0]==">":
            self.cur+=self.dat.pop(0)
            self.out(startTag(self.cur, *self.extradat))
            self.consumer=self.standard
        elif self.dat[0]=="/":
            self.setConsumer(self.selfClosingTag)
        else:
            if self.extradatPos==0 and (re.search(r"\s", self.dat[0])==None):
                self.extradatPush()
            else:
                self.extradatPos+=1
            self.cur+=self.dat.pop(0)
            self.contin=True

    def endtag(self):
        if self.isEof():
            return
        elif self.dat[0]==">":
            self.cur+=self.dat.pop(0)
            self.out(endTag(self.cur, *self.extradat))
            
            self.consumer=self.standard
            
        else:
            self.extradat[0]+=self.dat[0]
            self.cur+=self.dat.pop(0)
            self.contin=True
    def commentEnd2(self):
        if self.isEof():
            return
        elif self.dat[0]==">":
            self.cur+=self.dat.pop(0)
            self.out(commentTag(self.cur))
            self.consumer=self.standard
        else:
            self.setConsumer(self.comment)
            
    def commentEnd1(self):
        if self.isEof():
            return
        elif self.dat[0]=="-":
            self.setConsumer(self.commentEnd2)
        else:
            self.setConsumer(self.comment)
    def comment(self):
        if self.isEof():
            return
        elif self.dat[0]=="-":
            self.setConsumer(self.commentEnd1)
        else:
            self.cur+=self.dat.pop(0)
            self.contin=True
            
    
    def commentStart(self):
        if self.isEof():
            return
        elif self.dat[0]=="-":
            self.setConsumer(self.comment)
        else:
            raise RuntimeError()

    



    def afterBracet(self):
        """
        State for all tags starting with <
        """
        
        if self.isEof():
            return
        elif self.dat[0]=="!":
            self.setConsumer(self.exclame)
            
        elif self.dat[0]=="?":
            self.setConsumer(self.pi)
        elif self.dat[0]=="/":
            self.setConsumer(self.endtag)
        elif re.search("[a-zA-Z_]", self.dat[0])!=None:
            self.extradat[0]+=self.dat[0]
            self.setConsumer(self.tag)
        else:
            raise RuntimeError()
    
    def bracket(self):
        
        if self.isEof():
            return
        if self.dat[0]!="<":
            raise RuntimeError()
        else:
            self.setConsumer(self.afterBracet)
            
        

    def out(self, retType):
        self.extradat=[""]
        self.extradatPos=0
        self.cur=""
        self.handler(retType)
        
            
    def standard(self):
        
        if self.isEof():    
            return
        elif self.dat[0]!="<":
            self.cur+=self.dat.pop(0)
            self.contin=True
        else:
            
            self.consumer=self.bracket
            if self.cur=="":
                self.contin=True
            else:
                self.out(textTag(self.cur))
            
            
    def eat(self):
        self.consumer()
        while self.contin==True:
            self.contin=False
            self.consumer()
    


class eaerh():
    def __init__(self):
            self.x=Tageater(self.hand)
            self.x.append(open("htmlTest.html").read())
            self.tag="Start"
            self.count=0
    def hand(self, tag):
        self.tag=tag
    def eat(self):
        self.tag=None
        self.x.eat()
        
    
if __name__=="__main__":
    x=eaerh()
    while 1:

        x.eat()
        
        if x.tag==None:
            break
        print(x.tag)
        print(x.count)
        x.count+=1
