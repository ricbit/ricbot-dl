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
        if self._pop() != '(':
            print "Expecting (" 
            raise SGFParseError()
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
            key, value = self._property()
            if key in node:
                print "Duplicate property"
                raise SGFParseError()
            node[key] = value
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
            ident.append(self._pop())
        return ''.join(ident)

    def _propvalue(self):
        if self._pop() != '[':
            print "Expecting ["
            raise SGFParseError()
        value = []
        while self.data[self.pos] != ']':
            value.append(self._pop())
        if self._pop() != ']':
            print "Expecting ]"
            raise SGFParseError()
        return ''.join(value)

data = open("game.sgf", "rt").read()
sgf = SGF(data)
sgf.parse()

