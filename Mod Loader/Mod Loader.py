import shutil
from tkinter import *
from tkinter import filedialog
import sqlite3
import os

def select():
    global path
    path = filedialog.askdirectory(initialdir = "/", title = "Select Main Game Folder")
    
def contin():
    global path
    
    if path != "":
        frame_1.pack_forget()
        frame_2  = Frame(root)
        loading = Label(frame_2, text = "Loading...", font = ("Monoton", 15))
        loading.pack(anchor = "center")
        frame_2.pack(fill = "both")
        main_db_path = path + "/Songs.db"
        main_songs_path = path + "/Songs/"
        
        main_songs = sqlite3.connect(main_db_path)
        main_cursor = main_songs.cursor()
        
        main_cursor.execute("SELECT COUNT(*) FROM Songs")
        next_song_no = main_cursor.fetchone()[0] + 1
        
        sub_songs = sqlite3.connect("Songs.db")
        sub_cursor = sub_songs.cursor()
        
        sub_cursor.execute("SELECT COUNT(*) FROM Songs")
        total_new_songs = sub_cursor.fetchone()[0]
        
        for i in range(0,total_new_songs):
            row = i + 1
            sub_cursor.execute("SELECT Title FROM Songs WHERE rowid = ?", (row,))
            song_title = sub_cursor.fetchone()[0]
            sub_cursor.execute("SELECT Artist FROM Songs WHERE rowid = ?", (row,))
            song_artist = sub_cursor.fetchone()[0]

            folder_path = main_songs_path + str(next_song_no)
            sample_path = "Songs/" + str(row) + "/Aud.mp3"
            cvr_path = "Songs/" + str(row) + "/Cvr.png"
            
            os.mkdir(folder_path)
            shutil.copy(sample_path, folder_path)
            shutil.copy(cvr_path, folder_path)
            
            main_cursor.execute("INSERT INTO Songs VALUES (?, ?)", (song_title, song_artist))
            main_songs.commit()
        loading = Label(frame_2, text = "Loading Complete. You Can Now Close The Program.", font = ("Monoton", 15))
        loading.pack(anchor = "center")
        frame_2.pack(fill = "both")
        


path = ""

root = Tk()
root.geometry("500x150")
root.title("Install DLC 1")

frame_1 = Frame(root, padx = 10, pady = 10)
frame_1.rowconfigure(0)
frame_1.rowconfigure(1)
frame_1.rowconfigure(2)

install_txt = Label(frame_1, text = "Install DLC To:", font = ("Monoton", 15, "bold"))
install_txt.pack(anchor = "w", expand = True, fill = "x")

select_path = Button(frame_1, text = "Select Folder", command = select, font = ("Monoton", 10), anchor = "center", justify = "center")
select_path.pack(anchor = "center", expand = True, fill = "x", pady = 10)

cont = Button(frame_1, text = "Continue", command = contin, font = ("Monoton", 10), anchor = "center", justify = "center")
cont.pack(anchor = "center", expand = True, fill = "x")

frame_1.pack(fill = "x")

root.mainloop()