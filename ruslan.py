#Tokens
INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = (
    'INTEGER','PLUS','MINUS','MUL','DIV','(',')','EOF'
)

#token class
class Token(object):
    def __init__(self,type,value):
        self.type = type
        self.value = value

    def __str__(self):
        """ String representation of the class instance
        
        Examples:
            Token(INTEGER,3)
            TOKEN(PLUS, '+')
    
        """

        return str(f'Token({self.type}, {self.value})')
    
    def __repr__(self):
        return self.__str__()


#lexer class

class Lexer(object):
    def __init__(self,text):
        self.text = text
        self.pointer = 0 #or self.pos
        self.current_char = self.text[0] #or self.pos
    
    def error(self):
        raise Exception('Invalid character')
    
    def is_end_input(self):
        return False if self.pointer < len(self.text) else True
       
    def advance(self):
        '''Advance the pointer and set the current_char '''
        self.pointer += 1
        if self.is_end_input():
            self.current_char = None
        else:
            self.current_char = self.text[self.pointer]

    def lex_whitespace(self):
        while not self.is_end_input() and self.current_char.isspace():
            self.advance()
    
    def lex_integer(self):
        ''' Return a (multidigit) integer consumed from the input
        as long as the input did not end and is a digit
        '''
        result = ''
        while not self.is_end_input() and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return result
    
    def tokenize(self):
        """ Lexical analyzer main method. Breaks a sentence into tokens, one at a time."""

        while not self.is_end_input(): 
            #detect the beginning of each token 
            #then call other methods if the token is of variable size
            if self.current_char.isspace():
                self.lex_whitespace()
                continue #do not need to return a token here
            if self.current_char.isdigit():
                return Token(INTEGER,self.lex_integer())
            if self.current_char == '+':
                self.advance()
                return Token(PLUS,'+')
            if self.current_char == '-':
                self.advance()
                return Token(MINUS,'-')
            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')
            
            self.error()
        
        return Token(EOF, None)



def test_token():
    pass

def test_lexer(text="10 + 5"):
    lexer = Lexer(text)
    ls = list()
    while True:
        token = lexer.tokenize()
        ls.append(token)
        print(token)
        print(ls)
        if token.type == 'EOF':
            break

    return str(ls)
        
    
    

if __name__== "__main__":
    text = "10 + 5"
    lexer = Lexer(text)

    test_lexer()