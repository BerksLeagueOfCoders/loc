import piScoper
import tageater
import re
import collections
import functools
import sys
import os

class bind():
    def __init__(self, func, *args):
        self._func=func
        self._args=args
        
    def __call__(self, *args):
        y=list(self._args) + list(args)
        self._func(*y)
class templater():
    def __init__(self, string):
        self.outFile=""
        self.parser = piScoper.PIscoper()
        self.parser.appenddat(string)
        self.tcTag=None
        self.tcDepth=0
        self.pis=[]
        self.tcIntercept=[]
        self.intermode=False
        self.nameSearch=re.compile("^<([a-zA-Z\-]+)")
        self.parser.addDescopeHandler(self.piDescope)
        self.parser.addScopeHandler(self.piScope)
        self.parser.addHandler(tageater.startTag, self.tagStart)
        self.parser.addHandler(tageater.endTag, self.tagEnd)
        self.parser.addHandler(tageater.textTag, self.handleText)
        self.parser.addHandler(tageater.selfClosingTag, self.tagStartEnd)
        self.parser.addHandler(tageater.cdataTag, self.cdata)
        self.parser.addHandler(tageater.doctypeTag, self.doctype)
        self.tcFunctions={"REPLTAG" : [self.tcREPLTAGinit, self.tcREPLTAGexit]}#dictionary assosiating a tc command to an init and destructor
        self.tcFuncAssosiations=collections.defaultdict(list)#contains a dictionary assosiating a tag name to a tc funciton and a stack of [tcFunc, intermodeFunc, state]
        self.tcStack=[]#list of tc command destructors
        self.attSearch=x=re.compile("(\\S+)=[\"']?((?:.(?![\"']?\\s+(?:\\S+)=|[>\"']))+.)[\"']?")
    def tcREPLTAGinit(self, instruction):
        name=self.nameSearch.search(instruction).group(1)
        self.tcIntercept.append(name)
        self.tcFuncAssosiations[name].append([self.tcREPLTAG, self.tcREPLTAGinter, [instruction, ""]])
        self.tcStack.append(functools.partial(self.tcREPLTAGexit, name))
        
    def tcREPLTAGexit(self, name):
        self.tcIntercept.pop()
        self.tcFuncAssosiations[name].pop()
    def tcREPLTAGinter(self, tag):
        self.tcFuncAssosiations[self.tcTag.name][-1][2][1]+=tag.raw
    def repParse(self, com, inDict):
        out=""
        rem=re.search("<"+self.tcTag.name+">(.*?)</"+self.tcTag.name+">", com).group(1)
        left=re.search("(.*?)\$\{\{([a-zA-Z\-]+)\}\}(.*)", rem)
        while left!=None:
            out+=left.group(1)
            out+=inDict[left.group(2)]
            rem=left.group(3)
            left=re.search("(.*?)\$\{\{([a-zA-Z\-]+)\}\}(.*)", rem)
        out+=rem
        return out 
    def tcREPLTAG(self, dat):  
        atrDict=collections.defaultdict(str)
        pos=0
        res=self.attSearch.search(self.tcTag.raw, pos)
        while res!=None:
            atrDict[res.group(1)]=res.group(2)
            pos+=res.endpos
            res=self.attSearch.search(self.tcTag.raw, pos)
        atrDict[""]=dat[1]
        self.outFile+=self.repParse(dat[0], atrDict)
        dat[1]=""
    def intermodeHandler(self, tag):
        self.tcFuncAssosiations[self.tcTag.name][-1][1](tag)
    def tcHandle(self, instruction):
        x=re.search("([a-zA-Z]+)\s(.*)", instruction)
        if x==None:
            raise RuntimeError()

        function=x.group(1) 
        dat=x.group(2)
        
        target=function.upper()
        com=self.tcFunctions[target]
        com[0](dat)
        
    def intermodeExec(self):
        rep=self.tcFuncAssosiations[self.tcTag.name][-1]
        rep[0](rep[2])
        self.tcTag=None
        self.intermodeFile=""
        self.intermode=False
    def piScope(self, tag):
        self.pis.append(tag)
        if tag.target=="TC":
            self.tcHandle(tag.instruction)
        else:
            self.outFile+=tag.raw
    
    def piDescope(self, tag):
        if tag.target=="TC":
            self.tcStack.pop()()
    def tagStart(self, tag):
        """
        Process start tag.
        May trager intermode
        Will not triger intermodeExec
        """
        if self.intermode==False:
            if tag.name in self.tcIntercept:#if tag is special to tc
                self.tcTag=tag
                self.intermode=True#start intermode
                self.tcDepth+=1
                return
            
            else:
                self.outFile+=tag.raw#not special. add to raw
        else:
            if tag.name==self.tcTag.name:#increase depth so that closing tag wont end intermode
                self.tcDepth+=1
            self.intermodeHandler(tag)#handle intermode

    def tagStartEnd(self, tag):
        """
        Handles self closing tag.
        Will not trigger intermode
        May triger intermodeExec
        """
        if self.intermode==False:
            if tag.name in self.tcIntercept:
                self.tcTag=tag
                self.intermodeExec()
                return
            else:
                self.outFile+=tag.raw
        else:
            self.intermodeHandler(tag)

    def tagEnd(self, tag):
        """
        Handles closing tag
        Will not triger intermode
        May triger tcExec
        May be called from implicit tag close
        """
        if self.intermode==False:
            self.outFile+=tag.raw
        else:
            if tag.name==self.tcTag.name:
                self.tcDepth-=1

            if self.tcDepth==0:
                self.intermodeExec()
            else:
                self.intermodeHandler(tag)
    def cdata(self, tag):
        if self.intermode==False:
            self.outFile+=tag.raw
        else:
            self.intermodeHandler(tag)
    def doctype(self, tag):
        if self.intermode==False:
            self.outFile+=tag.raw
        else:
            raise RuntimeError("Encontered doctype during intermode")
    def handleText(self, tag):
        """
        Handles Text
        Will not triger intermode
        WIll not triger tcExec
        """
        if self.intermode==False:
            self.outFile+=tag.raw
        else:
            self.intermodeHandler(tag)
    


if __name__=="__main__":
    name=sys.argv[1]
    with open(name) as x:
        y=templater(x.read())

    y.parser.start()
    dirPath=os.path.dirname(os.path.abspath(name))
    outFile=os.path.splitext(os.path.basename(name))[0]+".php"
    outDir=os.path.join(dirPath, outFile)
    
    with open(outDir, "w") as x:
        x.write(y.outFile)

