import os
import os.path
import sgf

for (path, _, names) in os.walk('data/'):
    for name in names:
        fullname = os.path.join(path, name) 
        data = open(fullname, 'rt').read()
        try:
            game = sgf.SGF(data).parse()
            if len(game) != 1 or game[0].variations:
                print 'Has variations: ', fullname
        except sgf.SGFParseError, e:
            print e.error + ' on ' + fullname
