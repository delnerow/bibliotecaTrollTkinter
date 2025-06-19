import random
import tkinter as tk
from PIL import Image, ImageTk

from src.utils.popup import createPopup, off_submit, on_submit

class Livro:
    def __init__(self, id: int, titulo: str, ano_publicacao: int, genero: str, editora: str, autor: str, image: str = None):
        self.id = id
        self.titulo = titulo
        self.ano_publicacao = ano_publicacao
        self.genero = genero
        self.editora = editora
        self.autor = autor
        self.image = image
    def update(self, titulo: str = None, ano_publicacao: int = None, genero: str = None, editora: str = None):
        if titulo is not None:
            self.titulo = titulo
        if ano_publicacao is not None:
            self.ano_publicacao = ano_publicacao
        if genero is not None:
            self.genero = genero
        if editora is not None:
            self.editora = editora
        if self.autor is not None:
            self.autor = self.autor
    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "ano_publicacao": self.ano_publicacao,
            "genero": self.genero,
            "editora": self.editora,
            "autor": self.autor,
            "image": self.image
        }
    def from_dict(data: dict):
        return Livro(
            id=data.get("id"),
            titulo=data.get("titulo"),
            ano_publicacao=data.get("ano_publicacao"),
            genero=data.get("genero"),
            editora=data.get("editora"),
            autor=data.get("autor"),
            image=data.get("image", None)
        )

from src.utils.storage import load_data,save_data

