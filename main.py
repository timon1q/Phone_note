import tkinter as tk
from tkinter import ttk
import sqlite3


# ГЛАВНОЕ ОКНО
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # РАБОТА ГЛАВНОГО ОКНА
    def init_main(self):
        # ПАНЕЛЬ ИНСТРУМЕНТОВ
        toolbar = tk.Frame(bg='#d7d7d7', bd = 2)
        # ОФОРМЛЕНИЕ
        toolbar.pack(side=tk.TOP, fill=tk.X)
# КНОПКИ

        # ДОБАВЛЕНИЕ
        self.img_add = tk.PhotoImage(file='./img/add.png')
        btn_add = tk.Button(toolbar, text = 'Добавить', bg='#d7d7d7',
                            bd=0, image=self.img_add, command=self.open_child)
        btn_add.pack(side = tk.LEFT)

        # ИЗМЕНЕНИЕ
        self.update_img = tk.PhotoImage(file='./img/update.png')
        btn_edit = tk.Button(toolbar, text = 'Изменить', bg='#d7d7d7',
                            bd=0, image=self.update_img, command=self.open_update_dialog)
        btn_edit.pack(side = tk.LEFT)

        # УДАЛЕНИЕ
        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        btn_edit = tk.Button(toolbar, text = 'Изменить', bg='#d7d7d7',
                            bd=0, image=self.delete_img, command=self.delete_records)
        btn_edit.pack(side = tk.LEFT)

        # ПОИСК
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, text = 'Изменить', bg='#d7d7d7',
                            bd=0, image=self.search_img, command=self.open_search)
        btn_search.pack(side = tk.LEFT)

        # ОБНОВЛЕНИЕ
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, text = 'Изменить', bg='#d7d7d7',
                            bd=0, image=self.refresh_img, command=self.view_records)
        btn_refresh.pack(side = tk.LEFT)

        # ТАБЛИЦА ДАННЫХ
        # ДОБАВИТЬ СТОЛБЕЦ
        self.tree = ttk.Treeview(self, 
                                 columns=('ID', 'name', 'phone', 'email', 'zp'),
                                 height=45, 
                                 show='headings')
        
        # РАЗМЕРЫ И ВЫРАВНИВАНИЕ
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('phone', width=100, anchor=tk.CENTER)
        self.tree.column('email', width=100, anchor=tk.CENTER)
        self.tree.column('zp', width=90, anchor=tk.CENTER)
        # НАИМЕНОВАНИЯ
        self.tree.heading('ID', text='id')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('zp', text='Зарплата')
        self.tree.pack(side=tk.LEFT)
        # СКРОЛЛИНГ
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # МЕТОДЫ
    # ДОБАВЛЯЕМ ДАННЫЕ
    def records(self, name, phone, email, zp):
        self.db.insert_data(name, phone, email, zp)
        self.view_records()
    # ИЗМЕНЕНИЕ ДАННЫХ
    def update_record(self, name, phone, email, zp):
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute("UPDATE users SET name=?, phone=?, email=?, zp=? WHERE ID=?",
                            (name, phone, email, zp, id))
        self.db.conn.commit()
        self.view_records()
    # ВИДЖЕТ ТАБЛИЦЫ
    def view_records (self):
        self.db.cur.execute('''SELECT * FROM users ''')
        # УДАЛИТЬ
        [self.tree.delete(i) for i in self.tree.get_children()]
        # ДОБАВИТЬ
        [self.tree.insert('','end', values=row)
         for row in self.db.cur.fetchall()]
    # УДАЛИТЬ ЗАПИСИ
    def delete_records(self):
        #ЦИКЛ ПО ЗАПИСЯМ
        for selecetion_item in self.tree.selection():
            #УДАЛИТЬ ИЗ БД
            self.db.cur.execute('''DELETE FROM users WHERE ID=?''',
                                (self.tree.set(selecetion_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    # ПОИСК ЗАПИСИ
    def search_records(self, name):
        name = ('%' + name + '%')
        self.db.cur.execute(
            '''SELECT * FROM users WHERE name LIKE ?''', (name, ))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('','end', values=row)
         for row in self.db.cur.fetchall()]

    # ВЫЗВАТЬ ДОЧЕРНЕЕ ОКНО
    def open_child(self):
        Child()

    # ВЫЗОВ ОКНА ИЗМЕНЕНИЯ
    def open_update_dialog(self):
        Update()

    # ВЫЗОВ ОКНА ПОИСКА
    def open_search(self):
        Search()

    # ОКНО ДОБАВЛЕНИЯ
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

     # АКТИВАЦИЯ ВИДЖЕТОВ
    def init_child(self):
        # ЗАГОЛОВОК
        self.title('Добавление контакта')
        # РАЗМЕР
        self.geometry('400x220')
        # ОГРАНИЧИТЕЛЬ
        self.resizable(False, False)
        # ПЕРЕХВАТ СОБЫТИЙ
        self.grab_set()
        # ЗАХВАТ ФОКУСА
        self.focus_set()

        # ТЕКСТ
        label_name = tk.Label(self, text='ФИО: ')
        label_name.place(x=50, y=50)
        label_phone = tk.Label(self, text='Телефон: ')
        label_phone.place(x=50, y=80)
        label_email = tk.Label(self, text='E-mail: ')
        label_email.place(x=50, y=110)
        label_zp = tk.Label(self, text='Зарплата: ')
        label_zp.place(x=50, y=140)
        # ВИДЖЕТЫ ВВОДА
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200, y=80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)
        self.entry_zp = ttk.Entry(self)
        self.entry_zp.place(x=200, y=140)


        # ЗАКРЫТИЕ ДОЧЕРНЕГО ОКНА
        self.btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=200, y=180)

        # ДОБАВЛЕНИЕ ЗАПИСИ
        self.btn_add = tk.Button(self, text='Добавить')
        self.btn_add.place(x=265, y=150)
        self.btn_add.bind('<Button-1>', lambda event:
                    self.view.records(self.entry_name.get(),
                                       self.entry_phone.get(),
                                       self.entry_email.get(),
                                       self.entry_zp.get()))


