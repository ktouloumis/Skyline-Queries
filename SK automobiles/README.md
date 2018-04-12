In this folder a python program included that computes the skyline set on the automobile
dataset given in [1]

This data set specifies an auto in terms of various characteristics, among some of the characteristics are:
Among them the most characteristic are:

- Company 
- Fuel type 
- Number of doors
- Horse power
- Price
- Compression-ratio
- Fuel system
- Engine size
- Number of cylinders


The skyline query was built upon the following dominance rule:
An automobile dominates another if:
- it has equal or grater, horsepower, number of doors, compression ratio, size, fuel type
- and it is cheaper

We can see that the skyline set consists of 100 objects out of the 206 in the initial dataset.
So it is almost 49%.

[1]Automobile Dataset,Dataset consist of various characteristic of an auto
https://www.kaggle.com/toramky/automobile-dataset/data
