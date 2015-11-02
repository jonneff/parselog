(parse)jonneff (master *) parselog $   nosetests --with-coverage --cover-package=parselog
.......
Coverage.py warning: Module parselog was never imported.
Name                         Stmts   Miss  Cover   Missing
----------------------------------------------------------
app/__init__.py                  0      0   100%
app/parselog.py                 81     12    85%   79, 89-91, 101-102, 106-107, 115-118, 124
test/__init__.py                 0      0   100%
test/unit/__init__.py            0      0   100%
test/unit/parselog_test.py      58     11    81%   52, 59, 62-77
----------------------------------------------------------
TOTAL                          139     23    83%
----------------------------------------------------------------------
Ran 7 tests in 1.670s

OK