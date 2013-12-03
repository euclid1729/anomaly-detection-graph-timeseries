import os,sys
from collections import defaultdict
import numpy as np
import time

class timeseries():
 
 #get list of all input files in a directory (in sorted by file name fashion)
 def initDirectory(self,directory_path):
  self.directory_path=directory_path
  file_list=os.listdir(directory_path)
  #list of edge list files in ascending order  
  file_list_sorted=sorted(file_list,key=lambda x:int(str(x).split('_')[0]))
  return file_list_sorted
  
 #this function accepts adjacency list of files (time stamped graph indgree information) and outputs vertex set
 def getAllVertices(self,fileList):
  vertex_set=set()
  for f in fileList:
   data_file=[int(line.split("   ")[0]) for line in file(self.directory_path+'/'+f)]
   vertex_set|=set(data_file)
  vertex_set=sorted(vertex_set)
  self.vertex_set_len=max(vertex_set)
  return self.vertex_set_len
  
 #reading input file  
 def initFile(self,file_edge_graph):
  data=[(int(line.strip().split('   ')[0]),float(line.strip().split('   ')[1])) for line in file(file_edge_graph)]
  return data
 
 #this function reads an input file and make a global vector of degrees, i.e. at a particular day, what was the degree count for all vertex
 def makeDegreeVector(self,listVertex):
  #list vertex is list of (vertexID,degree) tuple, but does not contain all vertices, i.e. nodes that will join later of have left 
  vector=[0]*self.vertex_set_len
  for line in listVertex:
   vector[int(line[0])]=int(line[1]) 
   #here line is a tuple, (vertexID,degree)
  return vector #vector is the degree count for each vertex on a particular day
  
 #this function will accept matrix containing 7 days feature information for all vertices and will compute correlation matrix
 def generateCorrelationMatrix(self,data_time_window):
  #data time window is a numpy array with number of rows =7 and number of columns = len(vertex_set)
  #cor_matrix=np.corrcoef(data_time_window,rowvar=0)
  size=data_time_window.shape[1] 
  cor_matrix=np.zeros(size * size).reshape(size,size)
  mean_vector=[]
  std_vector=[]
  data=data_time_window
  cov_matrix=np.cov(data_time_window,rowvar=0)
  #mean =np.mean(cov_matrix)
  #sd=np.std(cov_matrix)
  #cov_matrix = (cov_matrix - mean)/sd

  #finding mean and standard deviation of each column vector
  for col in xrange(data_time_window.shape[1]):
    mean_vector.append(np.mean(data[:,col]))
    std_vector.append(np.std(data[:,col]))
  #calculating correlation coefficient for each pair of column vectors
  for X1 in xrange(data.shape[1]):
   for X2 in xrange(data.shape[1]):
    if std_vector[X1]==0: #if the standard deviation is zero, then just put zero for all X2 corresponding to row X1
     cor_matrix[X1,:]=0
     break
    elif std_vector[X2]==0:
     cor_matrix[X1,X2]=0
    else:
     #X1_mu1_diff = X1-mean_vector[X1]
     #X2_mu2_diff = X2-mean_vector[X2]
     #covariance_X1X2 = np.mean(X1_mu1_diff.flatten().dot(X2_mu2_diff.flatten()))
     #cor_coeff= covariance_X1X2/float(std_vector[X1] * std_vector[X2])
     #cor_matrix[X1,X2]=cor_coeff
     cor_matrix[X1,X2]=cov_matrix[X1,X2]/float(std_vector[X1] * std_vector[X2])
  return cov_matrix

 #given a covariance matrix for a particular time window this function returns the principal eigen vector  
 def getPrincipalEigenVector(self,cor_matrix):
   evalues,evectors = np.linalg.eig(cor_matrix)
   return evectors[:,0]
 
 def convertGlobalEigenVector(self,prin_eigen,unique_vertices):
   #this function fills zero for vertices that haven't been seen during the seven day period
   eigen_vector=[0]*self.vertex_set_len
   for index in range(len(unique_vertices)):
    eigen_vector[unique_vertices[index]-1]=prin_eigen[index]
   return eigen_vector

 def generateWeekDataMatrix(self,week_data_list):
   unique_vertices = list(sorted(set([l[0] for day in week_data_list for l in day])))
   dimension = len(unique_vertices)
   matrix = np.zeros(7*dimension).reshape(7,dimension)
   day_index=0
   for day in week_data:
    for data in day: # data is a tuple (vertex-id,degree)
      vertex_index=unique_vertices.index(data[0])
      degree=data[1]
      matrix[day_index,vertex_index]=degree
    day_index+=1
   return matrix,unique_vertices

