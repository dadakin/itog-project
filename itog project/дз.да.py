# Импорт
import tkinter as tk
from tkinter import ttk
import sqlite3

#Главное окно
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def open_search_dialog(self):
        Search()

    def delete_records(self): #Удаление данных
        for selection_item in self.tree.selection():
            self.db.c.execute("""DELETE FROM db WHERE
            ID = ?""", (self.tree.set(selection_item, '#1'),))
            self.db.conn.commit()
            self.view_records()

    def search_records(self, name): #Поиск записи
        name = ('%' + name + '%',)
        self.db.c.execute(
            '''SELECT * FROM db WHERE name LIKE ?''', name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
        for row in self.db.c.fetchall()]

    def update_record(self, name, tel, email, salary): #Обновление/измениение данных
        self.db.c.execute('''UPDATE db SET name=?, tel=?, email=?, salary=? WHERE ID=?''',
                          (name, tel, email, salary, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def open_update_dialog(self):
        Update()

    def update_record(self, name, tel, email):
        self.db.c.execute('''UPDATE db SET name=?, tel=?, email=? WHERE ID=?''',
            (name, tel, email, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()
    #Вывод данных в виджет таблицы 
    def view_records(self): 
        #Выбор информацию из БД 
        self.db.c.execute('''SELECT * FROM db''') 
        #Удаляем все из виджета таблицы 
        [self.tree.delete(i) for i in self.tree.get_children()] 
        #Добавление в виджет таблицы всей информации из БД 
        [self.tree.insert('', 'end', values=row) 
         for row in self.db.c.fetchall()]

    def records(self, name, tel, email, salary):
        self.db.insert_data(name, tel, email, salary)
        self.view_records()
                            
    def open_dialog(self):
        Child()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7b8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='./img/add.png') 
        #Создание кнопки добавления 
        #command - функция по нажатию 
        #bg - фон 
        #bd - граница 
        #compound - ориентация текста (tk.CENTER , tk.LEFT , tk.RIGHT , tk.TOP или tk.BOTTOM.) 
        #image - иконка кнопки 
        btn_open_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.add_img, command=self.open_dialog) 
        #Упаковка и выравнивание по левому краю 
        btn_open_dialog.pack(side=tk.LEFT)
        #Добавляем Treeview 
        #columns - столбцы 
        #height - высота таблицы 
        #show='headings' скрываем нулевую (пустую) колонку таблицы 
        self.tree = ttk.Treeview(columns=('id', 'name', 'tel', 'email', 'salary'), height=45, show='headings') 
        
        
        #Добавление параметров колонкам 
        #width - ширина 
        #anchor - выравнивание текста в ячейке 
        self.tree.column("id", width=30, anchor=tk.CENTER) 
        self.tree.column("name", width=300, anchor=tk.CENTER) 
        self.tree.column("tel", width=150, anchor=tk.CENTER) 
        self.tree.column("email", width=150, anchor=tk.CENTER) 
        self.tree.column("salary", width=100, anchor=tk.CENTER) 
        
        
        #Подписи колонок 
        self.tree.heading('id', text='ID')
        self.tree.heading("name", text='ФИО') 
        self.tree.heading("tel", text='Телефон') 
        self.tree.heading("email", text='E-mail') 
        self.tree.heading("salary", text='Зап.плата')
        
        
        #Упаковка 
        self.tree.pack(side=tk.LEFT)
        
        #Создание кнопки изменения данных
        self.update_img = tk.PhotoImage(file='./img/update.png')
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e0', 
                            bd=0,image=self.update_img, 
                            command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        #Создание кнопки удаления записи
        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        bth_delete = tk.Button(toolbar, bg='#d7dbe0', bd=0,
                               image=self.delete_img,
                               command=self.delete_records)
        bth_delete.pack(side=tk.LEFT)

       #Кнопка поиска
        self.search_img = tk.PhotoImage(file='img/search.png')
        btn_search = tk.Button(toolbar, text='Поиск', bg='#d7d7d7', bd=0,
                            image=self.search_img, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        #Кнопка обновления
        self.refresh_img = tk.PhotoImage(file='img/refresh.png')
        btn_refresh = tk.Button(toolbar, text='Обновление', bg='#d7d7d7', bd=0,
                               image=self.refresh_img, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

#Класс добавления
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_Child()
        self.view = app

    def init_Child(self):
        self.title('Добавить')
        self.geometry('400x200')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        #Подписи 
        label_name = tk.Label(self, text='ФИО:') 
        label_name.place(x=50, y=50) 
        label_select = tk.Label(self, text='Телефон') 
        label_select.place(x=50, y=80) 
        label_sum = tk.Label(self, text='E-mail') 
        label_sum.place(x=50, y=110) 
        label_salary = tk.Label(self, text='Заработная плата') 
        label_salary.place(x=50, y=140) 
        
        
        #Добавление строки ввода для наименования 
        self.entry_name = ttk.Entry(self) 
        #Изменение координаты объекта 
        self.entry_name.place(x=200, y=50) 
        
        
        #Добавление строки ввода для email 
        self.entry_email = ttk.Entry(self) 
        self.entry_email.place(x=200, y=80) 
        
        
        #Добавлние строки ввода для телефона 
        self.entry_tel = ttk.Entry(self) 
        self.entry_tel.place(x=200, y=110) 
        
        #Добавление строки ввода для заработной платы 
        self.entry_salary = ttk.Entry(self) 
        self.entry_salary.place(x=200, y=140) 
        
        #Кнопка закрытия дочернего окна 
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy) 
        self.btn_cancel.place(x=300, y=170) 
        
        
        #Кнопка добавления 
        self.btn_ok = ttk.Button(self, text='Добавить') 
        self.btn_ok.place(x=220, y=170) 
        #Срабатывание по ЛКМ 
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(),                                                                     
                    self.entry_email.get(),                                                       
                    self.entry_tel.get(),
                    self.entry_salary.get()))
         
        
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db

    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(
            self.entry_name.get(),
            self.entry_tel.get(),
            self.entry_email.get()
            ))
        #Закрывам окно редактирования
        #add='+' позволяет вешать на 1 кнопку более 1 события
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute('''SELECT * FROM db WHERE id=?''', (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_tel.insert(0, row[2])
        self.entry_email.insert(0, row[3])

class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title = ("Поиск")
        self.geometry('300x300')
        self.resizable(False, False)
        
        label_search = tk.Label(self, text='Поиск по ФИО')
        label_search.place(x=15, y=20)

        self.entry_search = tk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)
        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

#Класс БД

#Создание таблиц с работниками
class DB:
  #Создание подключения к бд
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.c = self.conn.cursor()
      #Метод создания таблицы Сотрудники
        self.c.execute("""CREATE TABLE IF NOT EXISTS db (
        id INTEGER PRIMARY KEY ,
        name TEXT,
        tel TEXT,
        email TEXT,
        salary TEXT);
        """)

    def insert_data(self, name, tel, email, salary):
        self.c.execute("""INSERT INTO db(name, tel, email, salary)
        VALUES (?, ?, ?, ?)
        """, (name, tel, email, salary))
        self.conn.commit()


if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Телефонная книга') #Заголовок
    root.geometry('730x450') #Размер окна
    root.resizable(False, False) #Настройка размера
    root.mainloop()
