#!/usr/bin/python -tt
"""

"""

from app.parselog import ParseLog
import json
from multiprocessing.dummy import Pool as ThreadPool # easy multithreading
from multiprocessing.dummy import Process
from multiprocessing.dummy import Lock 

def main():
  parse = ParseLog() 
  f = open('data/access.log','r') # open file, read only
  pool = ThreadPool(8) # create pool of 8 threads.  IO bound so this speeds up in spite of GIL.
  pool.map(parse.parse_write, f) # apply parse_write() across the sequence f
  pool.close() # Prevents any more tasks from being submitted to the pool.
  # On Unix when process finishes but has not been joined it becomes a zombie.
  pool.join() # Wait for worker threads to exit.  
  """
  for line in f:
    result = parse.parse_line(line)
    if result:
      print(", ".join(str(i) for i in result))
  """
  f.close()

if __name__ == '__main__':
  main()
