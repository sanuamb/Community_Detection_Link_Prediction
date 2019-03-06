import networkx as nx


def create_train_graph(graph,test_node,n):
    train_graph=graph.copy()
    #list of neighbors for test_node
    neighbors=sorted(train_graph.neighbors(test_node))
    for i in neighbors[:n]:
        train_graph.remove_edge(i,test_node)
    return train_graph
    

#similarity coefficient
def score_calculation(tr_gr,test_node,k):
    neighbors=set(tr_gr.neighbors(test_node))
    scores=[]
    for n in tr_gr.nodes():
        if test_node!=n and not tr_gr.has_edge(test_node,n):
            neighbors2=set(tr_gr.neighbors(n))
            scores.append(((test_node,n),1.*len(neighbors & neighbors2)/len(neighbors | neighbors2)))
    return sorted(scores,key=lambda x: (-x[1],x[0][1]))[:k]


#calculate from root node to each node the length of shortest path
def node2distances(train_graph,source_node):
    lengths=nx.single_source_shortest_path_length(train_graph,source_node)
    d={}
    for x in lengths.keys():
        d[x]=lengths[x]
    return d
    

#from each node to the length of shortest path from root node
def node2numpaths(train_graph,source_node):
    numpaths=nx.single_source_shortest_path(train_graph,source_node)
    d={}
    for x in numpaths.keys():
        d[x]=len(numpaths[x])
    return d


def path_score(graph,test_node,k,beta):
    dis=node2distances(graph,test_node)
    numpaths=node2numpaths(graph,test_node)
    score=[]
    for n in graph.nodes():
        if test_node!=n and not graph.has_edge(n,test_node):
            score.append(((test_node, n), (beta ** dis[n]) * numpaths[n]))
    return sorted(score, key = lambda x:(-x[1],x[0][1]))[:k]


#fraction of predicted edges that exist
def evaluate(predicted_edges,graph):
    count = 0
    for edg in predicted_edges:
        if graph.has_edge(*edg):
            count+=1
    return count/len(predicted_edges)


# In[105]:


def create_subgraph(graph,min_degree):
    newgraph=graph.copy()
    rem_nodes=[node for (node,val) in newgraph.degree() if val<min_degree]
    newgraph.remove_nodes_from(rem_nodes)
    return newgraph


graph=nx.read_edgelist('edges.txt',delimiter='\t')
print('Number of nodes',graph.order(),'number of edges',graph.number_of_edges())


#subgraph
partition=create_subgraph(graph,2)



#Link predicition with test node as Bill Gates

#create a train graph with by removing test nodes
tr_gr=create_train_graph(partition,'Bill Gates',5)
print('Train graph nodes',tr_gr.order(),'Train graph edges',tr_gr.number_of_edges())

#jaccard_scores=
jaccard_scores=score_calculation(tr_gr,'Bill Gates',5)
print(jaccard_scores)
#print([x[0]] for x in jaccard_scores)
#evaluate the accuracy 
lst=[]
for x in jaccard_scores:
    lst.append(x[0])
        
acc=evaluate(lst,partition)
print('Accuracy:',acc)

#print top path scores 
path_scores=path_score(tr_gr,'Bill Gates',5,0.1)
print('\nTop path scores for Bill gates:',path_scores)
acc1=evaluate([x[0] for x in path_scores],partition)
print('Accuracy:',acc1)

