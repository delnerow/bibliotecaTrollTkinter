import random
import tkinter as tk
from PIL import Image, ImageTk

from src.utils.popup import createPopup, on_submit

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
        self.load()
        botao_Add=tk.Button(self.root, text="Adicionar",command = lambda: self.confLivro())
        botao_Add.grid(row=0,column=5)

        
    def run(self):
        
        self.draw()
        self.root.mainloop()
    def draw(self):
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
        popup=createPopup("Detalhes do Livro",self.root)
        
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
        botao_Update=tk.Button(popup, text="Editar",command = lambda: print("WELBERSON"))
        botao_Update.grid(row=1,column=1)
        botao_Delete=tk.Button(popup, text="Deletar",command =  lambda: print("WELBERSON"))
        botao_Delete.grid(row=2,column=1)
        
    def addLivro(self,popup, titulo, autor, ano_publicacao, genero, editora):
        """Função para adicionar um livro ao catálogo."""
        cover = random.randint(0, 6)  # Simulando a escolha de uma imagem aleatória
        image = f"cover0{cover}.jpg"  # Exemplo de nome de arquivo de imagem
        livro = Livro(self.livros[-1].id+1,titulo, ano_publicacao, genero, editora,autor,image)
        self.livros.append(livro)
        print(f"Livro '{titulo}' adicionado com sucesso!")
        self.save()
        self.draw()
        popup.destroy()
       
    def confLivro(self):
        popup = createPopup("Adicionar Livro",self.root)

        campos = [
            ("Título", tk.StringVar()),
            ("Autor", tk.StringVar()),
            ("Ano de Publicação", tk.IntVar()),
            ("Gênero", tk.StringVar()),
            ("Editora", tk.StringVar())
        ]

        entries = []
        for i, (label_text, var) in enumerate(campos):
            label=tk.Label(popup, text=label_text + ":")
            label.grid(row=i, column=0)
            entry = tk.Entry(popup, textvariable=var)
            entry.grid(row=i, column=1)
            entries.append(var)

        submit_button = tk.Button(popup, text="Adicionar", command=lambda: on_submit(entries,popup,self))
        submit_button.grid(row=len(campos), column=1)
        
    def save(self):
        save_data(self.livros)
        print("Dados salvos com sucesso!")
    def load(self):
        self.livros = load_data()
        print("Dados carregados com sucesso!")
        self.draw()
        

