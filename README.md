# Churn Predictor Model
![Status](https://img.shields.io/badge/status-feature_engineering-yellow)

## File structure:
```
churn-predictor/
├── data/              (gitignored — see "Data" section for download)
├── src/
│   └── sample_data.py
├── notebooks/
├── data_decisions.md
└── README.md
```
## Introduction
Predicts whether a KKBox subscriber will churn in the next 30 days, with SHAP-based explanations of why. Built end-to-end as a portfolio project covering data engineering, modeling, explainability, and serving. This project uses a stratified sample (5000 churner + 5000 non-churner) of the KKBox dataset, 10000 data points from the original to be exact. This sampled dataset is then put through 3 different models of increasing complexity (logistic regression -> random forest -> gradient boosting) for comparison. Finally, the resulting models are discussed through explainability methods such as SHAP.

## Definitions
### Churn:
The concept of a user ceasing use of a product after an X amount of time. For example a user cancelling their subscription to a service after 5 months due to a competitor having better quality for price. 
### Churn Model: 
A model that can predict when a user will churn from certain predictors relevant to the specific product. For example; a Netflix user's usage time per day, the amount of Netflix originals they watch, the amount of movies they stop watching before the end etc. could be indicators for a churn model.
### Why create/use a churn model?
This type of model is very important for companies to decrease their user loss. A churn model can be used to predict leavers early on and use certain strategies to keep them in the service. A very popular approach is offering price deals to customers that are predicted to churn very early.

## Methodology
### Data
The dataset that will be used in this project is called KKBox WSDM Churn Prediction. This dataset is of a real Taiwanese music streaming service. It consists of the behavioral data of approximately 1 million users and has separate files for user logs, transactions and demographic data. 
### Preprocessing
First of all the whole dataset will not be used initially in this project. The beginning scale of this project is set to 10 thousand users so the preprocessing process will start by sampling down the dataset to 10 K users. 

It is also important to note that the data in hand is not very "clean" so to say. 
Firstly, it does not have a set definition as to how a "churner" is defined. Initially it is defined as: "no valid renewal within 30 days of subscription expiration.", however this definition has been called out for being loose by many Kagglers due to many possible edge cases such as users renewing the subscription after the 30 days period, renewal process being cancelled due to payment failures etc. 
Secondly, the data has some quality issues. The biggest issue is with user age. Apparently the service did not have "reasonable age verification" so some users have the age of 0 and some have values above 1000. 

### Pipeline

The preprocessing pipeline begins with sampling. This sampling process was - as explained in the introduction - is stratified sampling of 5000 users that churned and 5000 users that did not churn to avoid bias in the model. Users were sampled from train.csv, a label file from the original KKBox Kaggle competition that pairs each user ID with their churn outcome. From it, 5,000 churners and 5,000 non-churners were sampled at random. Then the other documents were parsed to extract demographic, transactional and behavioral data with respect to their codes. For some users, demographic and behavioral data were not available however I chose to keep those users as them not having the demographic and behavioral data puts them in another category altogether. The transaction and user_logs files were too large to load into memory whole, so a chunked-streaming approach was used. A default chunk size of 1 million rows at a time was selected to parse and record these files based on the 10000 selected users. The process was simply to create an iterator that would iterate through 1000000 rows at a time to create chunks of data and then these chunks were concatenated into parquet files for faster reading by the model and feature engineering algorithms. 