class Catalogo:
    def __init__(self, MAX_COLUMN=4):
        self.MAX_COLUMN = MAX_COLUMN
        self.root=tk.Tk()
        self.root.title("Catálogo de Livros")
        self.imagens = []
        self.buttons = []
        self.livros = []
        self.popup_window = None  # Controle de popup único
        self.load()
        botao_Add=tk.Button(self.root, text="Adicionar", command = lambda: self.confLivro())
        botao_Add.grid(row=0,column=5)

        
    def run(self):
        
        self.draw()
        self.root.mainloop()
    def draw(self):
        # Clear previous widgets except the 'Adicionar' button
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button) and widget['text'] == "Adicionar":
                continue
            widget.destroy()
        self.imagens.clear()
        self.buttons.clear()

        # Redraw Add button (if it was destroyed above)
        botao_Add = tk.Button(self.root, text="Adicionar", command=lambda: self.confLivro())
        botao_Add.grid(row=0, column=5)

        for livro in self.livros:
            idx= self.livros.index(livro)
            livro_label = tk.Button(self.root,text=f"{livro.titulo}",command=lambda l=livro: self.readLivro(l))
            livro_label.grid(row = 1 + int(idx/self.MAX_COLUMN)*2, column=idx%self.MAX_COLUMN)
            self.buttons.append(livro_label)
            
            pilImg = Image.open("src/images/covers/" + livro.image)
            pilImg = pilImg.resize((100, 150))
            img = ImageTk.PhotoImage(pilImg)
            self.imagens.append(img)
            livro_image = tk.Label(self.root, image=img)
            livro_image.grid(row = 0 + int(idx//self.MAX_COLUMN)*2, column=idx%self.MAX_COLUMN)
    def readLivro(self, livro):
        if self.popup_window is not None and self.popup_window.winfo_exists():
            return
        popup = createPopup("Detalhes do Livro", self.root)
        self.popup_window = popup
        
        campos = [
        ("Título", livro.titulo),
        ("Autor", livro.autor),
        ("Ano de Publicação", livro.ano_publicacao),
        ("Gênero", livro.genero),
        ("Editora", livro.editora),
        ("Id", livro.id)
        ]
        for i, (label_text, value) in enumerate(campos):
            label = tk.Label(popup, text=f"{label_text}: {value}")
            label.grid(row=i, column=0)
        botao_Update = tk.Button(popup, text="Editar", command=lambda: [self.close_popup(), self.updateLivro(livro)])
        botao_Update.grid(row=1,column=1)
        botao_Delete=tk.Button(popup, text="Deletar",command =  lambda: self.deleteLivro(livro))
        botao_Delete.grid(row=2,column=1)
        
        def close_popup():
            if self.popup_window is not None:
                self.popup_window.destroy()
                self.popup_window = None
        
    def addLivro(self, popup, titulo, autor, ano_publicacao, genero, editora):
        """Função para adicionar um livro ao catálogo."""
        cover = random.randint(0, 6)  # Simulando a escolha de uma imagem aleatória
        image = f"cover0{cover}.jpg"  # Exemplo de nome de arquivo de imagem
        # Verificação se ano_publicacao é inteiro positivo
        try:
            ano_publicacao_int = int(ano_publicacao)
            if ano_publicacao_int <= 0:
                raise ValueError
        except (ValueError, TypeError):
            print("Erro: Ano de publicação deve ser um número inteiro positivo.")
            popup.destroy()
            return
        if self.livros:
            new_id = self.livros[-1].id + 1
        else:
            new_id = 0
        livro = Livro(new_id, titulo, ano_publicacao_int, genero, editora, autor, image)
        self.livros.append(livro)
        print(f"Livro '{titulo}' adicionado com sucesso!")
        self.save()
        self.draw()
        popup.destroy()
       
    def confLivro(self):
        if self.popup_window is not None and self.popup_window.winfo_exists():
            return
        popup = createPopup("Adicionar Livro", self.root)
        self.popup_window = popup

        campos = [
            ("Título", tk.StringVar()),
            ("Autor", tk.StringVar()),
            ("Ano de Publicação", tk.StringVar()),
            ("Gênero", tk.StringVar()),
            ("Editora", tk.StringVar())
        ]

        entries = []
        for i, (label_text, var) in enumerate(campos):
            label = tk.Label(popup, text=label_text + ":")
            label.grid(row=i, column=0)
            entry = tk.Entry(popup, textvariable=var)
            entry.grid(row=i, column=1)
            entries.append(var)

        submit_button = tk.Button(popup, text="Adicionar", command=lambda: on_submit(entries, popup, self, self.close_popup))
        submit_button.grid(row=len(campos), column=1)

        def validate_fields(*args):
            # Verifica se todos os campos estão preenchidos
            values = [var.get().strip() for var in entries]
            if any(v == "" for v in values):
                submit_button.config(state=tk.DISABLED)
                return
            # Verifica se ano de publicação é inteiro positivo
            try:
                ano = int(entries[2].get())
                if ano <= 0:
                    submit_button.config(state=tk.DISABLED)
                    return
            except ValueError:
                submit_button.config(state=tk.DISABLED)
                return
            submit_button.config(state=tk.NORMAL)

        # Adiciona o trace para todos os campos
        for var in entries:
            var.trace_add('write', validate_fields)
        validate_fields()  # Validação inicial
    def update_finish(self, popup, titulo, autor, ano_publicacao, genero, editora, new_id, old_id):
        """Função para atualizar um livro do catálogo."""
        # Verificação se ano_publicacao é inteiro positivo
        try:
            ano_publicacao_int = int(ano_publicacao)
            if ano_publicacao_int <= 0:
                raise ValueError
        except (ValueError, TypeError):
            print("Erro: Ano de publicação deve ser um número inteiro positivo.")
            popup.destroy()
            return
        # Verificação se Id é inteiro válido
        try:
            new_id_int = int(new_id)
            if new_id_int < 0 or new_id_int >= len(self.livros):
                raise ValueError
        except (ValueError, TypeError):
            print(f"Erro: Id deve ser um inteiro entre 0 e {len(self.livros)-1}.")
            popup.destroy()
            return
        image = self.livros[old_id].image # Salvando a imagem do livro
        if new_id_int == old_id:
            livro = self.livros[new_id_int]
            livro.titulo = titulo
            livro.ano_publicacao = ano_publicacao_int
            livro.genero = genero
            livro.editora = editora
            livro.autor = autor
            livro.image = image
        else:
            # Swap all attributes between the two books
            livro_a = self.livros[old_id]
            livro_b = self.livros[new_id_int]
            # Store livro_b's original data
            temp = (old_id, livro_b.titulo, livro_b.ano_publicacao, livro_b.genero, livro_b.editora, livro_b.autor, livro_b.image)
            # Update livro_b with new data
            livro_b.id = new_id_int
            livro_b.titulo = titulo
            livro_b.ano_publicacao = ano_publicacao_int
            livro_b.genero = genero
            livro_b.editora = editora
            livro_b.autor = autor
            livro_b.image = image
            # Move livro_a's data to livro_b's old data
            livro_a.id, livro_a.titulo, livro_a.ano_publicacao, livro_a.genero, livro_a.editora, livro_a.autor, livro_a.image = temp
        print(f"Livro '{titulo}' atualizado com sucesso!")
        self.save()
        self.draw()
        popup.destroy()
    def updateLivro(self, livro):
        if self.popup_window is not None and self.popup_window.winfo_exists():
            return
        popup = createPopup("Editar Livro", self.root)
        self.popup_window = popup

        campos = [
            ("Título", tk.StringVar()),
            ("Autor", tk.StringVar()),
            ("Ano de Publicação", tk.StringVar()),  # Agora StringVar para validação
            ("Gênero", tk.StringVar()),
            ("Editora", tk.StringVar()),
            ("Id", tk.StringVar())  # Agora StringVar para validação
        ]
        entries = []
        for i, (label_text, var) in enumerate(campos):
            label = tk.Label(popup, text=label_text + ":")
            label.grid(row=i, column=0)
            entry = tk.Entry(popup, textvariable=var)
            entry.grid(row=i, column=1)
            entries.append(var)

        # Pre-fill the fields
        campos[0][1].set(livro.titulo)
        campos[1][1].set(livro.autor)
        campos[2][1].set(str(livro.ano_publicacao))
        campos[3][1].set(livro.genero)
        campos[4][1].set(livro.editora)
        campos[5][1].set(str(livro.id))

        # Add old_id as a tk.IntVar
        old_id_var = tk.IntVar()
        old_id_var.set(livro.id)
        entries.append(old_id_var)

        submit_button = tk.Button(
            popup,
            text="Salvar",
            command=lambda: off_submit(entries, popup, self, self.close_popup)
        )
        submit_button.grid(row=len(campos), column=1)

        def validate_fields(*args):
            # Verifica se todos os campos estão preenchidos
            values = [var.get().strip() if isinstance(var, tk.StringVar) else str(var.get()) for var in entries[:-1]]
            if any(v == "" for v in values):
                submit_button.config(state=tk.DISABLED)
                return
            # Verifica se ano de publicação é inteiro positivo
            try:
                ano = int(entries[2].get())
                if ano <= 0:
                    submit_button.config(state=tk.DISABLED)
                    return
            except ValueError:
                submit_button.config(state=tk.DISABLED)
                return
            # Verifica se Id é inteiro válido
            try:
                id_val = int(entries[5].get())
                if id_val < 0 or id_val >= len(self.livros):
                    submit_button.config(state=tk.DISABLED)
                    return
            except ValueError:
                submit_button.config(state=tk.DISABLED)
                return
            submit_button.config(state=tk.NORMAL)

        # Adiciona o trace para todos os campos relevantes
        for var in entries[:-1]:
            var.trace_add('write', validate_fields)
        validate_fields()  # Validação inicial
    def deleteLivro(self, livro):
        self.livros.remove(livro)
        # Reassign IDs to keep them in order
        for idx, livro in enumerate(self.livros):
            livro.id = idx
        self.save()
        self.draw()
    def save(self):
        save_data(self.livros)
        print("Dados salvos com sucesso!")
    def load(self):
        self.livros = load_data()
        print("Dados carregados com sucesso!")
        self.draw()

    def close_popup(self):
        if self.popup_window is not None:
            self.popup_window.destroy()
            self.popup_window = None