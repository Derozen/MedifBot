import argparse
import json
import os
import random
import string


def get_answers(responses) :
  a = responses[0]
  responses.remove(a)
  num = []
  idx = 1
  i=0
  query = ""
  ans = []
  print(len(a))
  while i < (len(a) - 1):
    #print(i)
    if a[i:i+2] == f'{idx})' :
      if query != "":
        num.append(query)
      query = ""
      i += 2
    elif a[i:i+2] == f'{idx+1})' :
      print(i)
      print(a[i:i+20])
      print("ok")
      responses.append(query)
      idx += 1
      i += 2
      query = ""
    else:
      j = a[i]
      query += j
      
      #print(query)
      #num[idx] = query
      i += 1
  #num = list(num.values())
  responses.append(query)
  for i in range(len(responses)) :
    ans = responses[i]
    if ans.startswith(" "):
      responses[i] = ans[1:]
    if ans.endswith(" "):
      responses[i] = ans[:-1]
#=========================================================================================
choices = []

def generate_id() :
  liste = list(string.ascii_lowercase + string.digits)
  mot = ""
  for i in range(10) :
    mot += random.choice(liste)
  if mot not in choices :
    choices.append(mot)
    return mot
  else :
    generate_id()
#=========================================================================================
def reformat_jsonl(input_file):
    output_file = input_file + "l"

    content_keys = ["content", "text"]
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        file_content = infile.read()  
        input = json.loads(file_content)
        input = input["intents"]
        for idx, line in enumerate(input):
            responses = line["responses"]
            patterns = line["patterns"]
            get_answers(responses)
            for pattern in patterns :
              data = {"prompt": pattern, "prompt_id":generate_id(), "messages":[{"content":pattern,"role":"user"},{"content":random.choice(responses),"role":"assistant"}]}
              outfile.write(json.dumps(data) + "\n")
        

            
            

           
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reformat a JSON file into a jsonl.")
    parser.add_argument("file", type=str, help="The input JSON file")

    args = parser.parse_args()
    reformat_jsonl(args.file)
