from __future__ import division
import math, random
import json
from collections import defaultdict, Counter
from sklearn.metrics import jaccard_similarity_score
from flask import Flask, request
from flask import render_template
​
app = Flask(__name__)
​
def most_popular_new_interests(user_interests, max_results=10):
  suggestions = [(interest, frequency) 
                 for interest, frequency in popular_interests
                 if interest not in user_interests]
  return suggestions[:max_results]
​
​
def jaccard_similarity(v, w):
    return jaccard_similarity_score(v,w)
​
​
def make_user_interest_vector(user_interests):
    """given a list of interests, produce a vector whose i-th element is 1
    if unique_interests[i] is in the list, 0 otherwise"""
    return [1 if interest in user_interests else 0
            for interest in unique_interests]
​
def most_similar_users_to(user_id):
    pairs = [(other_user_id, similarity)                      # find other
             for other_user_id, similarity in                 # users with
                enumerate(user_similarities[user_id])         # nonzero 
             if user_id != other_user_id and similarity > 0]  # similarity
​
    return sorted(pairs,                                      # sort them
                  key=lambda (_, similarity): similarity,     # most similar
                  reverse=True)                               # first
​
​
def user_based_suggestions(user_id, include_current_interests=False):
    # sum up the similarities
    suggestions = defaultdict(float)
    for other_user_id, similarity in most_similar_users_to(user_id):
        for interest in users_interests[other_user_id]:
            suggestions[interest] += similarity
​
    # convert them to a sorted list
    suggestions = sorted(suggestions.items(),
                         key=lambda (_, weight): weight,
                         reverse=True)
​
    # and (maybe) exclude already-interests
    if include_current_interests:
        return suggestions
    else:
        return [(suggestion, weight) 
                for suggestion, weight in suggestions
                if suggestion not in users_interests[user_id]]
​
​
@app.route('/popular')
def popular_places():
    user_index = int(request.args.get('user'))
    suggestions = [business_dict[s[0]] for s in most_popular_new_interests(users_interests[user_index])]
    return json.dumps(suggestions)
    # return json.dumps(request)
​
@app.route('/similarUsers')
def similar_users():
    user_index = int(request.args.get('user'))
    return json.dumps(most_similar_users_to(user_index))
​
​
@app.route('/recommendations')
def recommendation():
    user_index = int(request.args.get('user'))
    
    suggestions = [business_dict[s[0]] for s in most_popular_new_interests(users_interests[user_index])]
    recommendations = [business_dict[s[0]] for s in user_based_suggestions(user_index)[:20] if business_dict[s[0]] not in suggestions]
    return render_template('index.html',recommendations=recommendations[:6], suggestions = suggestions[:6], user_id= user_index)        
​
if __name__ == '__main__':
  global user_dict
  user_dict = {}
  f = open("/Users/arvindram/Documents/DataScience/MiniProject-3/la.csv", "r")
  line = f.readline()
  line = f.readline()
​
  while line:
    parts = line.split(",")
    user_id = parts[0]
    business_id = parts[1].replace('\n','').replace('\r','')
    if user_id in user_dict:
      user_dict[user_id].append(business_id)
    else:  
      user_dict[user_id] = [business_id] 
​
    line = f.readline()  
​
​
  f.close()
  
  global business_dict
  business_dict = {}
  f = open("/Users/arvindram/Documents/DataScience/MiniProject-3/la-business.csv", "r")
  line = f.readline()
  line = f.readline()
​
  while line:
    parts = line.split(",")
    business_id = parts[0]
    name = parts[1].replace('\n','').replace('\r','')
    business_dict[business_id] = name
    line = f.readline()  
​
  f.close()
​
  global users_interests
  users_interests = user_dict.values()
​
  global popular_interests 
  popular_interests = Counter(interest
                              for user_interests in users_interests
                              for interest in user_interests).most_common()
  global unique_interests
  unique_interests = sorted(list({ interest 
                                 for user_interests in users_interests
                                 for interest in user_interests }))
​
  global user_interest_matrix
  user_interest_matrix = map(make_user_interest_vector, users_interests)  
​
  global user_similarities
  user_similarities = [[jaccard_similarity(interest_vector_i, interest_vector_j)
                      for interest_vector_j in user_interest_matrix]
                     for interest_vector_i in user_interest_matrix]
​
  app.run(debug=True)
Add Comment Collapse