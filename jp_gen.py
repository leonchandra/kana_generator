import re
import random
import tkinter as tk
from tkinter import filedialog
import jaconv
from PIL import ImageGrab
from datetime import datetime
import os


file_name = "jp.txt"

# hiragana = ["んー", "あいうえお", "かきくけこ", "さしすせそ", "たちつってと", "なにぬねの", "はひふへほ", "まみむめも", 
#            "らりるれろ", "やゆよ",  "わを"]
# dakuten_hiragana = ["がぎぐげご", "ざじずぜぞ", "だぢづでど", "ばびぶべぼ"]
# handakuten_hiragana = ["ぱぴぷぺぽ"]
smol_hiragana = ["ゃゅょ", "ぁぃぅぇぉ"]

# all_hiragana = hiragana + dakuten_hiragana + handakuten_hiragana + smol_hiragana
# print(len(all_hiragana))
# print(all_hiragana)
all_hiragana = ["んー", "あいうえお", "かきくけこ", "さしすせそ", "たちつってと", 
                "がぎぐげご", "ざじずぜぞ", "だぢづでど",
                "なにぬねの", "はひふへほ", "ばびぶべぼ", "ぱぴぷぺぽ",
                "まみむめも", "らりるれろ", "やゆよ",  "わを"] + smol_hiragana
# print(all_hiragana)
# print(len(all_hiragana))

katakana = ["ンー", "アイウエオ", "カキクケコ", "サシスセソ", "タチツッテト", "ナニヌネノ", "ハヒフヘホ", 
            "マミムメモ", "ヤユヨ", "ラリルレロ", "ワヲ"]
dakuten_katakana = ["ガギグゲゴ", "ザジズゼゾ", "ダヂヅデド", "バビブベボ"]
handakuten_katakana = ["パピプペポ"]

jp_text = open(file_name, encoding='utf-8').read()

# Split the text by lines and then split each line by spaces
parsed_hk = [line.split()[2] for line in jp_text.splitlines()]

# Split jp_text into array of hiragana
jp_words = parsed_hk
list_words = []
for i in range(len(all_hiragana)):
    learned = "".join(all_hiragana[0:i+1])
    pattern = f'^[{learned}]+$'
    find_words = [word for word in jp_words if re.search(pattern, word)]
    jp_words = [word for word in jp_words if word not in find_words]

    filtered_words = [word for word in find_words if len(word) > 2]
    list_words.append(sorted(filtered_words, key=len, reverse=True))
    

