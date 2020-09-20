'''
Author: Wenkai Zheng
Email: zwkzmj@gmail.com
Purpose: Graph analyse and visulization through a social network.
'''
import networkx as nx
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import community as c
import operator
import numpy as np

'''
This funtion help return the paramter for drawing each community
the top6 nodes will be colored with pink other will be red
collect the path for then in edge list 
'''
def construct_new_graph2(vector):
    global edges
    color_map = []
    rc = []
    for i in range (0,6):
        rc.append(vector[i][0])
        color_map.append('red')
    for j in range(6,len(vector)):
        rc.append(vector[j][0])
        color_map.append('pink')
        

    rv = []
    for node in rc:
        for edge in edges:
            if (edge[0] == node and edge[1] in rc) or ( edge[1] ==node and edge[0] in rc):
                rv.append(edge)
    
    
    return rc,rv,color_map

'''
Data preprocess
clean the missing data 
calculate the age
simplified the job 
return the edge list 
'''
def data_preprocess():
    nodes = []
    edges = []
    with open('quakers_nodelist.csv', 'r') as node:                
         count = 0
         for n in csv.reader(node):
            if count == 0:
                count +=1
                continue
            else: 
                if n[0] == '' or n[1] == '' or n[2] == '' or n[3] =='' or n[4] == '':
                    pass
                else: nodes.append(n)
    for data in nodes:
       
        if (data[1].find('Quaker ')!=-1):
            job[data[0]] = data[1].replace('Quaker ','')
        
        else:
            job[data[0]] = data[1]
        
        gender[data[0]] = data[2]
        age[data[0]] = int(data[4])- int(data[3])
        names_map[data[0]] = data[0]
        names.append(data[0])                
    #print(names)
    with open('quakers_edgelist.csv', 'r') as edge: 
        edges = []
        count = 0
        for e in csv.reader(edge):
            if count ==0:
                count +=1
                continue
            if e[0] not in names or e[1] not in names:
               pass
            else:
                edges.append(tuple(e))
    return edges

'''
Draw the dot plot for age and degree
'''
def degree_age(Graph):
    degree = [Graph.degree(n) for n in Graph.nodes()]
   # sort_age = sorted(age.items(),key = lambda k:k[1])
    #print(age)
    x = [Graph.nodes[node]['age'] for node in Graph.nodes() ]
    y = [d for d in degree]
    ax = plt.gca()
    ax.set_title('Dot plot for degree and age')
    plt.scatter(x,y,s=1,color=(1,0,0))
    plt.show()
'''
Draw the box plot for gender and degree
'''
def degree_gender(Graph):
    #degree = [Graph.degree(n) for n in Graph.nodes()]
    male_degree = [Graph.degree(n)  for n in Graph.nodes()  if Graph.nodes[n]['gender'] == 'male']
    female_degree = [Graph.degree(n)  for n in Graph.nodes() if Graph.nodes[n]['gender'] == 'female']
    ax = plt.gca()
    ax.set_title('Box plot for degree and gender')
    labels = 'male','female'
    plt.boxplot([male_degree,female_degree],labels = labels,vert=False,showmeans = True)
    plt.show()
'''
Draw the box plot for job and degree
'''
def degree_job(Graph):
    one = job_rank[0][0]
    two = job_rank[1][0]
    three = job_rank[2][0]
    four = job_rank[3][0]
    five = job_rank[4][0]

    first = [Graph.degree(n)  for n in Graph.nodes()  if Graph.nodes[n]['job'] == one]
    second = [Graph.degree(n)  for n in Graph.nodes() if Graph.nodes[n]['job'] == two]
    third = [Graph.degree(n)  for n in Graph.nodes() if Graph.nodes[n]['job'] == three]
    fourth = [Graph.degree(n)  for n in Graph.nodes() if Graph.nodes[n]['job'] == four]
    fifth = [Graph.degree(n)  for n in Graph.nodes() if Graph.nodes[n]['job'] == five]
    ax = plt.gca()
    ax.set_title('Box plot for degree and job')
    labels = one,two,three,four,five
    plt.boxplot([first,second,third,fourth,fifth],labels = labels,vert=False,showmeans = True)
    plt.show()
'''
Draw the bar chart for age, gender, degree and job
'''
def draw_influential_helper(type_map):
    key_list = [key for key in type_map]
    key_list = sorted(key_list)
    value_list = []
    for key in key_list:
        value_list.append(type_map[key])
    plt.bar(range(len(key_list)), value_list,color=['red','green','blue'],tick_label=key_list)
    plt.show()
'''
Statistic for job, gender, age and degree
count the time for each type is enough
'''
def draw_influential(Graph,final_set):
    job_map = {}
    gender_map = {}
    age_map = {}
    degree_map = {}
    all_node = [node for node in Graph.nodes()]
    for name in final_set:
        for node in all_node:
            if name == Graph.nodes[node]['name']:
                j = Graph.nodes[node]['job']
                g = Graph.nodes[node]['gender']
                a = Graph.nodes[node]['age']
                d = Graph.nodes[node]['degree']
                if j in job_map:
                    job_map[j] = job_map[j] + 1
                else:
                    job_map[j] = 1
                if g in gender_map:
                    gender_map[g] = gender_map[g] + 1
                else:
                    gender_map[g] = 1
                if a in age_map:
                    age_map[a] = age_map[a] + 1
                else:
                    age_map[a] = 1
                if d in degree_map:
                    degree_map[d] = degree_map[d]+ 1
                else:
                    degree_map[d] = 1
    draw_influential_helper(job_map)
    draw_influential_helper(gender_map)
    draw_influential_helper(age_map)
    draw_influential_helper(degree_map)

