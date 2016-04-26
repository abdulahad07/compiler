import os

class sourceToSource(object):
    def __init__(self, prjFile):
        self.prjFile = prjFile
        self.fp = open(self.prjFile)
        self.indent = 0
        self.getChar()
        self.func = {'main': self.main, 'printf': self.printf, 'for': self.forLoop}
        self.dataTypes = ['int']
        self.loops = {}
        
    def getChar(self):
        '''read one character from i/p file'''
        self.look = self.fp.read(1)
    
    def error(self, msg):
        '''report an error'''
        print('Error: %s'% msg)
    
    def abort(self, msg):
        '''report an error and halt'''
        self.error(msg)
        exit(0)
    
    def expected(self, msg):
        '''report what was expected and halt'''
        self.abort(msg + ' Expected')
    
    def isWhite(self):
        return True if self.look in [' ', '\t', '\n'] else False

    def skipWhite(self):
        while self.isWhite():
            self.getChar()
    
    def isSpecial(self):
        if self.look == '{':
            self.indent += 1
        if self.look == '}':
            self.indent -= 1
        return True if self.look in [',', ';', '(', ')', '{', '}'] else False

    def skipSpecial(self):
        while self.isSpecial():
            self.getChar()

    def forLoop(self):
        self.getChar()
        self.match('(')
        string = ''
        while not self.match(')'):
            string += self.look
            self.getChar()
        condition = string.split(';')
        print condition
        print '%sfor(%s)' % (self.getIndent(), string)
        self.skipWhite()
        self.match('{')
        self.skipWhite()
        self.indent += 1
        self.run()

    def main(self):
        print "%sif __name__ == '__main__':" % (self.getIndent())
        self.run()

    def getIndent(self):
        ind = ''
        for i in range(self.indent):
            ind += ''.join('    ')
        return ind

    def printf(self):
        self.getChar()
        self.match('(')
        self.getChar()
        string = ''
        while not self.match("\""):
            string += self.look
            self.getChar()
        varList = []
        if not self.match(')'):
            expr = ''
            while not self.match(')'):
                expr += self.look
                self.getChar()
            varList = expr[1:].split(',')
            special = ['%']
            print '%sprint \'%s\' %s (%s)' % (self.getIndent(), string, special[0], ','.join(i for i in varList))#,varList)
        else:
            print '%sprint \'%s\'' % (self.getIndent(), string)
        self.run()

    def getName(self):
        '''get a name'''
        token = ''
        if not self.look.isalpha():
            self.expected('Name')
        while self.look.isalnum():
            token = token + self.look
            self.getChar()
        return token

    def match(self, c):
        if self.look == c:
            self.getChar()
            return True
        return False

    def run(self, skip=''):
        self.skipSpecial()
        self.skipWhite()
        self.skipSpecial()
        self.skipWhite()
        if self.look:
            name = self.getName()
            if self.func.has_key(name):
                f = self.func[name]
                f()
            if name in self.dataTypes:
                self.run()

if __name__ == '__main__':
    prjName = os.path.join(os.getcwd(), 'hello.c')
    r = sourceToSource(prjName)
    r.run()