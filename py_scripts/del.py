#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

from __future__ import print_function 

import sys 
from py2neo import neo4j, node, rel 

graph_db = neo4j.GraphDatabaseService() 

class Person(object): 
    
    _root = graph_db.get_or_create_indexed_node("reference", 
       "contacts", "root") 
    
    @classmethod 
    def create(cls, name, *emails): 
        person_node, _ = graph_db.create(node(name=name), 
            rel(cls._root, "PERSON", 0)) 
        for email in emails: 
            graph_db.create(node(email=email), rel(cls._root, "EMAIL", 0),
                rel(person_node, "EMAIL", 0)) 
        return Person(person_node) 
    
    @classmethod 
    def get_all(cls): 
        return [Person(person.end_node) for person in 
            cls._root.match("PERSON")] 
    
    def __init__(self, node): 
        self._node = node 
    
    def __str__(self): 
        return self.name + "\n" + "\n".join("  &lt;{0}&gt;"
           .format(email) for email in self.emails) 
    
    @property 
    def name(self): 
        return self._node["name"] 
    
    @property 
    def emails(self): 
        return [rel.end_node["email"] for rel in 
           self._node.match("EMAIL")] 

if __name__ == "__main__": 
    if len(sys.argv) &lt; 2: 
        app = sys.argv[0] 
        print("Usage: {0} add &lt;name&gt; &lt;email&gt;
            [&lt;email&gt;...]".format(app)) 
        print("       {0} list".format(app)) 
        sys.exit() 
    method = sys.argv[1] 
    if method == "add": 
        print(Person.create(*sys.argv[2:])) 
    elif method == "list": 
        for person in Person.get_all(): 
            print(person) 
    else: 
print("Unknown command")