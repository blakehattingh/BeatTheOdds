import numpy as np
import math as math
from numpy.core.fromnumeric import var

def choose(option, total):
    temp = np.zeros(total)
    temp[option] = 1.
    return temp

def choose(outcomes,choices):
    if (len(choices) == 0):
        return np.ones(len(outcomes))
    else:
        temp = np.zeros(len(outcomes))
        for i in choices:
            counter = 0
            Searching = True
            while (Searching):
                if (i == outcomes[counter]):
                    temp[counter] = 1
                    Searching = False
                else:
                    counter += 1
        return temp

def appendOutcomes(dx,pars,outcomes,p,index,n):
    if p==n:
        if len(index)>1:
            return dx[tuple(index)]
        else:
            return dx[index[0]]
    else:
        temp=[]
        for j in range(len(outcomes[pars[p]])):
            temp.append(appendOutcomes(dx,pars,outcomes,p+1,index+[outcomes[pars[p]][j]],n))
        return temp

def get_children(nodes,parents):
    children={}

    for n in nodes:
        if n not in parents:
            parents[n]=[]
        children[n]=[]

    for n in nodes:
        for p in parents[n]:
            children[p].append(n)

    return children

def factor_graph(nodes,parents,info):
    children=get_children(nodes,parents)
    variable_data={}
    variable_adj={}
    factor_data={}
    factor_adj={}
    for n in nodes:
        variable_data[n]=info[n]
        factor_data[n]=np.ones(info[n].size)
        factor_adj[n]=parents[n]+[n]
        variable_adj[n]=[n]+children[n]
            
    
    return variable_data,variable_adj,factor_data,factor_adj
    

def beliefpropagation(nodes, dist, parents, outcomes, info, iterations, tolerance, NodesToReturn, Viscosity=0.5, UsingVis = False):

    M={}
    for x in dist:
        if x in parents:
            M[x]=appendOutcomes(dist[x],parents[x],outcomes,0,[],len(parents[x]))
        else:
            M[x]=dist[x]
    
    msg_v_to_f = {}
    msg_f_to_v = {}

    variable_data, variable_adj, factor_data, factor_adj = factor_graph(nodes,parents,info)

    for n in nodes:
        msg_v_to_f[n]={}
        msg_f_to_v[n]={}
        for m in variable_adj[n]:
            msg_v_to_f[n][m]=np.ones(info[n].size)

        for m in factor_adj[n]:
            msg_f_to_v[n][m]=np.ones(info[m].size)
        
    for iteration in range(iterations):
        print('Iteration '+str(iteration+1))
        # v to f
        for v in nodes:
            variable_data[v]=info[v].copy()
            for f in variable_adj[v]:
                variable_data[v]*=msg_f_to_v[f][v]
            variable_data[v]/=sum(variable_data[v])
            
            for f in variable_adj[v]:
                temp=msg_v_to_f[v][f]
                msg_v_to_f[v][f]=info[v].copy()
                for g in variable_adj[v]:
                    if f!=g:
                        msg_v_to_f[v][f]*=msg_f_to_v[g][v]
                if UsingVis:
                    msg_v_to_f[v][f] = (Viscosity) * temp + (1. - Viscosity) * msg_f_to_v[g][v]
        
        if iteration>0:
            converged=True
            for v in nodes:
                conv=np.linalg.norm(previous[v]-variable_data[v])
                #print("Conv = " + str(conv))
                if conv>tolerance:
                    converged=False
                    break
            if converged:
                print("Converged!")
                break
                
        previous=variable_data.copy()

        #f to v
        for f in nodes:
            temp={}
            if len(factor_adj[f])==1:
                v=factor_adj[f][0]
                msg_f_to_v[f][v]=M[f]
            else:
                count=1
                div={}
                for v in factor_adj[f]:
                    div[v]=count
                    count*=info[v].size

                for v in factor_adj[f]:
                    temp=msg_f_to_v[f][v]
                    msg_f_to_v[f][v]=np.zeros(info[v].size)
                    for i in range(info[v].size):
                        for j in range(count):
                            index=math.floor(j/div[v]) % info[v].size
                            if index==i:
                                prob=M[f]
                                for k in factor_adj[f]:
                                    index=math.floor(j/div[k]) % info[k].size
                                    prob=prob[index]
                            
                                for k in factor_adj[f]:
                                    if k!=v:
                                        index=math.floor(j/div[k]) % info[k].size
                                        prob*=msg_v_to_f[k][f][index]
                                msg_f_to_v[f][v][i]+=prob
                    msg_f_to_v[f][v]/=sum(msg_f_to_v[f][v])
                    if UsingVis:
                        msg_f_to_v[f][v] = ( Viscosity) * temp + (1. - Viscosity) * msg_f_to_v[f][v]


    for v in nodes:
        print(v+': Outcomes ',end='')
        print(outcomes[v],end='')
        print(', Distribution ',end='')
        print(variable_data[v])
        
    # Return the distributions of interest (usually the leaf nodes):
    ReturnDists = []
    for node in NodesToReturn:
        ReturnDists.append(variable_data[node].tolist())
    return ReturnDists