# Canvas
class Whiteboard:
    def __init__(self, root, width, height, free_height):
        self.root = root
        # self.root.title("Tkinter Whiteboard")

        # Create the Canvas
        self.canvas = tk.Canvas(self.root, bg="white", width=width, height=height, borderwidth=1, relief="solid")
        self.canvas.grid(row = 0, column=amount_col+1, rowspan=7, sticky='nsew', pady=(0,5))

        # Initialize drawing state and stacks for undo/redo
        self.old_x = None
        self.old_y = None
        self.pen_color = "black"
        self.actions = []  # To store actions (lines) for undo/redo
        self.redo_stack = []

        # Bind mouse events to the canvas
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

        # Bind keyboard shortcuts
        self.root.bind_all('<Control-z>', self.undo)
        self.root.bind_all('<Control-y>', self.redo)
        self.root.bind_all('<Control-n>', self.clear_and_save)

        # Create color palette
        self.create_color_palette()

    def create_color_palette(self):
        colors = ['black', 'red', 'green', 'blue', 'yellow', 'orange', 'purple', 'brown', 'gray']
        for color in colors:
            color_button = tk.Button(self.root, bg=color, command=lambda c=color: self.change_color(c), width=2)
            #color_button.pack(side=tk.LEFT)

    def change_color(self, new_color):
        self.pen_color = new_color

    def draw(self, event):
        if self.old_x and self.old_y:
            # Draw a line from the last position to the current position
            line = self.canvas.create_line(self.old_x, self.old_y, event.x, event.y, width=3, fill=self.pen_color, capstyle=tk.ROUND, smooth=tk.TRUE)
            # Save the line action (starting and ending coordinates, color) for undo
            self.actions.append(('line', self.old_x, self.old_y, event.x, event.y, self.pen_color))
            self.redo_stack.clear()  # Clear the redo stack when drawing a new line
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        # Reset the drawing state when the mouse button is released
        self.old_x = None
        self.old_y = None

    def undo(self, event=None):
        if self.actions:
            last_action = self.actions.pop()
            self.redo_stack.append(last_action)
            self.redraw_canvas()

    def redo(self, event=None):
        if self.redo_stack:
            action_to_redo = self.redo_stack.pop()
            self.actions.append(action_to_redo)
            self.redraw_canvas()

    def clear_and_save(self, event=None):
        # Save the current canvas to an image
        # self.save_canvas_as_image("whiteboard_image.png")
        # self.save_canvas_as_image("whiteboard_image.png")

        # # List all files in the directory
        # directory = filedialog.askdirectory()
        # files = os.listdir(directory)

        # # Extract files with the current date prefix and find the highest number
        # current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # prefix = current_time
        # numbers = [int(f.split('_')[-1].split('.')[0]) for f in files if f.startswith(prefix) and f.split('_')[-1].split('.')[0].isdigit()]
        # latest_number = max(numbers) if numbers else 0

        # Clear the canvas
        self.canvas.delete("all")
        # Clear undo/redo stacks
        self.actions.clear()
        self.redo_stack.clear()

    def save_canvas_as_image(self, filename):
        # Save the current canvas as an image using PIL
        self.canvas.update()
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        ImageGrab.grab(bbox=(x, y, x + width, y + height)).save(filename)

    def redraw_canvas(self):
        self.canvas.delete("all")
        for action in self.actions:
            if action[0] == 'line':
                _, x1, y1, x2, y2, color = action
                self.canvas.create_line(x1, y1, x2, y2, width=3, fill=color, capstyle=tk.ROUND, smooth=tk.TRUE)

# GUI
def close_window(event=None):
    root.destroy()

def toggle_canvas(window, width, height, wb_width, wb_height):
    # if (window.winfo_width() != width & window.winfo_height() != height):

    if (window.canvas == "T"):
        # window.geometry(f"{width}x{height}")
        center_window(window, width, height)
        window.canvas = "F"
    else:
        # window.geometry(f"{width+wb_width}x{wb_height}")
        center_window(window, width+wb_width, wb_height)
        window.canvas = "T"

# Function to center the window on the screen
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x_coordinate = int((screen_width / 2) - (width / 2))
    y_coordinate = int((screen_height / 2) - (height / 2))
    
    window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")


def generate_words(a = ""):
    if (var_type.get() == "Type"): # No option selected
        return
    
    index = option_hiragana.index(var_type.get()) + 1 # Do not care about ん/ー

    global selected_words
    selected_words = []
    global question_amount
    if (len(list_words[index])) < question_amount:
        question_amount = len(list_words[index])

    while len(selected_words) in range(question_amount):
        selected_words.append(random.choice(list_words[index]))
        selected_words = list(set(selected_words))

    global ans_type
    # ans_type = type + ans_type
    # print(ans_type)
    ans = get_answer(selected_words, type + ans_type)
    
    selected_ques = selected_words
    if (type == 0):
        selected_ques = [jaconv.kana2alphabet(word) for word in selected_words]
    elif (type == 2):
        selected_ques = [jaconv.hira2kata(word) for word in selected_words]
    
    for i in range(question_amount):
        question[i].config(text=f"{selected_ques[i]}")#, ("question"))
        answer[i].config(text=f"{ans[i]}")
        answer[i].grid_forget()

        word_length = len(selected_ques[i])
        if (type > 0):
            if (word_length < 5):
                question[i].config(font=("Noto Sans CJK", 45))
            else:
                resize = min(25, 5 * (word_length - 4))
                question[i].config(font=("Noto Sans CJK", 45 - resize))
            # elif (word_length == 5):
            #     question[i].config(font=("Noto Sans CJK", 40))
            # elif (word_length == 6):
            #     question[i].config(font=("Noto Sans CJK", 30))
            # elif (word_length == 7):
            #     question[i].config(font=("Noto Sans CJK", 25))
            # elif (word_length > 7):
            #     question[i].config(font=("Noto Sans CJK", 20))
        else:
            if (word_length > 6):
                question[i].config(font=("Noto Sans CJK", 35))
            else:
                question[i].config(font=("Noto Sans CJK", 45))
        
