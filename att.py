from datetime import datetime
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk

class Gerenciador_Tarefas:
    def __init__(self,janela):
        self.janela=janela
        self.janela.title("Gerenciador de Tarefas")
        self.janela.geometry("800x600")

        self.tarefas = []

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.criar_widgets()

    def criar_widgets(self):
        frame_principal = ttk.Frame(self.janela , padding="10")
        frame_principal.pack(fill= tk.BOTH, expand=True)

        Entrada_frame = ttk.Frame(frame_principal,padding=10)
        Entrada_frame.pack(fill=tk.X)

        ttk.Label(Entrada_frame, text="Tarefa:").grid(row=0, column=0, padx=5,sticky= tk.W)
        self.entrada_tarefa = ttk.Entry(Entrada_frame, width=50)
        self.entrada_tarefa.grid(row=0, column=1, padx=5, pady=5)
        self.entrada_tarefa.focus()

        ttk.Label(Entrada_frame, text="Descrição:").grid(row=1, column=0, padx=5,sticky= tk.W)
        self.entrada_descricao= ttk.Entry(Entrada_frame, width=50)
        self.entrada_descricao.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(Entrada_frame, text="Prioridade:").grid(row=1, column=0, padx=5,sticky= tk.W)
        self.prioridade = tk.StringVar(value="Média")
        ttk.Combobox(Entrada_frame, textvariable= self.prioridade,values= ["Baixa", "Média","Alta"],state="readonly").grid(row=2,column=1, padx=5,pady=5,sticky=tk.W)

        ttk.Label(Entrada_frame,text='Data de Vencimento').grid(row=3,column=0,sticky=tk.W)
        self.entrada_data= ttk.Entry(Entrada_frame,width=20)
        self.entrada_data.grid(row=3, column=1, padx=5, pady=5 , sticky=tk.W)
        self.entrada_data.insert(0,datetime.now().strftime('%d/%m/%Y'))

        botoes_frame= ttk.Frame(Entrada_frame)
        botoes_frame.grid(row=4,column=1,pady=10, sticky=tk.W)

        ttk.Button(botoes_frame,text='adicionar',command=self.adicionar_tarefa).pack(side=tk.LEFT,padx=5)
        ttk.Button(botoes_frame,text='editar',command=self.editar_tarefa).pack(side=tk.LEFT,padx=5)
        ttk.Button(botoes_frame,text='remover',command=self.remover_tarefa).pack(side=tk.LEFT,padx=5)
        ttk.Button(botoes_frame,text='Marcar como concluída',command=self.marcar_concluida).pack(side=tk.LEFT,padx=5)

        self.tree=ttk.Treeview(frame_principal,columns=('ID','tarefa','descrição','prioridade','data de vencimento','concluída'), show='headings',selectmode='browse')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.heading('ID',text='ID')


        self.tree.column('tarefa', width=150, anchor=tk.CENTER)
        self.tree.heading('tarefa',text='tarefa')

        self.tree.column('prioridade', width=150, anchor=tk.CENTER)
        self.tree.heading('prioridade',text='prioridade')

        self.tree.column('descrição', width=200, anchor=tk.CENTER)
        self.tree.heading('descrição',text='descrição')

        self.tree.column('data de vencimento', width=80, anchor=tk.CENTER)
        self.tree.heading('data de vencimento',text='data de vencimento')

        self.tree.column('concluída', width=80, anchor=tk.CENTER)
        self.tree.heading('concluída',text='concluída')

        self.tree.pack(fill=tk.BOTH,expand=True,pady=10)
        scrollbar= ttk.Scrollbar(self.tree,orient=tk.VERTICAL,command=self.tree.yview)
        self.tree.configure(yscroll= scrollbar.set)
        scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

        self.atualizar_lista()

        self.tree.bind('<<TreeViewSelect>>',self.selecionar_tarefa)

        

    def adicionar_tarefa(self):
        tarefa=self.entrada_tarefa.get().strip()
        descricao=self.entrada_descricao.get().strip()
        prioridade =self.prioridade.get()
        data=self.entrada_data.get().strip()

        nova_tarefa={
            'id': len(self.tarefas)+1,
            'tarefa': tarefa,
            'descrição': descricao,
            'prioridade': prioridade,
            'data': data,
            'concluida': False
        }

        self.tarefas.append(nova_tarefa)
        self.atualizar_lista()
        self.limpar_tarefa()

    def editar_tarefa(self):
        selecionado=self.tree.selection()
        if not selecionado:
            return

        item=self.tree.item(selecionado)
        id_tarefa=item['values'][0]

        tarefa=self.entrada_tarefa.get().strip()
        descricao=self.entrada_descricao.get().strip()
        prioridade=self.prioridade.get()
        data=self.entrada_data.get().strip()

        for opcao in self.tarefas:
            if opcao['ID'] ==id_tarefa:
                opcao['tarefa']= tarefa
                opcao['descricao']=descricao
                opcao['prioridade']=prioridade
                opcao['data']=data
            break

        self.atualizar_lista()

    def remover_tarefa(self):
        selecionado=self.tree.selection()
        if not selecionado:
            return

        item=self.tree.item(selecionado)
        id_tarefa=item['values'][0]

        for opcao in self.tarefas:

            self.tarefas = [opcao for opcao in self.tarefas if opcao['id'] != id_tarefa]    

            self.atualizar_lista()
            self.limpar_tarefa()                     

    def marcar_concluida(self):
        selecionado=self.tree.selection()
        if not selecionado:
            return

        item= self.tree.item(selecionado)
        id_tarefa=item['values'][0]

        for opcao in self.tarefas:
            if opcao['id']==id_tarefa:
                opcao['concluida']= not opcao ['concluida']
                break

        self.atualizar_lista()    

    def limpar_tarefa(self):
        self.entrada_data.delete(0,tk.END)
        self.entrada_descricao.delete(0,tk.END)
        self.prioridade.set('média')
        self.entrada_data.insert(0,datetime.now().strftime('%d/%m/%Y'))  



    def atualizar_lista(self):
        for itens,tarefa in enumerate(self.tarefas,1):
            tarefa['id']= itens #manter id ognzd


        for item in self.tree.get_children():
            self.tree.delete(item)


        for tarefa in self.tarefas:
            self.tree.insert('',tk.END,values=(tarefa['id'],tarefa['tarefa'],tarefa['descricao'],tarefa['prioridade'],tarefa['data'],'sim' if tarefa['concluida'] else 'não' ))    


    def selecionar_tarefa (self,event):
        selecionado= self.tree.selection()
        if not selecionado:
            return

        item= self.tree.item(selecionado)

        valores= item['values']

        self.limpar_tarefa()

        self.entrada_tarefa.insert(0,valores[1])
        self.entrada_descricao.insert(0,valores[2])
        self.prioridade.set(valores[3])
        self.entrada_data.insert(0,valores[4])
        self.entrada_data.delete(0,tk.END)    

janela= tk.Tk()
app=Gerenciador_Tarefas(janela)
janela.mainloop()            
