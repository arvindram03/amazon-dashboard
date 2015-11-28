from __future__ import division
import math, random
import json
from collections import defaultdict, Counter
from sklearn.metrics import jaccard_similarity_score
from flask import Flask, request
from flask import render_template
import pg8000
import sys, traceback
from py2neo import Graph, authenticate, neo4j

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
    user_index = request.args.get('user')
    suggestions = []
    recommendations = []
    for s in most_popular_new_interests(user_index):
      if s[0] in business_dict and business_dict[s[0]] != "":
        suggestions.append({"title":business_dict[s[0]],"url":img_dict[s[0]]})

    for s in user_based_suggestions(user_index)[:50]:
      if s[0] in business_dict and business_dict[s[0]] != "":
        if {"title":business_dict[s[0]],"url":img_dict[s[0]]} not in suggestions:
          recommendations.append({"title":business_dict[s[0]],"url":img_dict[s[0]],"sim":round(s[1], 2)})
    return render_template('recommendation.html',recommendations=recommendations[:10], suggestions = suggestions[:10], user_id= user_index)

def get_recommendations(user_index):
    recommendations = []
    for s in user_based_suggestions(user_index)[:100]:
      if s[0] in business_dict and business_dict[s[0]] != "":
        recommendations.append(s[0])
    
    return recommendations

def get_actual(user_id):
    try:
      conn = pg8000.connect(user="arvindram", password="", database="arvindram")
      cur = conn.cursor()
      cur.execute("SELECT asin FROM movies where extract(year from to_timestamp(unixreviewtime)) > '2010' and reviewerid=%s",(user_id,))
      movies_cur = cur.fetchall()
      movies = [movie[0] for movie in movies_cur]
      cur.close()
      return movies
    except:  
      traceback.print_exc()  


def filter_by_price(recommendations, user_id):
  if user_id in price_dict:
    res = []
    (low, high) = price_dict[user_id]
    for r in recommendations:
      price = business_p_dict[r] 
      if price != 0 and low <= price <= high:
        res.append(r)
    return res    
  else:
    return recommendations  


def filter_by_path(recommendations, user_interests):
  # print len(recommendations),len(user_interests)
  authenticate("localhost:7474", "neo4j", "password")
  res = []
  g = Graph()
  min_len = -1
  MAX_PATH = 4
  for i in xrange(len(recommendations)):
    for j in xrange(len(user_interests)):
        query = "MATCH (from:Product { pid:'" + recommendations[i] + "' }), (to:Product { pid: '" + user_interests[j] + "'}) , path = shortestPath(from-[:TO*]->to ) RETURN path"
        results = g.cypher.execute(query)
        path_len = len(str(results).split(":TO")) - 1
        # print "PATH LEN",path_len
        if path_len == 0:
          continue
        if path_len < MAX_PATH:
          min_len = path_len
          break
        # if min_len == -1 or path_len < min_len:
        #     min_len = path_len
    # print "MIN LEN",min_len
     
    if min_len < MAX_PATH and min_len != -1:
        res.append(recommendations[i])
    min_len = -1

  return res

@app.route('/validate')
def validate():
  actual_count = 0
  filtered_count = 0
  for user_id, interests in user_dict.iteritems():
    actual = get_actual(user_id)
    recommendations = get_recommendations(user_id)
    actual_c = len(recommendations)    
    actual_count += actual_c
    # print "ACTUAL", actual_c
    if len(set(recommendations)) != 0:
      print len(set(recommendations).intersection(set(actual))) , len(set(recommendations)), len(set(recommendations).union(set(actual))), len(set(recommendations).intersection(set(actual))) / len(set(recommendations))

    reco_after_price = filter_by_price(recommendations, user_id)
    filtered_price_count = actual_c - len(reco_after_price)    
    # print "FILTERED_Price", filtered_price_count
    filtered_count += filtered_price_count

    if len(set(reco_after_price)) != 0:
      print len(set(reco_after_price).intersection(set(actual))) , len(set(reco_after_price)), len(set(reco_after_price).union(set(actual))), len(set(reco_after_price).intersection(set(actual))) / len(set(reco_after_price))  

    
    reco_after_path = filter_by_path(reco_after_price, users_interests[user_key.index(user_id)])
    filtered_path_count = len(reco_after_price) - len(reco_after_path)    
    # print "FILTERED_PATH", filtered_path_count
    filtered_count += filtered_path_count  
    
    # print actual_c, filtered_price_count, filtered_path_count
    if len(set(reco_after_path)) != 0:
      print len(set(reco_after_path).intersection(set(actual))) , len(set(reco_after_path)), len(set(reco_after_path).union(set(actual))), len(set(reco_after_path).intersection(set(actual))) / len(set(reco_after_path))
    

    try:
      conn = pg8000.connect(user="arvindram", password="", database="arvindram")
      for r in reco_after_path:
        cur = conn.cursor()
        cur.execute("INSERT INTO suggestions (user_id,movie) VALUES (%s, %s)",((user_id,r)))
        conn.commit()
        cur.close()

      conn.close()    
    except:
      traceback.print_exc()
      print "ERR"
      print sys.exc_info()[0]  
    print "\n"    
  print "T_ACTUAL",actual_count, "T_FILTERED", filtered_count   
  return "ok"

if __name__ == '__main__':
  global user_dict                     
  user_dict = {}
  f = open("/Users/arvindram/Documents/DataScience/final_project/movies-model-py.csv", "r")
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
  
  global price_dict                     
  price_dict = {}
  f = open("/Users/arvindram/amazon-dashboard/data_extract/reviewerid_prices_percentiles.csv", "r")
  line = f.readline()
  line = f.readline()
  
  while line:
    parts = line.split(",")
    user_id = parts[0]
    parts[4] = parts[4].replace('\n','')
    if parts[1] != parts[3] and int(parts[4]) >1:
      p_range = (float(parts[1]), float(parts[3]))
      price_dict[user_id] = p_range 
    line = f.readline()

  f.close()

  print "Reading movie titles..."
  global business_dict
  business_dict = {}
  global business_p_dict
  business_p_dict = {}
  global img_dict
  img_dict = {}
  f = open("/Users/arvindram/Documents/DataScience/final_project/movies-meta-py.csv", "r")
  line = f.readline()
  line = f.readline()

  while line:
    parts = line.split("\t")
    
    business_id = parts[0]
    name = parts[1].replace('"','')
    business_dict[business_id] = name

    if parts[2] == "":
      business_p_dict[business_id] = 0
    else:
      business_p_dict[business_id] = float(parts[2])

    url = parts[3].replace('\n','')
    
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