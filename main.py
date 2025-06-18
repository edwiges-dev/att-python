from tkinter import *
from tkinter import ttk
from datetime import datetime

root = Tk()
root.title("Gerenciador de Tarefas Avançado")
root.geometry("1000x700")
root.config(bg="#2d2d2d")

tasks = []
next_id = 1  # Contador para IDs únicos

def adiciona_task():
    global next_id
    task_nome = task_entry.get()
    task_descricao = description_entry.get("1.0", END).strip()
    prioridade = prioridade_var.get()
    data_vencimento = due_entry.get()

    if task_nome and data_vencimento:
        try:
            # Validar formato da data
            datetime.strptime(data_vencimento, "%d/%m/%Y")
            task = {
                "id": next_id,
                "name": task_nome,
                "description": task_descricao,
                "priority": prioridade,
                "due_date": data_vencimento,
                "completed": False
            }
            tasks.append(task)
            next_id += 1
            atualizar_treeview()
            clear_inputs()
        except ValueError:
            status_label.config(text="Formato de data inválido! Use DD/MM/AAAA", fg="red")
    else:
        status_label.config(text="Nome e data de vencimento são obrigatórios!", fg="red")

def editor_task():
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        task_id = item['values'][0]
        
        # Encontrar tarefa pelo ID
        task = next((t for t in tasks if t["id"] == task_id), None)
        if task:
            task_entry.delete(0, END)
            task_entry.insert(0, task["name"])
            
            description_entry.delete("1.0", END)
            description_entry.insert("1.0", task["description"])
            
            prioridade_var.set(task["priority"])
            due_entry.delete(0, END)
            due_entry.insert(0, task["due_date"])
            
            add_button.config(state=DISABLED)
            update_button.config(state=NORMAL)
            root.editing_id = task_id

def atualiza_task():
    if hasattr(root, 'editing_id'):
        task_nome = task_entry.get()
        task_descricao = description_entry.get("1.0", END).strip()
        prioridade = prioridade_var.get()
        data_vencimento = due_entry.get()
        
        if task_nome and data_vencimento:
            try:
                # Validar formato da data
                datetime.strptime(data_vencimento, "%d/%m/%Y")
                # Encontrar tarefa pelo ID
                task = next((t for t in tasks if t["id"] == root.editing_id), None)
                if task:
                    task["name"] = task_nome
                    task["description"] = task_descricao
                    task["priority"] = prioridade
                    task["due_date"] = data_vencimento
                    
                    atualizar_treeview()
                    clear_inputs()
                    
                    add_button.config(state=NORMAL)
                    update_button.config(state=DISABLED)
                    del root.editing_id
                    status_label.config(text="Tarefa atualizada com sucesso!", fg="green")
            except ValueError:
                status_label.config(text="Formato de data inválido! Use DD/MM/AAAA", fg="red")

def remove_task():
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        task_id = item['values'][0]
        
        # Encontrar e remover tarefa pelo ID
        global tasks
        tasks = [t for t in tasks if t["id"] != task_id]
        atualizar_treeview()
        clear_inputs()
        status_label.config(text="Tarefa removida com sucesso!", fg="green")

def marcar_concluida():
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        task_id = item['values'][0]
        
        # Encontrar tarefa pelo ID
        task = next((t for t in tasks if t["id"] == task_id), None)
        if task:
            task["completed"] = not task["completed"]
            atualizar_treeview()
            status_label.config(text="Status da tarefa atualizado!", fg="green")

def atualizar_treeview():
    # Limpar a treeview
    for item in tree.get_children():
        tree.delete(item)
    
    # Adicionar tarefas ordenadas por data de vencimento
    sorted_tasks = sorted(tasks, key=lambda x: datetime.strptime(x['due_date'], "%d/%m/%Y"))
    
    for task in sorted_tasks:
        completed = "Sim" if task["completed"] else "Não"
        # Cor baseada na prioridade
        if task["priority"] == "Alta":
            cor = "#ff6b6b"  # Vermelho
        elif task["priority"] == "Média":
            cor = "#ffd166"  # Amarelo
        else:
            cor = "#06d6a0"  # Verde
            
        tree.insert("", "end", values=(
            task["id"],
            task["name"],
            task["description"][:50] + "..." if len(task["description"]) > 50 else task["description"],
            task["priority"],
            task["due_date"],
            completed
        ), tags=(cor,))

def clear_inputs():
    task_entry.delete(0, END)
    description_entry.delete("1.0", END)
    prioridade_var.set("Baixa")
    due_entry.delete(0, END)
    due_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
    status_label.config(text="")
    if hasattr(root, 'editing_id'):
        add_button.config(state=NORMAL)
        update_button.config(state=DISABLED)
        del root.editing_id

