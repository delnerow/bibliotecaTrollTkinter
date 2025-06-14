import tkinter as tk


def createPopup(title: str, screen):
    popup = tk.Toplevel(screen)
    popup.title(title)
    tk.Button(popup, text="Close", command=popup.destroy).grid(row=6, column=0)
    return popup

def on_submit(entries, popup, catalogo):
        titulo, autor, ano_publicacao, genero, editora = [v.get() for v in entries]
        catalogo.addLivro(popup, titulo, autor, ano_publicacao, genero, editora)