if __name__=="__main__":
 print "enter input director"
 input_dname=raw_input()
 print "enter output file name"
 filename=raw_input()
 start=time.time()
 output_file=open(filename,'w')
 obj=timeseries()
 fileList=obj.initDirectory(input_dname)
 vertex_set_len=obj.getAllVertices(fileList)
 counter=0
 counter1=0
 counter2=0
 eigen_avg=0
 flag=False
 flag1=False
 W_eigen=np.zeros(0)
 zscore_array = []
 week_data=[] #this list will hold list of list, each list containing tuples (vertex-id,degree), each list will represent a day's data
 for f in fileList:
  counter+=1
  #print counter
  file_data=obj.initFile(input_dname+"/"+f)
  #day_degree_vector=np.array(obj.makeDegreeVector(file_data)).reshape(1,vertex_set_len)
  week_data.append(file_data)
  #append the Window array with this day degree vector, Window W_degree will keep degree information for vertices for last 7 days
  '''if flag1:
   W_degree=np.vstack((W_degree,day_degree_vector))
  else:
   W_degree=day_degree_vector
   flag1=True
  '''
  counter1+=1
  if counter1 == 7:
   #transforming week_data into matrix of degree information for seven days, each column vector will represent 7 days degree info of a vertex
   W_degree,unique_vertices = obj.generateWeekDataMatrix(week_data)
   #calculating correlation matrix
   cor_matrix=obj.generateCorrelationMatrix(W_degree)
   #calculating principal eigen vector
   prin_eigen=obj.getPrincipalEigenVector(cor_matrix).real
   #prin_eigen=prin_eigen.reshape(vertex_set_len,1)
   prin_eigen=np.array(obj.convertGlobalEigenVector(prin_eigen,unique_vertices)).reshape(vertex_set_len,1)
   if flag:
    #flag is True => find z score
    zscore=1- prin_eigen.flatten().dot(eigen_avg.flatten())
    #print "counter = ",str(counter),"  zscore = ",str(zscore)
    output_file.write(str(counter)+" "+str(zscore)+"\n")
    zscore_array.append(zscore)
    del week_data[0]
    counter1=counter1-1
    W_eigen=np.delete(W_eigen,0,1) #deleting the first eigen vector, since window is moving forward by one in each iteration
    W_eigen=np.hstack((W_eigen,prin_eigen))
    eigen_avg=W_eigen.sum(axis=1)/float(7) #finding average of eigen vectors
   elif flag==False:
    if W_eigen.shape[0] !=0:
     W_eigen=np.hstack((W_eigen,prin_eigen))
    else:
     W_eigen=prin_eigen
    counter2+=1
    if counter2==7:
     eigen_avg=np.array(W_eigen.sum(axis=1)/float(7)).reshape(vertex_set_len,1)
     flag=True
   #deleting first row of W_degree, since window is sliding forward, after calculating W_degree for day 1,2,3,4,5,6,7 we need to get window
   #for day 2,3,4,5,6,7,8
    del week_data[0]
    counter1=counter1-1
med = np.median(zscore_array)
#print "median = ",str(med)
sd= np.std(zscore_array) 
#print "standard deviation = ",str(sd)
threshold_pos = med+2*sd
#output_file.write(str(threshold_pos)+"\n")
print "upper z threshold for anomaly detection  = ",str(threshold_pos)
counter=0
for z in zscore_array :
    if z > threshold_pos:
        counter+=1
        week_start=zscore_array.index(z)+7
        week_end=week_start+7
        #output_file.write("("+str(week_start)+","+str(week_end)+")"+" "+str(z)+"\n")
print "total number of anomalies detected = ",str(counter)
print "time elapsed = ",str(time.time()-start)
