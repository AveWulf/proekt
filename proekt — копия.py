
import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

from django import db
# класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()
############################
    # Создание и работа  с главным окном
    def init_main(self):
        toolbar = tk.Frame(bg='#d7d7d7', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
########################################## КНОПКИ

    #Добавить
        self.add_img = tk.PhotoImage(file='./img/add.png')
        btn_add = tk.Button(toolbar, bg='#d7d7d7', bd=1,
                            image=self.add_img, command=self.open_child)
        btn_add.pack(side=tk.LEFT)    

        #Обновить
        self.upd_img = tk.PhotoImage(file='./img/update.png')
        btn_upd = tk.Button(toolbar, bg='#d7d7d7', bd=1,
                            image=self.upd_img, command=self.open_child)
        btn_upd.pack(side=tk.LEFT)
        
        #Удалить
        self.del_img = tk.PhotoImage(file='./img/del.png')
        btn_del = tk.Button(toolbar, bg='#d7d7d7', bd=1,
                            image=self.upd_img, command=self.open_child)
        btn_del.pack(side=tk.LEFT   )
        
        #поиск      
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d7d7', bd=1,
                            image=self.upd_img, command=self.open_child)
        btn_search.pack(side=tk.LEFT)

        # ОБНОВИТЬ
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d7d7', bd=1,
                                image=self.upd_img, command=self.open_child)
        btn_refresh.pack(side=tk.LEFT)
       
    ################################# cоздание таблицы
        #добавляем столбцы
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'phone', 'email'),
                                 height=45, show='headings')
        
        # Добавить параметры  колонкам
        self.tree.column('ID',width=45, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        
        #ПОдписи колонок
        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='E-mail')

        #Упаковка
        self.tree.pack(side=tk.LEFT)
       
        #Ползунок
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

#####################################Все методы
    
    def records(self, name, phone, email):
        self.db.insert_data(name, phone, email)
        self.view_records()

    #Отображение данных в Treeview    
    def view_records(self):
        self.db.cur.execute(""" SELECT * FROM users """)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
         for row in self.db.cur.fetchall()]

     # Метод обновления данных   
    def update_record(self, name, phone, email):
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute(""" UPDATE users SET name=?, phone=?, email=? WHERE ID=? """
                            (name, phone, email, id))
        self.db.conn.commit()
        self.view_records()
    
    #Метод для удаления данных
    def delete_records(self):
        for row in self.tree.selection():
            self.db.cur.execute(""" DELETE FROM users WHERE ID=? """,  
                                (self.tree.set(row, '#1'),) )
            self.db.conn.commit()
            self.view.records()   
        
        #Метод для поиска данных
    def search_records(self, name):
        name = ('%' + name + '%')
        self.db.cur.execute("""SELECT * FROM users WHERE name LIKE ?""", (name, ))

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
        for row in self.db.cur.fetchall()]    
    
 #####################################Вызов классов
    
            # Метод вызывающий окно добалве ния
    def open_child(self):
        Child() 

            #Метод вызывающий окно редактирования
    def open_update_dialog(self):
        Update()

    #  Метод вызывающий окно поиска
    def open_search(self):
        Update()     
##############################################
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child() 
        self.view = app  

    def init_child(self):
        self.title('Добавить контакт')
        self.geometry('400x220')
        self.resizable(False,False)
        self.grab_set()
        self.focus_get()    
##################################
        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50)
        label_phone = tk.Label(self, text='Телефон: ')
        label_phone.place(x=50, y=80)
        label_email = tk.Label(self, text='E-mail: ')
        label_email.place(x=50, y=110)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200, y=80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y =110)

        label_name = tk.Label(self, text='ФИО: ')
        label_name.place(x=50, y=50)
        label_phone = tk.Label(self, text='Телефон: ')
        label_phone.place(x=50, y=80)
        label_email = tk.Label(self, text='E-mail: ')
        label_email.place(x=50, y=110)


        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        self.btn_add = ttk.Button(self)
        self.btn_add.place(x=220, y=170)
        self.btn_add.bind('<Button-1>', lambda event:
                          self.view.records(self.entry_name.get(),
                                            self.entry_email.get(),
                                            self.entry_phone.get()))

###########################################

class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()


    def init_upgrade(self):
        self.title('Редактировать позицию')
        self.btn_add.destroy()

        self.but_upd = ttk.Button(self, text='Редактировать')
        self.but_upd.bind('<Button-1>', lambda event:
                          self.view.update_record(self.entry_name.get(),
                                                  self.entry_phone.get(),
                                                  self.entry_email.get()))
        self.but_upd.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.but_upd.place(x=200, y=170)
        
    def default_data(self):
        selected_item = self.view.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Закройте окно редактирования и выберите контактю")
            return
        
        
        id = self.view.tree.set(self.viev.tree.selection()[0], '#1')
        self.db.cur.execute(""" SELECT * FROM users WHERE ID=? """, (id, ))

        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_name.insert(0, row[1])
        self.entry_name.insert(0, row[1])

        
###############################################

# Класс поиска контакта

class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск по контактам')
        self.geometry('300x100')
        self.resizable(False,False)
        self.grab_set()
        self.focus_get()

        label_name= tk.Label(self, text='ФИО')
        label_name.place(x=20, y=20)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=70, y=20)

      #Кнопка закрытия

        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=200, y=70)
      #Кнопка поиска
        self.btn_search = ttk.Button(self, text='Найти')
        self.btn_search.place(x=70, y=70)
        self.btn_search.bind('<Button-1>', lambda event:    
                                self.view.search_records(self.entry_name.get()))
        self.btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')          

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('contacts.db')
        self.cur = self.conn.cursor()
        self.cur.execute(""" CREATE TABLE IF NOT EXISTS users(
                                id INTEGER PRIMARY KEY NOT NULL,
                                name TEXT,
                                phone TEXT,
                                email TEXT )""")   
        self.conn.commit()

    def insert_data (self, name, phone, email):
        self.cur.execute(""" INSERT INTO users (name, phone, email)
                         VALUES (?, ?, ?)"""    , (name, phone, email))
        self.conn.commit()
##################################
if __name__ == '__main__':
        root = tk.Tk()
        app= Main(root)
        app.pack()
        root.title('Телефонная книга')
        root.geometry('645x450')
        root.resizable(False,False)
        root.configure(bg='White')
        root.mainloop()

        
