#!/usr/bin/env python3

import yaml

from graphviz import Digraph
from neo4j import GraphDatabase, basic_auth

class Node:
    def __init__(self, name, label, type, color):
        self.name = name
        self.label = label
        self.type = type
        self.color = color

class Edge:
    def __init__(self, source, target):
        self.source = source
        self.target = target


def process():
    unique_counter = 0
    nodes = set()
    edges = set()
    names = set()
    with open("data/example.yaml", 'r') as stream:
        try:
            doc = yaml.load(stream)
            for node in doc:
                color = 'white'
                type = 'Service'
                name = node
                if isinstance(doc[node], dict):
                    if 'type' in doc[node]:
                        if 'external' == doc[node]['type']:
                            type = 'ExternalService'
                        if 'infra' == doc[node]['type']:
                            type = 'Infrastructure'
                if name not in names:
                    names.add(name)
                    nodes.add(Node(name, name, type, color))
                for dep in doc[node]['dependencies']:
                    dname = ''
                    dlabel = ''
                    dtype = ''
                    if isinstance(dep, dict):
                        for k, v in dep.items():
                            if v == None:
                                dname = k
                                dlabel = k
                        if 'external' == dep['type']:
                            dtype = 'ExternalService'
                        if 'infra' == dep['type']:
                            dtype = 'Infrastructure'
                    else:
                        dname = dep
                        dlabel = dep
                        dtype = 'Service'
                    if 'db' in dname:
                        dtype = 'DB'
                    unique = dname.startswith('(') and dname.endswith(')')
                    if unique:
                        dlabel = dname.lstrip('(').rstrip(')')
                        dname = '{}-{}'.format(dname, unique_counter)
                        unique_counter += 1

                    if dname not in names:
                        names.add(dname)
                        nodes.add(Node(dname, dlabel, dtype, 'white'))
                    edges.add(Edge(name, dname))
        except yaml.YAMLError as err:
            print(err)
    return nodes, edges

def write_to_dot(nodes, edges):
    dot = Digraph(comment='dependency graph')
    for n in nodes:
        dot.node(n.name, n.label, style='filled',fillcolor=n.color)
    for e in edges:
        dot.edge(e.source, e.target)

    print(dot.source)
    dot.render('out.gv', 'out', view=False)


def normalize_4_neo4j(s):
    return s.replace('-', ' ').title().replace(' ', '').replace('(', '').replace(')', '')


def print_to_cypher(nodes, edges):
    for n in nodes:
        cname = normalize_4_neo4j(n.name)
        print("CREATE ({}:{} {{name: '{}'}})".format(cname, n.type, n.label))
    for e in edges:
        source = normalize_4_neo4j(e.source)
        target = normalize_4_neo4j(e.target)
        print("CREATE ({})-[:USES]->({})".format(source, target))


def write_to_neo4j(nodes, edges):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "admin"))
    session = driver.session()
    session.run("MATCH (n) DETACH DELETE n")

    query = ''
    for n in nodes:
        cname = normalize_4_neo4j(n.name)
        query += "CREATE ({}:{} {{name: '{}'}})".format(cname, n.type, n.label) + "\n"
    for e in edges:
        source = normalize_4_neo4j(e.source)
        target = normalize_4_neo4j(e.target)
        query += "CREATE ({})-[:USES]->({})".format(source, target) + "\n"

    session.run(query)
    session.close()

nodes, edges = process()

#write_to_dot(nodes, edges)
#print_to_cypher(nodes, edges)
write_to_neo4j(nodes, edges)