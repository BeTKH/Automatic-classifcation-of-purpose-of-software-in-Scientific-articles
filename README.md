# Scientific Text Classification with BERT
Master's Thesis Project

### Project Overview

This project is about classification of scientific text using BERT-based models, including Bio-BERT and Sci-BERT. The primary goal is to identify and categorize the purpose of software or tools mentioned in scientific research papers.

To achieve this, a set of scientific texts is hand labeled using the BRAT text annotation tool. The annotated data is then leveraged along with pre-trained BERT models to automatically classify the texts based on their content.

# Implementation Steps
- Defined software categories for labeling using knowledge bases and network analysis 
- identified appropriate classification algorithms.
- Annotated the dataset using the BRAT text annotation tool.
- Cleaned and transformed the data into the I-O-B format for model compatibility.
- Performed text classification and visualized the results for better insights.

## Sample Labeled text in BRAT software:

![Simplified Architecture](ann2.png)

# Classifier Architecture

### Architecture:
![Architecture](arch4.png)

### Simplified Architecture:
![Simplified Architecture](arch2.png)


# Dependencies 

- This project uses [Articlenizer](https://github.com/dave-s477/articlenizer) to transofrm labeled text to I-O-B format.
- The project builds on the top of [SoMeNLP](https://github.com/dave-s477/SoMeNLP)


# Read More

[Paper](https://zenodo.org/records/6509908)

[View the project's data analysis steps](https://htmlpreview.github.io/?https://github.com/BeTKH/Automatic-classifcation-of-purpose-of-software-in-Scientific-articles/blob/main/somecode/1.SoMeSci_Data_Analysis_%28truncated%29.html)