def on_tree_select(event):
    editor_task()

# Frame de entrada
input_frame = Frame(root, bg="#2d2d2d")
input_frame.pack(pady=10, padx=20, fill=X)

# Nome da tarefa
task_label = Label(input_frame, text="Tarefa:", bg="#2d2d2d", fg="white")
task_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
task_entry = Entry(input_frame, width=50)
task_entry.grid(row=0, column=1, padx=5, pady=5, sticky=EW)

# Descrição
description_label = Label(input_frame, text="Descrição:", bg="#2d2d2d", fg="white")
description_label.grid(row=1, column=0, padx=5, pady=5, sticky=NW)

description_entry = Text(input_frame, width=50, height=4)
description_entry.grid(row=1, column=1, padx=5, pady=5, sticky=EW)

# Prioridade
priority_label = Label(input_frame, text="Prioridade:", bg="#2d2d2d", fg="white")
priority_label.grid(row=2, column=0, padx=5, pady=5, sticky=W)

prioridade_var = StringVar(value="Baixa")
priority_menu = ttk.Combobox(
    input_frame, 
    textvariable=prioridade_var, 
    values=["Baixa", "Média", "Alta"],
    state="readonly",
    width=17
)
priority_menu.grid(row=2, column=1, padx=5, pady=5, sticky=W)

# Data de Vencimento
due_label = Label(input_frame, text="Data Vencimento:", bg="#2d2d2d", fg="white")
due_label.grid(row=3, column=0, padx=5, pady=5, sticky=W)

due_entry = Entry(input_frame, width=20)
due_entry.grid(row=3, column=1, padx=5, pady=5, sticky=W)
due_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))

# Status Label
status_label = Label(input_frame, text="", bg="#2d2d2d", fg="green")
status_label.grid(row=4, column=1, padx=5, pady=5, sticky=W)

# Botões
button_frame = Frame(root, bg="#2d2d2d")
button_frame.pack(pady=10)

add_button = Button(
    button_frame, 
    text="Adicionar Tarefa", 
    command=adiciona_task,
    bg="#4CAF50",
    fg="white",
    width=15
)
add_button.grid(row=0, column=0, padx=5)

update_button = Button(
    button_frame, 
    text="Atualizar Tarefa", 
    command=atualiza_task,
    state=DISABLED,
    bg="#2196F3",
    fg="white",
    width=15
)
update_button.grid(row=0, column=1, padx=5)

edit_button = Button(
    button_frame, 
    text="Editar Tarefa", 
    command=editor_task,
    bg="#FF9800",
    fg="white",
    width=15
)
edit_button.grid(row=0, column=2, padx=5)

remove_button = Button(
    button_frame, 
    text="Remover Tarefa", 
    command=remove_task,
    bg="#F44336",
    fg="white",
    width=15
)
remove_button.grid(row=0, column=3, padx=5)

complete_button = Button(
    button_frame, 
    text="Concluir Tarefa", 
    command=marcar_concluida,
    bg="#9C27B0",
    fg="white",
    width=18
)
complete_button.grid(row=0, column=4, padx=5)

# Treeview (Tabela)
tree_frame = Frame(root, bg="#2d2d2d")
tree_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

# Criação da Treeview com barra de rolagem
scrollbar = Scrollbar(tree_frame)
scrollbar.pack(side=RIGHT, fill=Y)

tree = ttk.Treeview(
    tree_frame,
    columns=("ID", "Tarefa", "Descrição", "Prioridade", "Vencimento", "Concluída"),
    show="headings",
    height=15,
    yscrollcommand=scrollbar.set,
    selectmode="browse"
)
scrollbar.config(command=tree.yview)

# Definir cabeçalhos
tree.heading("ID", text="ID")
tree.heading("Tarefa", text="Tarefa")
tree.heading("Descrição", text="Descrição")
tree.heading("Prioridade", text="Prioridade")
tree.heading("Vencimento", text="Vencimento")
tree.heading("Concluída", text="Concluída")

# Definir largura das colunas
tree.column("ID", width=50, anchor=CENTER)
tree.column("Tarefa", width=150)
tree.column("Descrição", width=250)
tree.column("Prioridade", width=80, anchor=CENTER)
tree.column("Vencimento", width=100, anchor=CENTER)
tree.column("Concluída", width=80, anchor=CENTER)

# Configurar tags para cores
tree.tag_configure("#ff6b6b", background="#ff6b6b")
tree.tag_configure("#ffd166", background="#ffd166")
tree.tag_configure("#06d6a0", background="#06d6a0")

tree.pack(fill=BOTH, expand=True)

# Vincular seleção à função de edição
tree.bind("<<TreeviewSelect>>", on_tree_select)

# Rodar a aplicação
atualizar_treeview()
root.mainloop()



