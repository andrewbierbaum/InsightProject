# InsightProject

The goal of this project is to track technology trends in various technical and social medial sources. This help gauge momentum behind a technology and identify the best posts for user discussion. 



## Pipeline
![Screen Shot 2019-04-18 at 5 45 01 PM](https://user-images.githubusercontent.com/44590433/56399272-ca4c5400-6201-11e9-89c3-90587148854c.png)
## www.andrewbierbaum.com

Historical reddit data was batch processed using spark sql, processed in python, saved in sqlite, and visualized using dash. Near real-time updates were incorperated using a web API. The search tab was implemented using a reddit search API grabing 1000 records per call to generate the graph and comparison tables.



