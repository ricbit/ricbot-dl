import sys

class GameTree(object):
    def __init__(self):
        self.sequence = []
        self.variations = []
    def __repr__(self):
        return "GameTree(%s, %s)" % (str(self.sequence), str(self.variations))

class SGFParseError(Exception):
    pass

class SGF(object):
    def __init__(self, data):
        self.data = data
        self.pos = 0

    def parse(self):
        return self._collection()

    def _pop(self):
        value = self.data[self.pos]
        self.pos += 1
        return value

    def _expect(self, value):
        if self._pop() != value:
            print "Expecting " + value
            raise SGFParseError()

    def _ignore_space(self):
        while self.pos < len(self.data) and ord(self.data[self.pos]) <= 32:
            self.pos += 1

    def _collection(self):
        collection = []
        while True:
            self._ignore_space()
            if self.pos == len(self.data):
                break
            collection.append(self._gametree())
        return collection

    def _gametree(self):
        gametree = GameTree()
        self._expect('(')
        self._ignore_space()
        gametree.sequence.append(self._sequence())
        self._ignore_space()
        while self.data[self.pos] == '(':
            gametree.variations.append(self._gametree())
            self._ignore_space()
        self._expect(')')
        return gametree

    def _sequence(self):
        sequence = []
        while self.data[self.pos] == ';':
            sequence.append(self._node())
        return sequence

    def _node(self):
        self._expect(';')
        self._ignore_space()
        node = {}
        while self.data[self.pos] not in ";)(":
            key, value = self._property()
            if key in node:
                print "Duplicate property"
                raise SGFParseError()
            node[key] = value
        return node

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
        self._expect('[')
        value = []
        while self.data[self.pos] != ']':
            char = self._pop()
            if char == '\\':
                value.append(self._pop())
            else:
                value.append(char)
        self._expect(']')
        return ''.join(value)

data = open(sys.argv[1], "rt").read()
sgf = SGF(data)
print sgf.parse()

