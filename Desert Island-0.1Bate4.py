import tkinter as tk
from tkinter import messagebox
import random

#----------------------------------------------------------------------------------------------------------------------------------------#

def UpdateData(time):
    global water_value,food_value,food_value_RescueSpeed,water_value_RescueSpeed,living_time
    
    #FoodValue Calculation
    food_value -= int(food_value_RescueSpeed*time)

    #WaterValue Calculation
    water_value -= int(water_value_RescueSpeed*time)
    
    time_label.config(text=f"Living Time:{living_time}")
    health_value_label.config(text=f"Health Value:{health_value}")
    food_value_label.config(text=f"Food Value:{food_value}")
    water_value_label.config(text=f"Water Value:{water_value}")

def information(destination):
    global root, information_window, StartingPoint, move_time, LocationDict

    root.withdraw()                     # 隐藏窗口。
    information_window.deiconify()		# 使窗口重新显示在电脑屏幕上。
    
    key1 = (StartingPoint, destination)
    key2 = (destination, StartingPoint)

    if key1 in LocationDict:
        move_time = LocationDict[key1]
    elif key2 in LocationDict:
        move_time = LocationDict[key2]
    else:
        move_time = 0

    #The information of destination
    information_label.config(text=destination)
    move_time_label.config(text=f'Move Time:{move_time}')

    if destination == "Home" and StartingPoint == "Home":
        SleepButton.grid()
        information_label.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
    else:
        SleepButton.grid_remove()
        information_label.grid(row=0, column=1, columnspan=1, padx=5, pady=5)
    
def move():
    global living_time, destination, StartingPoint, move_time

    StartingPoint = destination.get()  # Get the string value from the StringVar
    living_time += move_time
    UpdateData(move_time)

    information_window.withdraw()            # 隐藏窗口。
    root.deiconify()		                 # 使窗口重新显示在电脑屏幕上.

    destination.set("")
    
def ExploreButton():
    global living_time
    
    #Time Calculation
    explore_time = 40
    living_time += explore_time
    
    #FoodCard Calculation
    FoodCard_Probability = random.uniform(0.7,1.1)
    item_number["FoodCard"] += int(FoodCard_Probability)

    #WaterCard Calculation
    WaterCard_Probability = random.uniform(0.85,1.2)
    item_number["WaterCard"] += int(WaterCard_Probability)

    feedback_label.config(text="Complete exploring")
    UpdateData(explore_time)

def go_back():
    information_window.withdraw()
    root.deiconify()
    destination.set("")

def show_current_location():
    feedback_label.config(text=f"Current Location: {StartingPoint}")

def update_bag_labels():
    bag_listbox.delete(0, tk.END)
    items = ["WaterCard","FoodCard","AidBag"]
    for i in items:
        bag_listbox.insert(tk.END, i)

def use_item(item_name):
    global water_value, food_value, health_value
    text = ''
    if item_number[item_name] > 0:
        item_number[item_name] -= 1
        for i,v in item_information[item_name].items():
            if i == "water value":
                water_value += v
            elif i == "food value":
                food_value += v
            elif i == "health value":
                health_value += v
            text += f"Add {v} {i}.\n"
        more_information_label.config(text=text)
        update_bag_labels()
        UpdateData(0)
        
    else:
        update_bag_labels()
        more_information_label.config(text=f"You don't have enough {item_name}!")

def sleep():
    global living_time, health_value, water_value, food_value
    living_time += 420
    water_value -= 30
    food_value -= 30
    health_value += 25
    UpdateData(0)
    messagebox.showinfo("Sleep", "You slept for 7 hours.\nHealth +25\nWater -30\nFood -30")

def BagButton():
    if BagButton.cget("text") == "Close Bag":
        BagButton.config(text="Open Bag")
        bag_scrollbar.grid_remove()
        use_button.grid_remove()
        bag_listbox.grid_remove()
        more_information_label.grid_remove()
        WIDTH = 390
        HEIGHT = 250

    elif BagButton.cget("text") == "Open Bag":
        BagButton.config(text="Close Bag")
        bag_scrollbar.grid()
        use_button.grid()
        bag_listbox.grid()
        more_information_label.grid()
        WIDTH = 390
        HEIGHT = 560

    x = (window_x - WIDTH) // 2
    y = (window_y - HEIGHT) // 2
    root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y - 100}")


