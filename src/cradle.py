import os
class cradle(object):
    def __init__(self, prjFile):
        self.prjFile = prjFile
        self.fp = open(self.prjFile)
        self.GetChar()
        self.SkipWhite()
        self.addOps = {'+': self.Add, '-': self.Subtract}
        self.mulOps = {'*': self.Multiply, '/': self.Divide}
        self.funcNames = ['printf']
    
    def GetChar(self):
        '''Get single character from input file'''
        self.Look = self.fp.read(1)
    
    def Error(self, msg):
        '''Report an error'''
        print('Error: %s.' % msg)
    
    def Abort(self, msg):
        '''Report an error and halt'''
        self.Error(msg)
        exit(0)

    def Expected(self, msg):
        '''Report what was expected'''
        self.Abort(msg + ' Expected')
    
    def IsAlpha(self):
        '''Recognizes an alpha character'''
        return self.Look.isalpha()
    
    def IsDigit(self):
        '''Recognizes a decimal character'''
        return self.Look.isdigit()
    
    def IsAlNum(self):
        '''Recognize an Alphanumeric'''
        return (self.IsAlpha() or self.IsDigit())
    
    def IsAddop(self):
        '''Recognize an Addop'''
        val = True if self.Look in ['+', '-'] else False
        return val
    
    def IsWhite(self):
        '''Recognize white space'''
        val = True if self.Look in [' ', '\t'] else False
        return val
    
    def SkipWhite(self):
        '''skip over leading white space'''
        while self.IsWhite():
            self.GetChar()
    
    def Match(self, x):
        '''match a specific i/p character'''
        if self.Look != x:
            self.Expected("'" + x + "'")
        else:
            self.GetChar()
            self.SkipWhite()
    
    def GetName(self):
        '''get an identifier'''
        Token = ''
        if not self.IsAlpha():
            self.Expected('Name')
        while self.IsAlNum():
            Token = Token + self.Look
            self.GetChar()
        return Token
    
    def GetNum(self):
        '''get a number'''
        val = ''
        if not self.IsDigit():
            self.Expected('Integer')
        while self.IsDigit():
            val = val + self.Look
            self.GetChar()
        return val
    
    def Emit(self, str):
        '''o/p a string with TAB'''
        print('\t%s' % str)
        
    def EmitLn(self, str):
        '''o/p a string with TAB and CRLF'''
        self.Emit(str)
#         WriteLn
    
    def Ident(self):
        '''Parse and translate an identifier'''
        name = self.GetName()
        if self.Look == '(':
            self.Match('(')
            self.Match(')')
            self.EmitLn('BSR %s' % name)
        else:
            self.EmitLn('MOVE %s(PC), D0' % name)
    
    def Factor(self):
        '''Parse and Translate a Math Factor'''
        if self.Look == '(':
            self.Match('(')
            self.Expression()
            self.Match(')')
        elif self.IsAlpha():
            self.Ident()
        else: 
            self.EmitLn('MOVE #%s, D0' % self.GetNum())

    def Multiply(self):
        '''Recognize and Translate Multiply'''
        self.Match('*')
        self.Factor()
        self.EmitLn('MULS (SP)+, D0')
    
    def Divide(self):
        '''Recognize and Translate Divide'''
        self.Match('/')
        self.Factor()
        self.EmitLn('MOVE (SP)+, D1')
        self.EmitLn('EXS.L D0')
        self.EmitLn('DIVS D1, D0')
        
    def Term(self):
        '''Parse and Translate a Math Term'''
        self.Factor()
        self.GetChar()
        while self.Look in ['*', '/']:
            self.EmitLn('MOVE D0, -(SP)')
            f = self.mulOps.get(self.Look, self.Expected)
            if f == self.Expected:
                f('Mulop')
            else:
                f()
#             self.GetChar()
            
    def Add(self):
        '''Recognize and Translate an Add'''
        self.Match('+')
        self.Term()
        self.EmitLn('ADD (SP)+, D0')
    
    def Subtract(self):
        '''Recognize and Translate a Subtract'''
        self.Match('-')
        self.Term()
        self.EmitLn('SUB (SP)+, D0')
        self.EmitLn('NEG D0')
    
    def Expression(self):
        '''Parse and Translate an Expression'''
#         self.Term()
#         self.GetChar()
        if self.IsAddop():
            self.EmitLn('CLR D0')
        else:
            self.Term()
        while self.IsAddop():
            self.EmitLn('MOVE D0, -(SP)')
            f = self.addOps.get(self.Look, self.Expected)
            if f == self.Expected:
                f('Addop')
            else:
                f()
#             self.GetChar()
    def Assignment(self):
        name = self.GetName()
        if name in self.funcNames:
            print('%s is a function' % name)
        else:
            print('%s is not a function' % name)
#        self.Match('=')
#        self.Expression()
#        self.EmitLn('LEA %s(PC), A0'% name)
#        self.EmitLn('MOVE D0, (A0)')
        
if __name__ == '__main__':
    pwd = os.getcwd()
    prjFile = os.path.join(pwd, 'hello.c')
    m = cradle(prjFile)
    m.Assignment()
