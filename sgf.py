import sys

class GameTree(object):
    def __init__(self, sequence=[], variations=[]):
        self.sequence = sequence
        self.variations = variations
        self.pos = 0
    def __repr__(self):
        return "GameTree(%s, %s)" % (str(self.sequence), str(self.variations))
    def reset(self):
        self.pos = 0
    def next(self):
        self.pos += 1
    def get(self):
        if 'B' in self.sequence[self.pos]:
            return self._parse('B', self.sequence[self.pos]['B'][0])
        elif 'W' in self.sequence[self.pos]:
            return self._parse('W', self.sequence[self.pos]['W'][0])
        else:
            return None
    def _parse(self, color, coords):
        return (color, self._convert(coords[0]), self._convert(coords[1]))
    def _convert(self, letter):
        return ord(letter) - ord('a')

class SGFParseError(Exception):
    def __init__(self, error):
        self.error = error

# Based on the EBNF from http://www.red-bean.com/sgf/sgf4.html
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
            raise SGFParseError("Expecting " + value)

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
        self._expect('(')
        self._ignore_space()
        sequence = self._sequence()
        self._ignore_space()
        variations = []
        while self.data[self.pos] == '(':
            variations.append(self._gametree())
            self._ignore_space()
        self._expect(')')
        return GameTree(sequence, variations)

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
                raise SGFParseError("Duplicate property " + key)
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

if __name__ == '__main__':
    data = open(sys.argv[1], "rt").read()
    sgf = SGF(data)
    print sgf.parse()

