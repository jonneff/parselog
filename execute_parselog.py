#!/usr/bin/python -tt
"""

"""

from app.parselog import ParseLog
import json

def main():
  parse = ParseLog() 
  f = open('data/access.log','r')
  fout = open('data/access.log.out', 'w')
  for line in f:
    result = parse.parse_line(line)
    if result:
      json.dump(result, fout)

if __name__ == '__main__':
  main()