def show_answer(question_index):
    # Can you grid_forget() to remove completely, but need to reapply grid()
    # this_question = question[question_index]
    
    # this_text = this_question.cget("text")
    # key = answer[question_index]

    # if (type == 0):
    #     converted = this_text

    # key.config(text=converted)
    # this_question.unbind("<Button-1>")
    # this_question.unbind(f"<Key-{question_index + 1}>")
    # answer.grid_
    
    answer[question_index].grid(row=int(question_index / 3) + 3, column=question_index % 3, pady=(30, 0)) 

    
def show_all(a):
    for i in range(question_amount):
        answer[i].grid(row=int(i / 3) + 3, column=i % 3, pady=(30, 0)) 

def change_type(a, b, c):
    #print(a, b, c) -> PY_VAR1 write
    
    global type
    # print(option_select)
    type = option_select.index(var_select.get())
    # print(type)
 
def change_mode(a):
    # print(a) -> <KeyPress event send_event=True state=Control keysym=d keycode=68 char='\x04' x=500 y=77>
    global ans_type, type, question_amount
    if (ans_type == 0):
        ans_type = 10
    else:
        ans_type = 0

    tipe = ans_type + type

    # if (tipe == 1 or tipe == 12):
    #     fcn = "jaconv."
    # elif (tipe < 10):
    #     fcn = "jaconv.kana2alphabet"
    # else:
    #     fcn = "jaconv.kata"
    # # jaconv.

    # print(ans_type)
    # print(type+ans_type)
    local_selected = selected_words
    ans = get_answer(local_selected, type + ans_type)
    for i in range(question_amount):
        # eval(answer[i].cget("text"))
        # answer[i].config(text=f"{[i]}") v copied.
        # print("Hi")
        # print(ans[i])
        answer[i].config(text=f"{ans[i]}")

def get_answer(selected_words, ans_type):
    # 0,1,2 -> Romaji, Hira, Kata
    # print(ans_type)
    # print(selected_words[0])
    if (ans_type == 1 or ans_type == 12):
        # print("1")
        return [jaconv.kana2alphabet(word) for word in selected_words]
    elif (ans_type < 10):
        # print("2")
        return selected_words

    # print("3")
    return [jaconv.hira2kata(word) for word in selected_words]



# Create the main window
root = tk.Tk()
root.title("Japanese Test")

# Whiteboard size
whiteboard_height = 500
whiteboard_width = 500
wb_free_height = 50
root.canvas = "F"

# Set the window size (width x height)
question_size = 300
# window_width = question_size * 3 +whiteboard_width
# window_height = whiteboard_height + wb_free_height
window_width = question_size * 3
window_height = whiteboard_height + wb_free_height

# Center the window on the screen
center_window(root, window_width, window_height)




# Column for questions
amount_col = 3
pad_between = 80
y_between = 40
index = 0
type = 0
ans_type = type
question_amount = 9


instruction = tk.Label(root, text="Ctrl + C: Open canvas"
                       "\nCtrl + N: Clear canvas"
                       "\nCtrl + D: Change answer type"
                       "\nCtrl + G: Generate"
                       "\nCtrl + A: Show All"
                       "\n1~9      : Show Answer",
                       font=("Arial", 10), justify="left")
instruction.grid(row = 0, rowspan=2, sticky="nw")

label = tk.Label(root, text="Japanese Word Generator",
                 font=("Times New Roman", 16),
                 anchor="center")
label.grid(row = 0, columnspan = amount_col)


button = tk.Button(root, text="Generate", command=generate_words, 
                   font=("Arial", 14),
                   width=20)
button.grid(row = 1, columnspan = amount_col, rowspan=2, pady=(0, 0))#, ipady=10)#, sticky="s")