'''
Use centrality to get the top5 influential people from each community
we apply closeness, eigenvector and betweenness
merge them together and pass to helper function for drawing
'''
def expand_from_centrality(modularity,Graph):
    final_list= []
    for group in modularity:
        
        module = [node for node in Graph.nodes() if Graph.nodes[node]['modularity']==group]
        
        closeness = {Graph.nodes[node]['name']:Graph.nodes[node]['closeness'] for node in module}
        closeness = sorted(closeness.items(),key = lambda k:k[1],reverse=True)[:5]
        closeness_final = [i [0] for i in closeness]
        
        eigen = {Graph.nodes[node]['name']: Graph.nodes[node]['eigenvector'] for node in module}
        eigen = sorted(eigen.items(),key = lambda k:k[1],reverse=True)[:5]
        eigen_final = [i[0] for i in eigen]

        between = {Graph.nodes[node]['name']:Graph.nodes[node]['betweenness'] for node in module}
        between= sorted(between.items(),key = lambda k:k[1],reverse=True)[:5]
        between_final = [i[0] for i in between]

        final_list += (list(set(closeness_final + eigen_final + between_final)))

    draw_influential(Graph,final_list)
'''
Community detection and give each community different color
return a map which include community number and community member.
'''
def community(Graph):
    community = c.best_partition(Graph)
    modularity = {}
    for key in community:
        if community[key] in modularity:
           modularity[community[key]].append(key)
        else: modularity[community[key]] = [key]
    #print(modularity)
    # add attribute to nodes
    nx.set_node_attributes(Graph,community,'modularity') 
    pos = nx.spring_layout(Graph)
    # color the nodes according to their partition
    ax = plt.gca()
    ax.set_title('Community')
    cmap = cm.get_cmap('viridis', max(community.values()) + 1)
    nx.draw_networkx_nodes(Graph, pos, community.keys(), node_size=80,
                       cmap=cmap, node_color=list(community.values()))
    nx.draw_networkx_edges(Graph, pos, alpha=0.5, ax = ax)
    #nx.draw(Graph,with_labels = True)
    plt.show()
    return modularity

'''
Draw the graph for community2 and ranked them with closeness centrality
Draw the graph for community2 and ranked them with eigen_vector centrality
Draw the graph for community2 and ranked them with betweeness centrality
'''
def community_centrality(Graph,m):
    #closeness_centrality
    closeness = nx.closeness_centrality(Graph)
    nx.set_node_attributes(Graph, closeness,m)  
    module_two = [node for node in Graph.nodes() if Graph.nodes[node]['modularity']==2]
    class2 = {node: Graph.nodes[node][m] for node in module_two }
    class2 = sorted(class2.items(),key = lambda k:k[1],reverse=True)
    Graph = nx.Graph()
    close_node,close_egde,color_map1 = construct_new_graph2(class2)
    Graph.add_nodes_from(close_node)
    Graph.add_edges_from(close_egde)
    ax = plt.gca()
    ax.set_title('Top6 nodes and edges according to ' + m)
    nx.draw(Graph,with_labels = True,node_color = color_map1,font_size = 7,ax = ax)
    plt.show()

# list of dictionary to store the meta data from each member as gobal value
# main function starts from here
job = {}
gender = {}
age = {}
names = []
degree ={}
names_map = {}
edges = data_preprocess()
# for drawing the job and degree box plot
job_rank = {}
for key in job:
    if job[key] in job_rank:
         job_rank[job[key]] = job_rank[job[key]] + 1
    else:
        job_rank[job[key]] = 1
job_rank= sorted(job_rank.items(),key = lambda k:k[1],reverse=True)
Graph = nx.Graph()
Graph.add_nodes_from(names)
Graph.add_edges_from(edges)

# set attribute for nodes in the graph
nx.set_node_attributes(Graph,names_map,'name')
nx.set_node_attributes(Graph,age,'age') 
nx.set_node_attributes(Graph,gender,'gender') 
nx.set_node_attributes(Graph,job,'job')
degree = {Graph.nodes[node]['name']: Graph.degree(node)for node in Graph.nodes() }
nx.set_node_attributes(Graph,degree,'degree')

# some info and data visulization
print(nx.info(Graph))
tc = nx.transitivity(Graph)
print("Triadic closure:", tc)
print("Graph density:",nx.density(Graph))


degree_age(Graph)
degree_gender(Graph)
degree_job(Graph)

modularity = community(Graph)
community_centrality(Graph,'closeness')
community_centrality(Graph,'eigenvector')
community_centrality(Graph,'betweenness')
expand_from_centrality(modularity,Graph)
