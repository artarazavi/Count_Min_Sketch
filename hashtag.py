import json

tweets_data_path = 'tweetstream.txt'

hashtag_list = []
hashtag_list_second_pass = []
k = 500

tweets_file = open(tweets_data_path, "r")
hashtag_counter = 0
counter = 0
for lines in tweets_file:
  counter+=1
  if counter % 2000000 == 0:
    print (counter)  
  '''
  if counter == 100000:
    break
  '''
  try:
      line = json.loads(lines)
      if line is not None:
        get_list = line.get('entities',{}).get('hashtags',{})

        for list_line in get_list:
          in_list = False
          hashtags = list_line.get('text',{})
          if hashtags:
            hashtags = hashtags.lower()
            hashtag_counter += 1

          #go through hastag counting list
          for hs in hashtag_list:
            if(hs.get('hashtag') == hashtags):
                hs['count'] += 1
                in_list = True        
          #if hashtag not in list of hashtags
          if(in_list == False):
            #is there is less than k items in the list append to list
            if(len(hashtag_list)<k):
              hashtag_list.append({'hashtag':hashtags, 'count':1})
            #if more than k items in the list decrement the count of everything by 1
            else:
              for idx,hs in enumerate(hashtag_list):
                hs['count'] -= 1

              hashtag_list[:] = [hs for hs in hashtag_list if hs['count'] > 0]
     
  except:
      continue

tweets_file.close()

print("1st pass done")
counter = 0
hashtag_list_second_pass = hashtag_list
tweets_file = open(tweets_data_path, "r")

#set all counts to zero
for hashtag in hashtag_list_second_pass:
  hashtag['count'] = 0

#2nd pass
for lines in tweets_file:
  counter+=1
  if counter % 2000000 == 0:
    print (counter)
  '''
  if counter == 100000:
    break
  '''
  try:
      line = json.loads(lines)
      if line is not None:
        get_list = line.get('entities',{}).get('hashtags',{})

        for list_line in get_list:
          in_list = False
          hashtags = list_line.get('text',{})
          if hashtags:
            hashtags = hashtags.lower()
          #go through hastag counting list
          for hs in hashtag_list_second_pass:
            if(hs.get('hashtag') == hashtags):
              hs['count'] += 1
  except:
      continue

print("hashtag_counter",hashtag_counter)
print("2nd pass done")
tweets_file.close()

#write to file
file = open("hashtag_output.txt","w")
for hashtag in hashtag_list_second_pass:
  if hashtag['count'] > hashtag_counter/k:
    file.write(hashtag.get('hashtag')+"\n")

file.close() 














