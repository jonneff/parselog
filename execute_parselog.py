#!/usr/bin/python -tt
"""

"""

from app.parselog import ParseLog
import json

def main():
  parse = ParseLog() 
  f = open('data/access.log','r')
  for line in f:
    result = parse.parse_line(line)
    if result:
      print(", ".join(str(i) for i in result))
  f.close()

if __name__ == '__main__':
  main()
