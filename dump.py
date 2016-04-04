import sgf
import sys

data = open(sys.argv[1], 'rt').read()
game = sgf.SGF(data).parse()[0]
for i in xrange(5):
    print '\n'.join(''.join(p) for p in game.prior())
    print '\n%s\n' % ('#' * 19)
    game.next()
