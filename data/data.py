import pandas as pd 
data= pd.read_csv("Final_data.csv")
data["result"] = data["result"].str.replace("Blockbuster","1",regex=True)
data["result"] = data["result"].str.replace("Super Hit","2",regex=True)
data["result"] = data["result"].str.replace("Hit","3",regex=True)
data["result"] = data["result"].str.replace("disaster","4",regex=True)
data["result"] = data["result"].str.replace("flop","5",regex=True)
data.to_csv("Final_Data.csv")