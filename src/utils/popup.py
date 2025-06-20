import tkinter as tk


def createPopup(title: str, screen):
    popup = tk.Toplevel(screen)
    popup.title(title)
    tk.Button(popup, text="Fechar", command=popup.destroy).grid(row=6, column=0)
    return popup

def on_submit(entries, popup, catalogo, close_popup=None):
        titulo, autor, ano_publicacao, genero, editora = [v.get() for v in entries]
        catalogo.addLivro(popup, titulo, autor, ano_publicacao, genero, editora)
        if close_popup:
            close_popup()
        else:
            popup.destroy()

def off_submit(entries, popup, catalogo, close_popup=None):
    titulo, autor, ano_publicacao, genero, editora, new_id, old_id = [v.get() for v in entries]
    catalogo.update_finish(popup, titulo, autor, ano_publicacao, genero, editora, new_id, old_id)
    if close_popup:
        close_popup()
    else:
        popup.destroy()