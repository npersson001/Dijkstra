#!/usr/bin/python
import pandas as pd
import sys

#generic graph class
class Graph:
    #initialize graph object
    def __init__(self):
        self.nodes = set()
        self.edges = {}

    #add nodes to graph set
    def add_node(self, value):
        self.nodes.add(value)
    
    #add edges and cost to dictionary of dictionaries 
    def add_edge(self, from_node, to_node, distance):
        self.edges.setdefault(from_node, {})[to_node] = distance

def dijkstra(g, start, end):
    #initialize the structures needed for the algorithm
    curNode = start
    curDist = 0
    visited = {}
    prevNodes = {}
    unvisited = {node: None for node in g.nodes}
    unvisited[curNode] = curDist

    #core of dijkstras algorithm
    while True:
        for adj, dist in g.edges[curNode].items():
            #only address nodes that are not already completely visited
            if(adj in unvisited):
                newDist = curDist + dist
            else:
                continue
            #update distance to node in unvisited dict
            if(unvisited[adj] is None or unvisited[adj] > newDist):
                unvisited[adj] =  newDist
                prevNodes[adj] = curNode
                
        #add evaluated node to the visited dict and update prevNode
        visited[curNode] = curDist
        
        #stop early if the visited node is the end node
        if(curNode == end):
            return curDist, prevNodes
        
        #delete evaluated node from unvisited dict and break if none left
        del unvisited[curNode]
        if not unvisited: break
            
        #select smallest dist available
        pos = [node for node in unvisited.items() if node[1]]
        curNode, curDist = sorted(pos, key = lambda x: x[1])[0]
        
def reconstructPath(prevNodes, start, end):
    #initialize variables for reconstruction
    route = []
    curNode = end
    
    #loop through to reconstruct the path from end to start
    while True:
        route.append(curNode)
        if(curNode == start):
            route.reverse()
            return route
        curNode = prevNodes[curNode]

def findShortest(start, end, fileName):
    #create graph and get information from csv file
    g = Graph()
    dataframe = pd.read_csv(fileName, header=None)

    #add nodes to graph from csv file
    for i, row in dataframe.iterrows():
        g.add_node(i + 1)

    #add edges to graph from csv file
    for i, row in dataframe.iterrows():
        for j, col in enumerate(row):
            if(col > 0):
                g.add_edge(i+1, j+1, col)
            
    #check if graph actually filled
    if(len(g.edges) == 0):
        print "file path not found, exiting program"
        sys.exit()
    
    #call dijkstras algorithm function
    distance, prevNodes = dijkstra(g, start, end)
    
    #put visited in format project requested [x1, x2, ..., xn]
    route = reconstructPath(prevNodes, start, end)
    
    #visited, path = dijkstra(g, start, end)
    return route, distance

#note: first node starts at 1
route, distance = findShortest(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
print "distance =", distance
print "route =", route