import requests, json, zipfile, io, csv, datetime, calendar, os, glob, math, sys
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk 
from tkinter import ttk
from PIL import Image, ImageTk

def welcome():
	"""welcome message to users"""
	print("================================================================================")
	print("==============================WEEKLY ANALYSIS===================================")
	print("================================================================================")
	print("\n")
	print("This program is designed to analyise the weekly trading history of a pair,")
	print("choose a trading pair and you can see if there are any weekly trends.\n\n")

def date_set(timeframe):
	"""asks the user for the date range and returns this as a date formate for the url"""
	days = int(timeframe)*7
	end_date = datetime.datetime.today() - datetime.timedelta(days=2)
	dates = pd.date_range(end = end_date, periods=days).strftime('%Y-%m-%d')
	return dates

def clean_folder():
	"""makes sure the folders used dont have any old data in them"""

	files = glob.glob('csv/*')
	for f in files:
		os.remove(f)

	days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

	for d in days:
		new_file = f"csv/{d}.csv"
		with open(new_file, 'w') as f:
			f.write('')

def data_set(dates, pair):
	"""asks user to choose pair and downloads the set"""
	#Downloading the zip files for all the dates and saving them
	for date in dates:
		url = f"https://data.binance.vision/data/spot/daily/klines/{pair}/1h/{pair}-1h-{date}.zip"
		r = requests.get(url, stream = True)
		check = zipfile.is_zipfile(io.BytesIO(r.content))
		while not check:
   			r = requests.get(url, stream =True)
   			check = zipfile.is_zipfile(io.BytesIO(r.content))
		else:
			z = zipfile.ZipFile(io.BytesIO(r.content))
			z.extractall('csv')

	print('\n---Download complete---')

	#Extracts the High and low price and saves it in a seperate file

	for date in dates:
		filename = f"csv/{pair}-1h-{date}.csv"
		
		def findDay(date):
			wd = datetime.datetime.strptime(date, '%Y-%m-%d').weekday()
			return (calendar.day_name[wd])

		days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

		for d in days:

			if findDay(date) == d:

				new_file = f"csv/{d}.csv"
									
				#saving the highs and lows
				with open(filename) as f:
					reader = csv.reader(f)
					highs = []
					lows = []
					for row in reader:
						high = str(row[2])
						low = str(row[3])
						highs.append(high)
						lows.append(low)

						with open(new_file, 'a') as file_object:
							file_object.write(f"{high},{low}\n")

	print('---Finished seperating---')		

def choose_method(timeframe):
	"""Choosing the method"""
	choice_text1 = tk.Label( text = 
		"\n\nWhich method would you like to use (1,2,3):\nFor more information on them type 'h':")
	choice_text1.grid(column=2, row=3, sticky=tk.S, padx=5, pady=5)

	def choice_command():
		"""choosing the options"""
		active = True
		while active:
			option = c.get()
			if option == "1":
				method_1()
				active = False
			elif option == "2":
				method_2(timeframe)
				active = False
			elif option == "3":
				method_3(timeframe)
				active = False
			elif option == "h" or "H":
				details()
				active = False
			else:
				print("Please choose a valid input")
				print("What method do you choose?")
	
	c= tk.Entry( width = 7)
	c.grid(column=2, row=4, sticky=tk.S, padx=5, pady=5)

	c1=tk.Button(text = "Apply",
		command=lambda: choice_command())
	c1.grid(column=2, row=5, sticky=tk.N, padx=5, pady=5)
			
def method_1():
	"""all the maths to pot the graph"""
	filename = "csv/hourly_average.csv"
	with open(filename, 'w') as file_object:
		file_object.write('')

	days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	for d in days:

		filename = f"csv/{d}.csv"

		with open(filename) as f:
			reader = csv.reader(f)
			highs = []
			lows = []
			for row in reader:
				high = str(row[0])
				low = str(row[1])
				highs.append(high)
				lows.append(low)
			
		new_h = []
		new_l = []

		for num in range(0,24):

			for r in range(num, len(highs), 24):
				new_h.append(highs[r])
				new_l.append(lows[r])
				
			x = [float(y) for y in new_h]
			x = sum(x)
			z = len(new_h)
			average_h = (x/z)
			
			x = [float(y) for y in new_l]
			x = sum(x)
			z = len(new_l)
			average_l = (x/z)

			filename = "csv/hourly_average.csv"
			with open(filename, 'a') as file_object:
				file_object.write(f"{average_h},{average_l}\n")

	print('---Averages Calculated---')

	plot_m1()

def plot_m1():
	filename = "csv/hourly_average.csv"

	with open(filename) as f:
		reader = csv.reader(f)
		header_row = next(reader)

		# Get dates, and high and low prices from this file.
		highs, lows = [], []
		

		for row in reader:
			high = float(row[0])
			low = float(row[1])
			highs.append(high)
			lows.append(low)

	# Plot the high and low prices.
	plt.style.use('seaborn')
	fig, ax = plt.subplots()
	ax.plot(highs, c='green')
	ax.plot(lows, c='red')

	# Format plot.
	#plt.title("Weekly average results", fontsize=24)
	ax.axes.get_xaxis().set_visible(False)
	ax.axes.get_yaxis().set_visible(False)

	#plt.show()
	plt.savefig('csv/results.png', bbox_inches='tight')
	display_results()

