class SGFParseError(Exception):
    pass

class SGF(object):
    def __init__(self, data):
        self.data = data
        self.pos = 0

    def parse(self):
        try:
            self._collection()
            return True
        except SGFParseError:
            return False

    def _pop(self):
        value = self.data[self.pos]
        self.pos += 1
        return value

    def _ignore_space(self):
        while self.pos < len(self.data) and ord(self.data[self.pos]) <= 32:
            self.pos += 1

    def _collection(self):
        while True:
            self._ignore_space()
            if self.pos == len(self.data):
                return
            self._gametree()

    def _gametree(self):
        if self.data[self.pos] != '(':
            print "Expecting (" 
            raise SGFParseError()
        self.pos += 1
        self._ignore_space()
        self._sequence()
        self._ignore_space()
        while self.data[self.pos] == '(':
            self._gametree()
            self._ignore_space()
        if self.data[self.pos] != ')':
            print "Expecting )"
            raise SGFParseError()
        self.pos += 1

    def _sequence(self):
        while self.data[self.pos] == ';':
            self._node()

    def _node(self):
        if self._pop() != ';':
            print "Expecting ;"
            raise SGFParseError()
        self._ignore_space()
        node = {}
        while self.data[self.pos] not in ";)":
            k, v = self._property()
            node[k] = v
        print node

    def _property(self):
        prop = self._propident()
        self._ignore_space()
        values = []
        while self.data[self.pos] == '[':
            values.append(self._propvalue())
            self._ignore_space()
        return (prop, values)
    
    def _propident(self):
        ident = []
        while self.data[self.pos].isalpha():
            ident.append(self.data[self.pos])
            self.pos += 1
        return ''.join(ident)

    def _propvalue(self):
        if self.data[self.pos] != '[':
            print "Expecting ["
            raise SGFParseError()
        self.pos += 1
        value = []
        while self.data[self.pos] != ']':
            value.append(self._pop())
        self.pos += 1
        return ''.join(value)

data = open("game.sgf", "rt").read()
sgf = SGF(data)
sgf.parse()