# РЕДАКТИРОВАНИЕ КОНТАКТОВ
class Update(Child):
        
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title ('Редактировать позицию')
        self.btn_add.destroy()

        self.btn_edit = ttk.Button(self, text="Редактировать")
        self.btn_edit.place(x=265, y=180)
        self.btn_edit.bind('<Button-1>', lambda event:
                    self.view.update_record(self.entry_name.get(),
                                            self.entry_phone.get(),
                                            self.entry_email.get(),
                                            self.entry_zp.get()))
        self.btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')

    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cur.execute(''' SELECT * FROM users WHERE ID=?''', (id, ))
        # ПОЛУЧАЕМ ДОСТУП К ПЕРВОЙ ЗАПИСИ
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_zp.insert(0, row[4])

class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Поиск по контактам')
        self.geometry('300x100')
        self.resizable(False,False)
        self.grab_set()
        self.focus_set()
        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=20, y=20)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=70, y=20)

        self.btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=200, y=70)

        self.btn_add = tk.Button(self, text='Найти')
        self.btn_add.place(x=150, y=70)
        self.btn_add.bind('<Button-1>', lambda event: self.view.search_records(self.entry_name.get()))




# БД
class DB:
    def __init__(self):
        # СОЕДИНЕНИЕ С БД
        self.conn = sqlite3.connect('contacts.db')
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                phone TEXT,
                                email TEXT,
                                zp TEXT) """)
        self.conn.commit()

    def insert_data(self, name, phone, email, zp):
        self.cur.execute(""" INSERT INTO users (name, phone, email, zp)
                             VALUES(?, ?, ?)""", (name, phone, email, zp))
        self.conn.commit()


# ПРИ ЗАПУСКЕ ПРОГРАММЫ
if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Журнал')
    root.geometry('800x500')
    root.configure(bg ='white')
    root.resizable(False, False)
    root.mainloop()