def method_2(timeframe):
	"""This method just shows the weeks on top of each other so you can see your own trends"""
	days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	start = 0
	end = 24

	plt.style.use('seaborn')
	fig, ax = plt.subplots()
	colors = "bgrcmykw"
	color_index = 0
	#plt.title("Overlayed Results", fontsize=24)
	ax.axes.get_xaxis().set_visible(False)
	ax.axes.get_yaxis().set_visible(False)

	for t in range(1,timeframe+1):
		new_file = f"csv/week{t}.csv"
		with open(new_file, 'w') as f:
			f.write("")

		for d in days:

			filename = f"csv/{d}.csv"

			#opens the week day file and changes it to a week file list

			with open(filename) as f:
				reader = csv.reader(f)
				header_row = next(reader)
				week = []
				for row in reader:
					high = float(row[0])
					low = float(row[1])
					average = high + low
					average = average/2
					week.append(str(average))
					

				#writes this list to a new document
				week1 = []
				try:
					for num in range(start,end):
						week1.append(week[num])
						with open(new_file, 'a') as file_object:
							file_object.write(f"{week[num]}\n")
				except IndexError:
					pass

		start = start + 24
		end = end + 24

	for t in range(1,timeframe+1):
		new_file = f"csv/week{t}.csv"
		with open(new_file) as f:
			reader = csv.reader(f)
			week_dif = []
			for row in reader:
				week_dif.append(row)

		x = 0
		y = 1
		diff_list = []

		try:
			for r in range(0,len(week_dif)):
				point_1 = week_dif[x]
				point_2 = week_dif[y]
				for p in point_1:
					p1 = float(p)
				for p in point_2:
					p2 = float(p)
				new_point = p1 - p2 
				diff_list.append(new_point)
				x = x+1
				y = y+1
		except IndexError:
			pass

		#print(diff_list)


		ax.plot(diff_list, c = colors[color_index])
		color_index += 1


	#plt.show()
	plt.savefig('csv/results.png', bbox_inches='tight')
	display_results()
			
def method_3(timeframe):
	"""This method just shows the weeks on top of each other so you can see your own trends"""
	days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	start = 0
	end = 24
	timeframe = int(timeframe)

	for t in range(1,timeframe+1):
		new_file = f"csv/week{t}.csv"
		with open(new_file, 'w') as f:
			f.write("")

		

		for d in days:

			filename = f"csv/{d}.csv"

			with open(filename) as f:
				reader = csv.reader(f)
				header_row = next(reader)
				week = []
				for row in reader:
					high = float(row[0])
					low = float(row[1])
					average = high + low
					average = average/2
					week.append(str(average))
					

				week1 = []
				try:
					for num in range(start,end):
						week1.append(week[num])
						with open(new_file, 'a') as file_object:
							file_object.write(f"{week[num]}\n")
				except IndexError:
					pass

		start = start + 24
		end = end + 24

	plot_m3(timeframe)

def plot_m3(timeframe):
	

	plt.style.use('seaborn')
	fig, ax = plt.subplots()
	colors = "bgrcmykw"
	color_index = 0

	for t in range(1,timeframe+1):
		filename = f"csv/week{t}.csv"

		with open(filename) as f:
			reader = csv.reader(f)
			prices = []
			for row in reader:
				for r in row:
					price = float(r)
					prices.append(price)
			ax.plot(prices, c = colors[color_index])
			color_index += 1

	
	#plt.title("Overlayed Results", fontsize=24)
	ax.axes.get_xaxis().set_visible(False)
	ax.axes.get_yaxis().set_visible(False)

	#plt.show()
	plt.savefig('csv/results.png', bbox_inches='tight')
	display_results()

def details():
	"""the how to text"""
	detail = tk.Label( text =
	 """In this program we offer you three methods
	 to use to anaylise your data:

	Method 1
	This method takes an average price of each hour of 
	the day over the week period and
	plots it so you can see the trends

	Method 2
	This method calculates the difference in price 
	between each hour then averages that
	price difference over the weeks

	Method 3
	Lastly this method just plots all the weeks prices
	 on top of each other so you can see")
	for yourself if there are any trends
	
	What method do you choose?""")
	detail.grid(column=1, row=6, sticky=tk.S, padx=5, pady=5)

def display_results():
	image = Image.open("csv/results.png")
	resize_image = image.resize((900, 600))
	img = ImageTk.PhotoImage(resize_image)
	results = tk.Label(image=img)
	results.image = img
	results.grid(column=0, row=1, columnspan = 3, rowspan = 5, sticky=tk.N, padx=0)

	days_label = tk.Label( text = 
		"Monday\t\tTuesday\t\tWednesday\t\tThursday\t\tFriday\t\tSaturday\t\tSunday")
	days_label.grid(column=0, row=6, columnspan = 3, sticky=tk.S, padx=5, pady=5)

	reset = tk.Button(text="Restart", command=restart)
	reset.grid(column=0, row=7, sticky=tk.S, padx=5, pady=5)


def restart():
	"""a process to reset the program"""
	python = sys.executable
	os.execl(python, python, * sys.argv)












		

			




