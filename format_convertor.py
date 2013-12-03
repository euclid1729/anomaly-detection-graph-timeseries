import os
from collections import defaultdict
class formatconvertor:
 #taking directory path as input, this directory contains time stamped graph edge list
 def initDirectory(self,directory_path):
  self.directory_path=directory_path
  file_list=os.listdir(directory_path)
  #list of edge list files in ascending order  
  file_list_sorted=sorted(file_list,key=lambda x:str(x).split('_')[0])
  return file_list_sorted
  
 #reading input file  
 def initFile(self,file_edge_graph):
  data=[(line.strip().split(' ')[0],line.strip().split(' ')[1]) for line in file(file_edge_graph)]
  return data

 #adjacency list creation
 def getAdjacencylist(self,data):
  alist = defaultdict(list) 
  for e in data:
   alist[int(e[0])].append(int(e[1]))  
   alist[int(e[1])].append(int(e[0]))
  return alist
 
 #calculate sum of node degrees, here adjacencyListGraph is a dictionary of list, each key corresponds to a node id and value to list of  neighbours
 def sumDegree(self,adjacencyListGraph):
  degreeList=[]
  for node in adjacencyListGraph.keys():
   degree_sum = len(adjacencyListGraph[node])
   degreeList.append((node,degree_sum)) # list of tuples, first value is vertex id and value is its degree 
  return degreeList
 
 def clustering_coefficient(self,adjacencyListGraph):
  coefficientList=[]
  for node in adjacencyListGraph.keys():
   node_neighbours=adjacencyListGraph[node]
   #finding neighbours that have edges between them 
   set_node_neighbors=set(node_neighbours)
   edges=sum([len(set_node_neighbors & set(adjacencyListGraph[v])) for v in node_neighbours])
   if len(node_neighbours)-1 == 0:
    coefficientList.append((node,0))
    continue
   # clustering coefficient  = 2 * number of egdes k between neighbors / k * (k-1)
   coefficientList.append((node,edges/float(len(node_neighbours)*(len(node_neighbours)-1)))) 
  return coefficientList
 
 def writeToDisk(self,degree_list,filename):
  f=open(filename,'w')
  for line in degree_list:
   print >>f,str(line[0]).rstrip()," ",str(line[1]).rstrip()
  f.close()
 
 def egoNet(self,adjacencyListGraph):
  egonetList=[]
  for node in adjacencyListGraph.keys():
   node_neighbours=adjacencyListGraph[node]
   #finding neighbours that have edges between them 
   set_node_neighbors=set(node_neighbours)
   edges=sum([len(set_node_neighbors & set(adjacencyListGraph[v])) for v in node_neighbours]) #each edge will be counted twice
   egonetList.append((node,edges+len(node_neighbours)))
  return egonetList
if __name__=="__main__":
 print "enter input directory name"
 dname=raw_input()
 print "enter output directory name"
 output_directory=raw_input()
 print " enter choice \n 1: degree count \n 2: clustering coeffieicent \n 3: ego net"
 choice=input()
 if not os.path.exists(output_directory):
  os.mkdir(output_directory)
 formatter=formatconvertor()
 fileList=formatter.initDirectory(dname)
 for f in fileList:
  f_data=formatter.initFile(dname+'/'+str(f))
  alist_file = formatter.getAdjacencylist(f_data)
  if choice == 1:
   degreeList= formatter.sumDegree(alist_file) #this is a list of tuples, [(vertex,degree),.....]
  elif choice == 2:
   degreeList= formatter.clustering_coefficient(alist_file)
  elif choice ==3:
   degreeList= formatter.egoNet(alist_file)
  formatter.writeToDisk(degreeList,output_directory+'/'+str(f))

