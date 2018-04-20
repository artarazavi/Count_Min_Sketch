from random import randint
import random
import json
from itertools import islice
import heapq
#((ax+b) mod p) mod m
#a != 0
#a and b from 0 to p-1
#m = w = 1000e
#d = 30
tweets_data_path = 'tweetstream.txt'
#build hash function
#large prime number
#from 1mil to 2mil 
p = 1500041#1999993
w = 2719
d = 30
hash_parameters=[]
for x in range(0, d):
  a = randint(1, p)
  b = randint(0, p)
  hash_parameters.append({'a': a, 'b': b})

#build hash table
r, c = d, w
#w, h = 5, w;
matrix = [[0 for x in range(c)] for y in range(r)] 

#stream data fromn file
min_heap = {}
tweets_file = open(tweets_data_path, "r")
m = 0
k=500
counter = 0
for lines in tweets_file:
  
  #print to command line
  counter+=1
  if counter % 2000000 == 0:
    print (counter)
  #streaming
  try:
      line = json.loads(lines)
      if line is not None:
        get_list = line.get('entities',{}).get('hashtags',{})
        for list_line in get_list:
          m += 1
          min_finder = []
          hashtags = (list_line.get('text',{})).lower()
          hashed_hashtag = hash(hashtags)

          for x in range (0,d):
            #((ax+b) mod p) mod m
            #ax+b
            axb = ((hash_parameters[x].get('a') * hashed_hashtag) + hash_parameters[x].get('b'))
            #((ax+b) mod p) mod m
            axb_modw = (axb % p) % w
            #set value in hash table to value + 1
            value = (matrix[x][axb_modw])+1
            matrix[x][axb_modw] = value
            #record into min value table
            min_finder.append(value)
          
          #extrct min value
          min_table_value = min(min_finder)

          #put into heap if greater than or equal to m/k
          if(min_table_value >= (m/k)):
            min_heap[hashtags] = min_table_value

          #get rid of all elements in the heap that have count less than m/k
          for key, value in min_heap.items():
            if(value < (m/k)):
              del min_heap[key]

  except:
      continue

#write to file
file = open("heap_output.txt","w")
for key, value in min_heap.items():
  file.write(key+"\n")
file.close()



