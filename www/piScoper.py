import tageater
import sys

class tagScope():
    def __init__(self, tag):
        self.name=tag.name
        self.tag=tag
        self.scope=[]
        self.children=[]

class PIscoper():
    def addHandler(self, typeof, handler):
        """
        Add handler to tag type typof
        """
        self.typedict[typeof].append(handler)
    def addScopeHandler(self, handler):
        self.scopeHandlers.append(handler)
    def addDescopeHandler(self, handler):
        self.descopeHandlers.append(handler)
    def addFulltagHandler(self, handler):
        """
        Add a handler for a tag and everyrthing in it from start to end, excluding PI and comments
        """
    def handle_startTag(self, tag):
        """
        Intenal startTag handler
        """
        if len(self.stack)>0:
            self.stack[-1].children.append(tagScope(tag))
            self.stack.append(self.stack[-1].children[-1])
        else:
            self.stack.append(tagScope(tag))
    def descope(self, scopedTag):
        for x in scopedTag.scope[::-1]:
            if(x==self.curscope[-1]):
               q=self.curscope.pop()
               for x in self.descopeHandlers:
                   x(q)
            else:
               raise(RuntimeError())
    def scope(self, pi):
        
        self.stack[-1].scope.append(pi)
        self.curscope.append(pi)
        for x in self.scopeHandlers:
            x(pi)
    

    def closedSkiped(self, name):
        skiped=[]
        while 1:
            x=self.stack.pop()
            self.descope(x)
            if x.name==name:
                break
            else:
                skiped.append(x.name)
        return skiped
    def handle_endTag(self, tag):
        try:
            x=self.closedSkiped(tag.name)
        except IndexError:
            print("Fatal Error: \n\tEnd Tag "+tag.name+"has no start tag", file=sys.stderr)
            exit()
        if len(x)!=0:
            print("Implicitly closed "+str(len(x))+" tag(s):", file=sys.stderr)
            for y in x:
                print("\t"+y, file=sys.stderr)
            print()

    def handle_cdata(self, tag):
        if len(self.stack)>0:
            self.stack[-1].children.append(tag)
    def handle_doctype(self, tag):
        if len(self.stack)>0:
            self.stack[-1].children.append(tag)
    
    def handle_text(self, tag):
        """
        Internal text handler
        """
        if len(self.stack)>0:
            self.stack[-1].children.append(tag)
    def handle_selfClosingTag(self, tag):
        """
        Internal text handler
        """
        if len(self.stack)>0:
            self.stack[-1].children.append(tag)
    def handle_pi(self, tag):
        """
        Internal PI handler
        """
        
        self.scope(tag)
    def handle_comment(self, tag):
        """
        Internal comment handler
        """
        pass
    def appenddat(self, x):
        self.parser.append(x)
    
    def handler(self, ret):
        """
        tag handler dispacher
        """
        for x in self.typedict[type(ret)]:
            x(ret)
        self.breaker=False
        

    def feed(self):
        self.parser.eat()
    def start(self):
        while self.breaker==False:
            self.breaker=True
            self.feed()

    def __init__(self):
        self.stack=[]
        self.breaker=False
        self.outdata=""
        self.typedict={tageater.startTag                 : [self.handle_startTag],
                       tageater.endTag                   : [self.handle_endTag],
                       tageater.selfClosingTag           : [self.handle_selfClosingTag],
                       tageater.textTag                  : [self.handle_text],
                       tageater.processingInstructionTag : [self.handle_pi],
                       tageater.commentTag               : [self.handle_comment],
                       tageater.cdataTag                 : [self.handle_cdata],
                       tageater.doctypeTag               : [self.handle_doctype],
                       }
        self.parser=tageater.Tageater(self.handler)
        self.curscope=[]
        self.scopeHandlers=[]
        self.descopeHandlers=[]



