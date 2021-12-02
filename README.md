# Automatic Classification of purpose of Software Usage Statements from Scientific Articles

### (Master Thesis)

In a modern research, scientists use various kinds of software for various purposes to accomplish tasks ranging from very simple ones to complicated. Typically, scientists use software for purposes like Data Analysis, Modelling, Simulation and so on.  

It is very important to identify for what purpose scientists use software during their research. This gives insights about what types of software are impacting a research, to what direction a modern research is being geared, etc..

This project tries , first to explore all possible software usage possibilities by categorizing software in groups. List of all possible software categories has been queried from WikiData using SPARQL. To extract meaningful relation between all software categories, Network analysis and visualization has been carried out using Gephi Software as well as the built in WikiData grapgh visualizer. Moreover, list of software types from SciCrunch has also been incorporated to make sure all software categories are listed. 

Based on the list of software categories and its hierarchical classification, all software usage possibilities will be identified and will be used to annotate text data from SoMeSci with software usage statements. 

Once SoMeSci is annotated with software usage statements, features will be selected along with a training algorithm. 
Finally, results from various training algorithms will be compared, fine tuned and presented.