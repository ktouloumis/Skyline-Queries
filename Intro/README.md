In this file I attach the implementation in Python of some algorithms mentioned in [1].
The specific research builds uppon a very simple example. That is a 2 dimensional database.
Suppose the dataset describes houses with 2 attributes. The first is the distance from the University 
and the second is the distance from the train. In this case the skyline set will contain all
the houses with the minimum distance from both the train and the university. Because the dataset consists of 2 attributes 
it can be represented on the 2 dimensional x-y plane. So, the points we are looking for are the ones closer to 
the zero point (0,0). Three algorithms are implemented specifically, the Naive, the Block-Nested-Loop, and the Divide and Conquer.
Each algorithm is developed in each own module with the corresponding name and each module is imported in the main.py where
all the algorithms are executed and the results are displayed

[1]Eleftherios Tiakas, Apostolos N. Papadopoulos, and Yannis Manolopoulos. 2016.
Skyline Queries: An Introduction. In Proceedings 6th International Conference on
Information, Intelligence, Systems & Applications (IISA). 1–6
