from functions import *


#welcome to the program
welcome()

# choose time frame

timeframe = input("How many weeks:\n")
dates = date_set(timeframe)

#choose data set 
print("please type your chosen dataset(eg: BTCUSDT):")
clean_folder()
data_set(dates, input())

#process data and choose which method

choose_method(timeframe)

#create graph