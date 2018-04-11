This file contains the python program to compute the skyline set on a 
car data set given in [1]. The attributes of the data set are:

- buying price: vhigh, high, med, low. 
- maintenance cost: vhigh, high, med, low. 
- number of doors: 2, 3, 4, 5more. 
- persons: 2, 4, more. 
- lug_boot: small, med, big. 
- safety: low, med, high.

The dominance relationship is built in the following way:
An object(x) dominates another object(y) if has:
- equal or grater safety, luggage size, capacity, number of doors
- smaller buying price and mentainance cost.

The skyline set is retrieved using the Naive algorithm and it can be seen it consists of 756 objects
out of 1728 in the dataset. So it is almost 44% of the dataset.

[1] UCI Machine Learning Repository - Car Evaluation Data Set
https://archive.ics.uci.edu/ml/datasets/Car+Evaluation
