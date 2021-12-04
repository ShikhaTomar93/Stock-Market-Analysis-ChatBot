# StockMarketAnalysis-withChatBot

Project Objective – 

We plan to automate the stock market analysis using a chatbot. There are various strategies and techniques available in the market which are used by the market traders to predict the direction of a particular stock. But none of these strategies give 100% perfect prediction. We plan to develop a chatbot which can do the comparative analysis for us and tell us what are the hit rates of various techniques combination.

Data Source -

We are using the historic data from Kaggle and it  will consist of various features of the stock market for various companies. We will store the above data in our database and will combine some columns to create other features such as technical indicators, SMA, EMA etc. We will also train our bot to play with the said data to make different combinations and give user the required result.

 
Proposed Analysis-

Our chatbot will interact with the user and ask them about what strategy they want to use and on which stocks, the user can either chose the inbuilt regression techniques or create their own using various technical indicators. Then the bot will backtest the technique on the historic data in our db and will display the success to failure ratio of the technique on the selected stocks.

We also plan to do a live alert, if the user chooses to do a live alert for any stock, as soon as the conditions of a choosen technique meets, he will get the alert regarding same. For this we will need to deploy our project on cloud, so this part is litle complicated 
Milestones-

•	First step will be to get the data set and cleaning it and saving it in the data base.

•	Then we will have to make different technical indicators using the different combinations of the columns of the dataset.

•	Create the chatbot and train the bot to interact with the user related to stock market strategies.

•	Run the chosen strategy on the data and display the hit ratio and plot the graph of success-failure.
