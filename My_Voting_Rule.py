#!/usr/bin/env python
# coding: utf-8

# In[47]:


import numpy as np

pairwise_graph = open("ED-00009-00000001.pwg", "r")
pairwise_graph_lines = pairwise_graph.readlines()

voting_profile = open("ED-00009-00000001.soc", "r")
voting_profile_lines = voting_profile.readlines()

start_point = int(voting_profile_lines[0]) + 2

n_candidates = int(pairwise_graph_lines[0])
num_of_rounds = int(n_candidates/2)
#print(num_of_rounds)

list_out = []

def check_for_condorcet_winner(pairwise_graph_lines):
    start_point = int(pairwise_graph_lines[0]) + 2
    candidates = np.zeros((int(pairwise_graph_lines[0]), int(pairwise_graph_lines[0])))
    counter = 0
    for line in pairwise_graph_lines[1:]:
        if counter < start_point - 1:
            if counter < start_point - 2:
                counter = counter + 1
            else:
                total_number_voters, total_rankings, unique_rankings = line.split(",")
                total_number_voters = int(total_number_voters)
                counter = counter + 1
                continue
        else:
            weight, source, destination = line.split(",")
            candidates[int(source) - 1][int(destination) - 1] = total_number_voters
    #print(candidates)
    condorcet_winner_l = [True] * len(candidates)
    for i in range(0, len(candidates)):
        for j in range(0, len(candidates)):
            if i == j:
                continue
            else:
                if candidates[i][j] < candidates[j][i]:
                    condorcet_winner_l[i] = False
                    
    #print(condorcet_winner_l)
    condorcet_winner = None
    for i in range(0, len(condorcet_winner_l)):
        if condorcet_winner_l[i] == True:
            condorcet_winner = i + 1
            
    return candidates, condorcet_winner

candidates, condorcet_winner = check_for_condorcet_winner(pairwise_graph_lines)

list_out.append(condorcet_winner)

k = 0
while (k < num_of_rounds):
    points_STV = [0] * (n_candidates)
    counter = 0
    for line in voting_profile_lines[1:]:
        if counter < start_point - 1:
            if counter < start_point - 2:
                counter = counter + 1
            else:
                total_number_voters, total_rankings, unique_rankings = line.split(",")
                total_number_voters = int(total_number_voters)
                counter = counter + 1
                continue
        else:
            c = [None] * int(voting_profile_lines[0])
            line_list = line.split(",")
            num_of_votes = line_list[0]
            c = []
            for i in range(1, len(line_list)):
                c.append(int(line_list[i]))
            first_place = int(c[0])
            for i in range(1, len(c)):
                if first_place in list_out:
                    first_place = int(c[i])
            else:
                points_STV[int(first_place) - 1] = points_STV[int(first_place) - 1] + int(num_of_votes)
    #print(points_STV)
    loser_STV = 0
    for i in range(1, len(points_STV)):
        if (loser_STV + 1) in list_out:
            loser_STV = i
        if (i + 1) in list_out:
            continue
        elif points_STV[i] < points_STV[loser_STV]:
            loser_STV = i
    loser_STV = loser_STV + 1
    list_out.append(loser_STV)
    k = k + 1
    #print(list_out)


# last round
#print("plurality")
points_plurality = [0] * (n_candidates)

counter = 0
for line in voting_profile_lines[1:]:
    if counter < start_point - 1:
        if counter < start_point - 2:
            counter = counter + 1
        else:
            total_number_voters, total_rankings, unique_rankings = line.split(",")
            total_number_voters = int(total_number_voters)
            counter = counter + 1
            continue
    else:
        #c = [None] * int(voting_profile_lines[0])
        line_list = line.split(",")
        num_of_votes = line_list[0]
        c = []
        for i in range(1, len(line_list)):
            c.append(int(line_list[i]))
        #print(c)
        for i in range(0, len(c)):
            if c[i] in list_out:
                #print(c[i])
                continue
            else:
                #print(c)
                #print("first", c[i])
                first_place = c[i]
                break
        #print("voters", num_of_votes)
        #print("first place", first_place)
        #print(points_plurality)
        points_plurality[int(first_place) - 1] = points_plurality[int(first_place) - 1] + int(num_of_votes)
        #print(points_plurality)
#print(points_plurality)
winner_plurality = 0
for i in range(1, len(points_plurality)):
    if points_plurality[i] > points_plurality[winner_plurality]:
        winner_plurality = i

#breaking ties lexicographic
for i in range(0, len(points_plurality)):
    if points_plurality[i] == points_plurality[winner_plurality]:
        if i > winner_plurality:
            winner_plurality = i
              
winner_plurality = winner_plurality + 1
print("The winner in our new method is: Course", winner_plurality)

    
    


# In[ ]:




