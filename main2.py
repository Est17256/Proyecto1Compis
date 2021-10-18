from tkinter import *
from tkinter import filedialog
from main import *
root=Tk()
root.title("Proyecto 2")
root.geometry("1000x1000")

# def load_error():
#     pop=Tk()
#     my_text=Text(pop, width=60,height=10,font=("helvetica",16))
#     my_text.pack(pady=20)
#     text_file="C:/Users/lcest/Desktop/FinalCompis/error.txt"
#     text_file=open(text_file,'r')
#     stuff=text_file.read()
#     my_text.insert(END,stuff)
#     text_file.close()

# def load_table():
    
#     pop=Tk()
#     my_text=Text(pop, width=60,height=10,font=("helvetica",16))
#     my_text.pack(pady=20)
#     text_file="C:/Users/lcest/Desktop/FinalCompis/tabla.txt"
#     text_file=open(text_file,'r')
#     stuff=text_file.read()
#     my_text.insert(END,stuff)
#     text_file.close()
def load_inter():
    
    pop=Tk()
    my_text=Text(pop, width=60,height=40,font=("helvetica",16))
    my_text.pack(pady=20)
    text_file="inter.txt"
    text_file=open(text_file,'r')
    stuff=text_file.read()
    my_text.insert(END,stuff)
    text_file.close()

def open_txt():
    text_file= filedialog.askopenfilename(initialdir="./", title="Open FIle",filetypes=(("txt","*.txt"),))
    text_file=open(text_file,'r')
    stuff=text_file.read()
    my_text.insert(END,stuff)
    text_file.close()

def save_txt():
    text_file= filedialog.askopenfilename(initialdir="./", title="Save File",filetypes=(("txt","*.txt"),))
    text_file=open(text_file,'w')
    text_file.write(my_text.get(1.0,END))
    text_file.close()

def select_txt():
    text_file= filedialog.askopenfilename(initialdir="./", title="Execute FIle",filetypes=(("txt","*.txt"),))
    print(text_file)
    main(text_file)


my_text=Text(root, width=60,height=30,font=("helvetica",16))
my_text.pack(pady=20)


open_button=Button(root,text="Open File", command=open_txt)
open_button.pack(pady=10)
save_button=Button(root,text="Save File", command=save_txt)
save_button.pack(pady=10)
start_button=Button(root,text="Execute File", command=select_txt)
start_button.pack(pady=10)
start_button=Button(root,text="Intermedio", command=load_inter)
start_button.pack(pady=10)



root.mainloop()