#------------------------------------------------------------------------------#

# Initialized Data
explore_time = 0   #单位：minute
move_time = 0
living_time = 0
health_value = 100
food_value = 100
water_value = 100

selected_item = ''

food_value_RescueSpeed = 0.23  # per minute
water_value_RescueSpeed = 0.34  # per minute

StartingPoint = 'Home'
destination = ''

item_number = {
    "WaterCard":3,
    "FoodCard":2,
    "AidBag":1
}

item_information= {
    "WaterCard":{"water value":20},
    "FoodCard":{"food value":25},
    "AidBag":{"health value":40}
}

LocationDict = {
    ('Home', 'Forest'): 60,
    ('Home', 'Waterfall'): 50,
    ('Home', 'Mountain'): 100,
    ('Home', 'Beach'): 80,
    ('Forest', 'Waterfall'): 100,
    ('Forest', 'Mountain'): 110,
    ('Forest', 'Beach'): 100,
    ('Waterfall', 'Mountain'): 80,
    ('Waterfall', 'Beach'): 110,
    ('Mountain', 'Beach'): 160
}


#----------------------------------------------------------------------------------------------------------------------------------------#

root = tk.Tk()
root.title("Desert Island-0.1Bate4")

# Set the placement position of the window to the middle of the screen
root.update_idletasks()
window_x = root.winfo_screenwidth()
window_y = root.winfo_screenheight()
WIDTH = 390
HEIGHT = 250
x = (window_x - WIDTH) // 2
y = (window_y - HEIGHT) // 2
root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y - 100}")

# Set whether to prohibit adjusting the width and height of the window
root.resizable(width=True, height=True)

#Auto Fill Blank
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

#------------------------------------------------------------------------------#

# Create Feedback Labels
feedback_label = tk.Label(root, text="Click", font=("Helvetica", 16))
feedback_label.grid(row=0, column=0, columnspan=5, pady=10)

# Create Data Labels
time_label = tk.Label(root, text=f"Living Time:{living_time}", font=("Helvetica", 10))
time_label.grid(row=1, column=0, padx=5, pady=5)

health_value_label = tk.Label(root, text=f"Health Value:{health_value}", font=("Helvetica", 10))
health_value_label.grid(row=2, column=0, padx=5, pady=5)

food_value_label = tk.Label(root, text=f"Food Value:{food_value}", font=("Helvetica", 10))
food_value_label.grid(row=2, column=1, padx=5, pady=5)

water_value_label = tk.Label(root, text=f"Water Value:{water_value}", font=("Helvetica", 10))
water_value_label.grid(row=2, column=2, padx=5, pady=5)

# Create Buttons
ExploreButton = tk.Button(root, text="Explore", command=ExploreButton, padx=10, pady=5)
ExploreButton.grid(row=4, column=0, padx=10, pady=5, sticky="w"+"e")

where_button = tk.Button(root, text="Where?", command=show_current_location, padx=10, pady=5)
where_button.grid(row=4, column=1, padx=10, pady=5, sticky="w"+"e")

BagButton = tk.Button(root, text="Open Bag", command=BagButton, padx=10, pady=5)
BagButton.grid(row=4, column=2, padx=10, pady=5, sticky="w"+"e")

# Create Radiobuttons
destination = tk.StringVar()

HomeRadiobutton = tk.Radiobutton(root, text="Home", variable=destination, value="Home", command=lambda: information("Home"), indicatoron=False, padx=10, pady=5)
HomeRadiobutton.grid(row=5, column=0, padx=10, pady=5, sticky="w"+"e")

ForestRadiobutton = tk.Radiobutton(root, text="Forest", variable=destination, value="Forest", command=lambda: information("Forest"), indicatoron=False, padx=10, pady=5)
ForestRadiobutton.grid(row=5, column=1, padx=10, pady=5, sticky="w"+"e")

