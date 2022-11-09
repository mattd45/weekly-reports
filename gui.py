import csv
from functions import *
import tkinter as tk 
from tkinter import ttk
from PIL import Image, ImageTk

#Creates the window
root = tk.Tk()
root.geometry("900x1000")
root.resizable(width=False, height=False)
root.title("Weekly Analyizer")
root.columnconfigure(0, minsize=300, weight= 1)
root.columnconfigure(1, minsize=300, weight= 1)
root.columnconfigure(2, minsize=300, weight= 1)



#setting up the header message

# Read and resize the Image
image = Image.open("header.png")
resize_image = image.resize((900, 300))
img = ImageTk.PhotoImage(resize_image)
header = tk.Label(image=img)
header.image = img
header.grid(column=0, row=0, columnspan = 3, sticky=tk.N, padx=0, pady=5)


#giving a bio of the program
intro1 = tk.Label( text = "\nThis program is designed to analyise the weekly trading history of a pair")
intro2 = tk.Label( text = "choose a trading pair and you can see if there are any weekly trends")
intro1.grid(column=0, row=1, columnspan = 3, sticky=tk.S, padx=5, pady=5)
intro2.grid(column=0, row=2, columnspan = 3, sticky=tk.S, padx=5, pady=5)


#getting the amount of weeks
def weeks_command():
	timeframe = e.get()
	dates = date_set(timeframe)

	def pair_command(dates):
		pair = clicked.get()
		pair = pair.replace("',)","")
		pair = pair.replace("('","")
		clean_folder()
		data_set(dates, pair)
		choose_method(timeframe)

	file = "pairs.csv"

	with open(file) as f:
		reader = csv.reader(f)
		pairs = []
		for row in reader:
			pairs.append(row)

	clicked = tk.StringVar()
	clicked.set( "BTCUSDT" )

	pair_text = tk.Label( text = "\nplease type your chosen dataset(eg: BTCUSDT):")
	pair_text.grid(column=1, row=3, sticky=tk.S, padx=5, pady=5)

	drop = tk.OptionMenu( root , clicked , *pairs )
	drop.grid(column=1, row=4, sticky=tk.S, padx=5, pady=5)

	b2 = tk.Button(root, 
		text = "Apply",
		command=lambda: pair_command(dates))
	b2.grid(column=1, row=5, sticky=tk.N, padx=5, pady=5)


week_text = tk.Label( text = "\nHow many weeks:")
week_text.grid(column=0, row=3, sticky=tk.S, padx=5, pady=5)

e= tk.Entry(root, width = 3)
e.grid(column=0, row=4, sticky=tk.S, padx=5, pady=5)

b1= tk.Button(root, text = "Apply", command=weeks_command)
b1.grid(column=0, row=5, sticky=tk.N, padx=5, pady=5)

root.mainloop()
