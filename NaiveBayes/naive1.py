"""
Implementing Naive bayes from scratch
2 class outcome
"""

import csv

filename = 'stayorgo.csv'
with open(filename, 'r') as csvfile:
    lines = csv.reader(csvfile)
    dataset = list(lines)

#print(dataset)

weather = [x[0] for x in dataset[1:]]
car = [x[1] for x in dataset[1:]]
outcome = [x[2] for x in dataset[1:]]

featurelist = []
for i in range(len(dataset[0])-1):
    feat = [x[i] for x in dataset[1:]]
    featurelist.append(feat)

featurename = dataset[0][0:-1]

# Calculate class probabilites
cl_prob = [outcome.count(x)/len(outcome) for x in set(outcome)]
cl_prob = dict(zip(set(outcome), cl_prob))
print(cl_prob)  # dictionary

# Calculate conditional probability
cond_prob = {}
for i in range(len(dataset[0])-1):
    pred_cl = [[x[i], x[-1]] for x in dataset[1:]]

    pred = [x[0] for x in pred_cl]
    cl = [x[1] for x in pred_cl]
    clcount = dict(zip(set(cl), [cl.count(x) for x in set(cl)]))
    set_pred_cl = [[x,y] for x in set(pred) for y in set(cl)]
    pred_cl_count = [[el, pred_cl.count(el)] for el in set_pred_cl]
    d = {}
    for el1 in cl:
        d[el1] = {}
        for el2 in pred:
            d[el1][el2] = 0

    for item in pred_cl_count:
        d[item[0][1]][item[0][0]] = item[1] / clcount[item[0][1]]

    print(d)
    cond_prob[dataset[0][i]] = d

# print(cond_prob)    # dictionary


# Calculate for each rows

# calc for 2 rows:
prediction_prob_dict = {}
# for each outcome possibility:
for res in set(outcome):
    print("Calculate feature probability for:", res)
    #Calculate feature probability for each outcome
    featureprob = []
    for i in range(len(featurename)):
        
        temp_prob = []
        for val in featurelist[i]:
            temp_prob.append(cond_prob[featurename[i]][res][val])
        # print(temp_prob)
        featureprob.append(temp_prob)
    print('Feature Probability [', res, ']:', featureprob)
    # Calculate the total probability
    outcome_prob_temp = []
    for j in range(len(featureprob[0])):
        prob = cl_prob[res]
        for i in range(len(featureprob)):
            prob *= featureprob[i][j]
        outcome_prob_temp.append(round(prob, 2))
    # print(outcome_prob_temp)
    prediction_prob_dict[res] = outcome_prob_temp


print("Probability Calculation:", prediction_prob_dict)

pred_result = [list(prediction_prob_dict)[0] if x > y else list(prediction_prob_dict)[1] \
                for x,y in zip(list(prediction_prob_dict.values())[0], list(prediction_prob_dict.values())[1])]
print('Prediction Result:', pred_result)

# Alternative for multi-class Naive Bayes problem
# l1 = zip(*prediction_prob_dict.values())
# l2 = list(prediction_prob_dict.keys())
# l3 = [l2[i.index(max(i))] for i in l1]
# print('Prediction Result:', l3)

print('** Accuracy **')
score = 0
for i in range(len(pred_result)):
    if outcome[i] == pred_result[i]:
        score += 1

accuracy_score = score / len(outcome)
print('Accuracy:', accuracy_score*100, '%')