WaterfallRadiobutton = tk.Radiobutton(root, text="Waterfall", variable=destination, value="Waterfall", command=lambda: information("Waterfall"), indicatoron=False, padx=10, pady=5)
WaterfallRadiobutton.grid(row=5, column=2, padx=10, pady=5, sticky="w"+"e")

MountainRadiobutton = tk.Radiobutton(root, text="Mountain", variable=destination, value="Mountain", command=lambda: information("Mountain"), indicatoron=False, padx=10, pady=5)
MountainRadiobutton.grid(row=6, column=0, padx=10, pady=5, sticky="w"+"e")

BeachRadiobutton = tk.Radiobutton(root, text="Beach", variable=destination, value="Beach", command=lambda: information("Beach"), indicatoron=False, padx=10, pady=5)
BeachRadiobutton.grid(row=6, column=1, padx=10, pady=5, sticky="w"+"e")


#----------------------------------------------------------------------------------------------------------------------------------------#

information_window = tk.Tk()
information_window.withdraw()
information_window.title("Information")

# Set the placement position of the window to the middle of the screen
WIDTH_1 = 250
HEIGHT_1 = 100
information_window.geometry(f"{WIDTH_1}x{HEIGHT_1}+{x}+{y - 100}")

#------------------------------------------------------------------------------#

# Create Buttons
GoButton = tk.Button(information_window, text="Go", command=move, padx=10, pady=5)
GoButton.grid(row=1, column=1, padx=10, pady=5)

BackButton = tk.Button(information_window, text="Back", command=go_back, padx=10, pady=5)
BackButton.grid(row=1, column=0, padx=10, pady=5)

SleepButton = tk.Button(information_window, text="Sleep", command=sleep, padx=10, pady=5)
SleepButton.grid(row=1, column=2, padx=10, pady=5)

# Create Data Labels
information_label = tk.Label(information_window, text=destination, font=("Helvetica", 16))

move_time_label = tk.Label(information_window, text=f"Move Time:{move_time}", font=("Helvetica", 10))
move_time_label.grid(row=0, column=0, padx=10, pady=5)

#Auto Fill Blank
information_window.grid_columnconfigure(0, weight=1)
information_window.grid_columnconfigure(1, weight=1)
information_window.grid_columnconfigure(2, weight=1)

#----------------------------------------------------------------------------------------------------------------------------------------#
# Create Listbox to display items with the scrollbar
bag_listbox = tk.Listbox(root, font=("Helvetica", 12),selectmode=tk.SINGLE)
bag_listbox.grid(row=9, column=0, columnspan=3, padx=5, pady=5,sticky="w"+"e")

update_bag_labels()
def more_information(event):
    global selected_item
    text = ''
    index = bag_listbox.curselection()
    selected_item = bag_listbox.get(index)
    for i,v in item_information[selected_item].items():
        text += f"Add {v} {i} "
    more_information_label.config(text=f"""Information: {text}\nNumber: {item_number[selected_item]}""")

#Create Data Labels
more_information_label = tk.Label(root, text="\n", font=("Helvetica", 13))
more_information_label.grid(row=7, column=0,columnspan=3, padx=5, pady=5)

# 绑定选中事件到more_information函数
bag_listbox.bind('<<ListboxSelect>>', more_information)

#Create Buttons
use_button = tk.Button(root, text="Use", command=lambda : use_item(selected_item), padx=10, pady=5)
use_button.grid(row=10, column=0, columnspan=3, padx=5, pady=5)
# Create Scrollbar
bag_scrollbar = tk.Scrollbar(root)
bag_scrollbar.grid(row=9, column=2, padx=5, pady=5, sticky="e"+"n"+"s")

#Bind Listbox and Scrollbar
bag_scrollbar.config(command=bag_listbox.yview)
bag_listbox.config(yscrollcommand=bag_scrollbar.set)

#----------------------------------------------------------------------------------------------------------------------------------------#
root.mainloop()
