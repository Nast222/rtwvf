import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

FILENAME = 'movies.json'

def load_movies():
    if os.path.exists(FILENAME):
        with open(FILENAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_movies(movies):
    with open(FILENAME, 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)

def add_movie():
    title = entry_title.get().strip()
    genre = entry_genre.get().strip()
    year = entry_year.get().strip()
    rating = entry_rating.get().strip()

    if not title or not genre or not year or not rating:
        messagebox.showwarning('Ошибка', 'Заполните все поля!')
        return

    if not year.isdigit() or int(year) < 1888 or int(year) > 2100:
        messagebox.showerror('Ошибка', 'Год должен быть числом (1888-2100)!')
        return

    if not (rating.replace('.', '', 1).isdigit() and 0 <= float(rating) <= 10):
        messagebox.showerror('Ошибка', 'Рейтинг должен быть числом от 0 до 10!')
        return

    movies.append({
        'title': title,
        'genre': genre,
        'year': int(year),
        'rating': float(rating)
    })
    save_movies(movies)
    update_treeview()
    clear_entries()

def clear_entries():
    entry_title.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_year.delete(0, tk.END)
    entry_rating.delete(0, tk.END)

def update_treeview(filtered=None):
    for i in tree.get_children():
        tree.delete(i)
    data = filtered if filtered else movies
    for m in data:
        tree.insert('', tk.END, values=(m['title'], m['genre'], m['year'], m['rating']))

def filter_movies():
    genre = entry_filter_genre.get().strip().lower()
    year = entry_filter_year.get().strip()
    filtered = movies

    if genre:
        filtered = [m for m in filtered if genre in m['genre'].lower()]

    if year.isdigit():
        filtered = [m for m in filtered if m['year'] == int(year)]

    update_treeview(filtered)

# Загрузка данных при запуске
movies = load_movies()

# Основное окно
root = tk.Tk()
root.title('Movie Library')
root.geometry('700x500')

# Вкладки (для удобства)
tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Добавить фильм')
tab_control.add(tab2, text='Фильтрация')
tab_control.pack(expand=1, fill='both')

# Вкладка 1: Добавление фильма
tk.Label(tab1, text='Название:').grid(row=0, column=0, padx=5, pady=5)
entry_title = tk.Entry(tab1, width=40)
entry_title.grid(row=0, column=1, padx=5, pady=5)

tk.Label(tab1, text='Жанр:').grid(row=1, column=0, padx=5, pady=5)
entry_genre = tk.Entry(tab1, width=40)
entry_genre.grid(row=1, column=1, padx=5, pady=5)

tk.Label(tab1, text='Год:').grid(row=2, column=0, padx=5, pady=5)
entry_year = tk.Entry(tab1, width=40)
entry_year.grid(row=2, column=1, padx=5, pady=5)

tk.Label(tab1, text='Рейтинг:').grid(row=3, column=0, padx=5, pady=5)
entry_rating = tk.Entry(tab1, width=40)
entry_rating.grid(row=3, column=1, padx=5, pady=5)

tk.Button(tab1, text='Добавить фильм', command=add_movie).grid(row=4, columnspan=2, pady=10)

# Таблица фильмов
tree = ttk.Treeview(root, columns=('title', 'genre', 'year', 'rating'), show='headings')
tree.heading('title', text='Название')
tree.heading('genre', text='Жанр')
tree.heading('year', text='Год')
tree.heading('rating', text='Рейтинг')
tree.column('title', width=200)
tree.column('genre', width=120)
tree.column('year', width=80)
tree.column('rating', width=80)
tree.pack(pady=10)
update_treeview()

# Вкладка 2: Фильтрация
tk.Label(tab2, text='Жанр:').grid(row=0, column=0, padx=5, pady=5)
entry_filter_genre = tk.Entry(tab2, width=40)
entry_filter_genre.grid(row=0, column=1, padx=5, pady=5)

tk.Label(tab2, text='Год:').grid(row=1, column=0, padx=5, pady=5)
entry_filter_year = tk.Entry(tab2, width=40)
entry_filter_year.grid(row=1, column=1, padx=5, pady=5)

tk.Button(tab2, text='Фильтровать', command=filter_movies).grid(row=2, columnspan=2, pady=10)

root.mainloop()