# Dropdowns variable
var_type = tk.StringVar(root)
var_type.set("Type")  # Set default value

var_select = tk.StringVar(root)
var_select.set("ローマ字")
var_select.trace_add("write", change_type)

var_ans = tk.StringVar(root)
var_ans.set("")

# Create the dropdown menu
option_select = ["ローマ字", "ひらがな", "カタカナ"]
option_hiragana = ["あ", "か", "さ", "た", "が", "ざ", "だ", 
                   "な", "は", "ば", "ぱ",
                   "ま", "ら", "や", "わ", 
                   "ゃゅょ", "ぁぃぅぇぉ"]
option_katakana = ['ア', 'カ', 'サ', 'タ', 'ナ', 'ハ', 'マ', 'ラ', 'ヤ', 'ワ']

dropdown_selection = tk.OptionMenu(root, var_select, *option_select)
dropdown_selection.grid(row = 1, columnspan=amount_col, pady=(0, y_between * 2), padx=(0, pad_between))

dropdown_type = tk.OptionMenu(root, var_type, *option_hiragana)
dropdown_type.grid(row = 1, columnspan=amount_col,  pady=(0, y_between * 2), padx=(pad_between, 0))

dropdown_ans = tk.OptionMenu(root, var_ans, *option_katakana)


# Question spouting
question = []
answer = []
for i in range(question_amount):
    question_label = tk.Label(root, font=("Noto Sans CJK", 45)) #, bg="lightgray",
                     #borderwidth=2, relief="solid")
    question_label.grid(row= int(i / 3) + 3, column=i % 3, pady= (0, 60), sticky="nesw") 
    question.append(question_label)

    answer_label = tk.Label(root, font=("Noto Sans CJK", 20))
    answer.append(answer_label)

    question[i].bind("<Button-1>", lambda event, index=i: show_answer(index))

    # Will not work for question > 9
    key_num = i + 1
    root.bind(f"<Key-{key_num}>", lambda event, index=i: show_answer(index))

#question[len(question) - 1].grid(pady= (0,80))

# root.bind('<FocusOut>', close_window)
root.bind('<Control-d>', change_mode)
root.bind('<Control-a>', show_all)
root.bind('<Control-g>', generate_words)
label_dummy = tk.Label(root, text="")
label_dummy.grid(row = 6, columnspan=amount_col)#, pady = (0, 800))

for i in range(amount_col):
    root.grid_columnconfigure(i, weight = 1, minsize=question_size)
# root.grid_columnconfigure(2, weight = 0)
root.grid_rowconfigure(3, minsize=130)
root.grid_rowconfigure(4, minsize=130)
root.grid_rowconfigure(5, minsize=130)
root.grid_rowconfigure(2, minsize=0)
# root.grid_rowconfigure(5, weight = 1)
#root.grid_rowconfigure(5, pady = (0, 50))

whiteboard = Whiteboard(root, whiteboard_width, whiteboard_height + wb_free_height, wb_free_height)

root.bind_all('<Control-c>', lambda event: toggle_canvas(root, window_width, window_height, whiteboard_width, whiteboard_height + wb_free_height))

# Start the main event loop
root.mainloop()

# Analysis Length
# sum = 0
# print([sum == sum + length for length in [len(word_list) for word_list in list_words]])
# print([length for length in [len(word_list) for word_list in list_words]])
# for i in [len(word_list) for word_list in list_words]:
#     sum = sum + i
# print(sum)
# print(len(list_words[1]))

# Text data:
# 4999 + 4591
# == 1 -> 1099
# ん　あ　　か　さ　　た　　な　　は　ま　　ら　　や　　わ　　が　　ざ　だ　　ば　　ぱ　ゃゅょ
# [0, 10,  93, 203, 355,  98, 203, 219,  498, 217,  87, 344, 295, 273, 292,  55,  891]        ぁ
# [0, 15, 178, 356, 662, 214, 396, 463, 1042, 359, 164, 679, 598, 617, 583, 234, 1931] [1847, 84]
#                                                                 inc  dec