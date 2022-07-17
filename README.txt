===============================================
This Project includes 2 parts corresponding to 2 folders:

1. Sentiment Analysis on Stock related news
2. Stock Price Prediction

===============================================

About the materials:

7404Project
| Sentiment Analysis
  | analyst_ratings_processed.csv
  | Sentiment Analysis.py
| Stock Price Prediction
  | data
     | Stock_Data.csv
     | Stock_Data_with_Sentiment.csv
  | models
     | lstm_sentiment.py
     | lstm_pure.py
     | Other_models.py
  | mymodels
  | myplots
  | requirement.txt
| README.txt

===============================================

How to execute:

For the Sentiment Analysis part:
The data of stock news is given, and there is no requirement environment. It is applicable to run the Sentiment Analysis.py to get the results of the news' sentiment.

For the Stock Price Prediction part:
There are 2 datasets, one with the results of the sentiment analysis above, and the other not.
If you want to execute the 2 lstm related programs, you need to firstly set the requirement environment in the .txt file, and load the dataset needed respectively. Feel free to tune the parameter or change the structure of the lstm model. And you can save the models you trained in the mymodels folders and the plots you produce in the myplots folders.
We also provided some other models like Decision Tree, SVM, MLP, which can be executed through Other_models.py.
===============================================

Please enjoy the project, and we are looking forward to more interesting and better models :)