#!/usr/bin/env python

import yaml

from graphviz import Digraph

class Node:
    def __init__(self, name, label):
        self.name = name
        self.label = label

class Edge:
    def __init__(self, source, target):
        self.source = source
        self.target = target

unique_counter = 0
with open("data/example.yaml", 'r') as stream:
    try:
        doc = yaml.load(stream)

        dot = Digraph(comment='dependency graph')
        nodes = set()
        edges = set()
        for node in doc:
            nodes.add(Node(node, node))
            for dep in doc[node]['dependencies']:
                name = dep
                label = dep
                unique = dep.startswith('(') and dep.endswith(')')
                if unique:
                    label = name.lstrip('(').rstrip(')')
                    name = '{}-{}'.format(name, unique_counter)
                    unique_counter += 1

                nodes.add(Node(name, label))
                edges.add(Edge(node, name))

        for n in nodes:
            dot.node(n.name, n.label)
        for e in edges:
            dot.edge(e.source, e.target)

        print(dot.source)
        dot.render('out.gv', 'out', view=False)
    except yaml.YAMLError as err:
        print(err)
