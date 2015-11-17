from __future__ import division
import math, random
import json
from collections import defaultdict, Counter
from sklearn.metrics import jaccard_similarity_score
from flask import Flask, request
from flask import render_template
import pg8000
import sys, traceback

app = Flask(__name__, static_url_path='/static')


usr_obj = {}

data = [[[760, 801, 848, 895, 965], [733, 853, 939, 980, 1080], [714, 762, 817, 870, 918], [724, 802, 806, 871, 950]],
    [[12, 20, 34, 10, 23], [34, 24, 12, 45, 34], [13, 46, 2, 3, 6], [33, 43, 10, 19, 18]],
        [[67, 45, 78, 67, 68], [95, 54, 45, 68, 78], [13, 46, 2, 3, 6], [33, 43, 10, 19, 18]]]

@app.route('/user')
def users():
  usr_obj["uid"] = request.args.get('id')
  usr_obj["box"] = {}
  usr_obj["box"]["data"] = data[random.randint(0, 2)]

  usr_obj["box"]["outlier_data"] = [
                    [0, 644],
                    [4, 718],
                    [4, 951],
                    [4, 969]
                  ]
  return json.dumps(usr_obj)


def most_popular_new_interests(user_id, max_results=10):
  user_interests = users_interests[user_key.index(user_id)]
  suggestions = [(interest, frequency) 
                 for interest, frequency in popular_interests
                 if interest not in user_interests]
  return suggestions[:max_results]


def jaccard_similarity(v, w):
    return jaccard_similarity_score(v,w)


def make_user_interest_vector(user_interests):
    """given a list of interests, produce a vector whose i-th element is 1
    if unique_interests[i] is in the list, 0 otherwise"""
    return [1 if interest in user_interests else 0
            for interest in unique_interests]

def most_similar_users_to(user_id):
    try:
      print user_id
      conn = pg8000.connect(user="arvindram", password="", database="arvindram")
      cur = conn.cursor()
      cur.execute("SELECT u2, sim_index FROM sim_model where u1 = %s",(user_id,))
      similar_users = cur.fetchall()
      similar_users = [(user[0],float(user[1])) for user in similar_users]
      cur.close()
      pairs = [(other_user_id, similarity)                      # find other
             for other_user_id, similarity in similar_users     # users with nonzero 
             if user_id != other_user_id and similarity > 0]  # similarity

      # print pairs       
      return sorted(pairs,                                      # sort them
                  key=lambda (_, similarity): similarity,     # most similar
                  reverse=True)                               # first
    except:  
      traceback.print_exc()  
    
    


def user_based_suggestions(user_id, include_current_interests=False):
    # sum up the similarities
    suggestions = defaultdict(float)
    for other_user_id, similarity in most_similar_users_to(user_id):
        for interest in users_interests[user_key.index(other_user_id)]:
            suggestions[interest] += similarity

    # convert them to a sorted list
    suggestions = sorted(suggestions.items(),
                         key=lambda (_, weight): weight,
                         reverse=True)

    # and (maybe) exclude already-interests
    if include_current_interests:
        return suggestions
    else:
        return [(suggestion, weight) 
                for suggestion, weight in suggestions
                if suggestion not in users_interests[user_key.index(user_id)]]


@app.route('/popular')
def popular_places():
    user_index = int(request.args.get('user'))
    suggestions = [business_dict[s[0]] for s in most_popular_new_interests(users_interests[user_index])]
    return json.dumps(suggestions)

@app.route('/similarUsers')
def similar_users():
    user_index = int(request.args.get('user'))
    return json.dumps(most_similar_users_to(user_index))

@app.route('/')
def index():
  return app.send_static_file('index.html')

@app.route('/recommendations')
def recommendation():
    print "HERE"
    user_index = request.args.get('user')
    suggestions = []
    recommendations = []
    for s in most_popular_new_interests(user_index):
      if s[0] in business_dict and business_dict[s[0]] != "":
        suggestions.append({"title":business_dict[s[0]],"url":img_dict[s[0]]})

    for s in user_based_suggestions(user_index)[:20]:
      if s[0] in business_dict and business_dict[s[0]] != "":
        if {"title":business_dict[s[0]],"url":img_dict[s[0]]} not in suggestions:
          recommendations.append({"title":business_dict[s[0]],"url":img_dict[s[0]],"sim":round(s[1], 2)})
    return render_template('recommendation.html',recommendations=recommendations[:6], suggestions = suggestions[:6], user_id= user_index)        

if __name__ == '__main__':
  
  global user_dict                     
  user_dict = {}
  f = open("/Users/arvindram/Documents/DataScience/final_project/movies-py.csv", "r")
  line = f.readline()
  line = f.readline()
  
  while line:
    parts = line.split(",")
    user_id = parts[0]
    business_id = parts[1].replace('\n','').replace('\r','')
    if user_id in user_dict:
      user_dict[user_id].append(business_id)
    else:  
      user_dict[user_id] = [business_id] 
    line = f.readline()

  f.close()
  
  print "Reading movie titles..."
  global business_dict
  business_dict = {}
  global img_dict
  img_dict = {}
  f = open("/Users/arvindram/Documents/DataScience/final_project/movies-meta-py.csv", "r")
  line = f.readline()
  line = f.readline()

  while line:
    parts = line.split(",")
    
    business_id = parts[0]
    name = parts[1].replace('"','')
    url = parts[2].replace('\n','')
    business_dict[business_id] = name
    img_dict[business_id] = url
    line = f.readline()  

  f.close()
  
  print "Computing user interests..."
  global user_key
  global users_interests
  user_key = []
  users_interests = []

  for key, value in user_dict.iteritems():
    user_key.append(key)
    users_interests.append(value)

  print "Computing popular interests..."
  global popular_interests
  popular_interests = Counter(interest
                            for user_interests in users_interests
                            for interest in user_interests).most_common()
  
  print "Computing unique interests..."
  global unique_interests
  unique_interests = sorted(list({ interest 
                               for user_interests in users_interests
                               for interest in user_interests }))

  print "Starting recommendations engine..."                     
  app.run(debug=True)