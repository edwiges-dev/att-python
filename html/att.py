from datetime import datetime
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk


class Gerenciador_Tarefas:
    """
    Classe principal para o aplicativo de Gerenciador de Tarefas.
    Gerencia a interface gráfica e a lógica das tarefas.
    """
    def __init__(self, janela):
        """
        Inicializa o Gerenciador de Tarefas.

        Args:
            janela (tk.Tk): A janela principal do Tkinter.
        """
        self.janela = janela
        self.janela.title("Gerenciador de Tarefas")
        self.janela.geometry("800x600")

        # Lista para armazenar as tarefas. Cada tarefa é um dicionário.
        self.tarefas = []

        # Configura o estilo dos widgets ttk.
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Chama a função para criar todos os widgets da interface.
        self.criar_widgets()

    def criar_widgets(self):
        """
        Cria e organiza todos os widgets da interface gráfica do usuário.
        Esta função configura a janela principal, campos de entrada, botões e a Treeview.
        """
        # Frame principal que contém todos os outros elementos.
        frame_principal = ttk.Frame(self.janela, padding="10")
        frame_principal.pack(fill=tk.BOTH, expand=True)

        # Frame para os campos de entrada de dados (tarefa, descrição, prioridade, data).
        Entrada_frame = ttk.Frame(frame_principal, padding=10)
        Entrada_frame.pack(fill=tk.X)

        # Rótulo e campo de entrada para o nome da tarefa.
        ttk.Label(Entrada_frame, text="Tarefa:").grid(row=0, column=0, padx=5, sticky=tk.W)
        self.entrada_tarefa = ttk.Entry(Entrada_frame, width=50)
        self.entrada_tarefa.grid(row=0, column=1, padx=5, pady=5)
        self.entrada_tarefa.focus() # Define o foco inicial neste campo.

        # Rótulo e campo de entrada para a descrição da tarefa.
        ttk.Label(Entrada_frame, text="Descrição:").grid(row=1, column=0, padx=5, sticky=tk.W)
        self.entrada_descricao = ttk.Entry(Entrada_frame, width=50)
        self.entrada_descricao.grid(row=1, column=1, padx=5, pady=5)
        
        # Rótulo e Combobox para a prioridade da tarefa.
        ttk.Label(Entrada_frame, text="Prioridade:").grid(row=2, column=0, padx=5, sticky=tk.W) # Corrigido para row=2
        self.prioridade = tk.StringVar(value="Média") # Variável para armazenar a prioridade selecionada.
        ttk.Combobox(Entrada_frame, textvariable=self.prioridade, values=["Baixa", "Média", "Alta"], state="readonly").grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        # Rótulo e campo de entrada para a data de vencimento.
        ttk.Label(Entrada_frame, text='Data de Vencimento').grid(row=3, column=0, sticky=tk.W)
        self.entrada_data = ttk.Entry(Entrada_frame, width=20)
        self.entrada_data.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        # Preenche o campo de data com a data atual por padrão.
        self.entrada_data.insert(0, datetime.now().strftime('%d/%m/%Y'))

        # Frame para os botões de ação (adicionar, editar, remover, marcar como concluída).
        botoes_frame = ttk.Frame(Entrada_frame)
        botoes_frame.grid(row=4, column=1, pady=10, sticky=tk.W)

        # Botões e suas respectivas funções de comando.
        ttk.Button(botoes_frame, text='Adicionar', command=self.adicionar_tarefa).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes_frame, text='Editar', command=self.editar_tarefa).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes_frame, text='Remover', command=self.remover_tarefa).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes_frame, text='Marcar como concluída', command=self.marcar_concluida).pack(side=tk.LEFT, padx=5)

        # Treeview para exibir a lista de tarefas.
        self.tree = ttk.Treeview(frame_principal, columns=('ID', 'tarefa', 'descrição', 'prioridade', 'data de vencimento', 'concluída'), show='headings', selectmode='browse')

        # Definição das colunas da Treeview (largura, alinhamento, cabeçalho).
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.heading('ID', text='ID')

        self.tree.column('tarefa', width=150, anchor=tk.CENTER)
        self.tree.heading('tarefa', text='Tarefa')

        self.tree.column('descrição', width=200, anchor=tk.CENTER) # Movido 'descrição' para a posição correta.
        self.tree.heading('descrição', text='Descrição')

        self.tree.column('prioridade', width=100, anchor=tk.CENTER) # Ajustada largura.
        self.tree.heading('prioridade', text='Prioridade')

        self.tree.column('data de vencimento', width=120, anchor=tk.CENTER) # Ajustada largura.
        self.tree.heading('data de vencimento', text='Data de Vencimento')

        self.tree.column('concluída', width=80, anchor=tk.CENTER)
        self.tree.heading('concluída', text='Concluída')

        # Empacota a Treeview.
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Adiciona uma barra de rolagem vertical à Treeview.
        scrollbar = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Atualiza a lista de tarefas exibida na Treeview.
        self.atualizar_lista()

        # Vincula o evento de seleção de item na Treeview à função selecionar_tarefa.
        self.tree.bind('<<TreeviewSelect>>', self.selecionar_tarefa)

    def adicionar_tarefa(self):
        """
        Adiciona uma nova tarefa à lista de tarefas.
        Pega os valores dos campos de entrada, cria um dicionário para a nova tarefa,
        adiciona à lista 'self.tarefas' e atualiza a interface.
        """
        tarefa = self.entrada_tarefa.get().strip()
        descricao = self.entrada_descricao.get().strip()
        prioridade = self.prioridade.get()
        data = self.entrada_data.get().strip()

        # Validação básica para garantir que a tarefa não está vazia.
        if not tarefa:
            messagebox.showwarning("Entrada Inválida", "O campo 'Tarefa' não pode estar vazio.")
            return

        # Cria um dicionário representando a nova tarefa.
        nova_tarefa = {
            'id': len(self.tarefas) + 1,  # ID simples baseado no tamanho da lista.
            'tarefa': tarefa,
            'descricao': descricao, # Corrigido para 'descricao' para consistência.
            'prioridade': prioridade,
            'data': data,
            'concluida': False  # Nova tarefa não está concluída por padrão.
        }

        self.tarefas.append(nova_tarefa)  # Adiciona a nova tarefa à lista.
        self.atualizar_lista()           # Atualiza a exibição na Treeview.
        self.limpar_tarefa()             # Limpa os campos de entrada.

    def editar_tarefa(self):
        """
        Edita uma tarefa existente na lista.
        Pega a tarefa selecionada na Treeview, atualiza seus dados com os valores
        dos campos de entrada e, em seguida, atualiza a exibição.
        """
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Nenhuma Seleção", "Selecione uma tarefa para editar.")
            return

        # Obtém os valores do item selecionado na Treeview.
        item = self.tree.item(selecionado)
        id_tarefa_selecionada = item['values'][0] # O ID é o primeiro valor.

        # Pega os valores atualizados dos campos de entrada.
        tarefa = self.entrada_tarefa.get().strip()
        descricao = self.entrada_descricao.get().strip()
        prioridade = self.prioridade.get()
        data = self.entrada_data.get().strip()

        # Validação básica para garantir que a tarefa não está vazia.
        if not tarefa:
            messagebox.showwarning("Entrada Inválida", "O campo 'Tarefa' não pode estar vazio.")
            return

        # Itera sobre a lista de tarefas para encontrar e atualizar a tarefa correta.
        for opcao in self.tarefas:
            if opcao['id'] == id_tarefa_selecionada: # Compara com o ID correto 'id'.
                opcao['tarefa'] = tarefa
                opcao['descricao'] = descricao
                opcao['prioridade'] = prioridade
                opcao['data'] = data
                break # Sai do loop assim que a tarefa é encontrada e atualizada.

        self.atualizar_lista() # Atualiza a exibição na Treeview.
        self.limpar_tarefa()   # Limpa os campos de entrada.

    def remover_tarefa(self):
        """
        Remove uma tarefa selecionada da lista.
        Pega a tarefa selecionada na Treeview e a remove da lista 'self.tarefas'.
        Em seguida, atualiza a exibição.
        """
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Nenhuma Seleção", "Selecione uma tarefa para remover.")
            return

        confirmar = messagebox.askyesno("Remover Tarefa", "Tem certeza que deseja remover esta tarefa?")
        if not confirmar:
            return

        # Obtém os valores do item selecionado na Treeview.
        item = self.tree.item(selecionado)
        id_tarefa_a_remover = item['values'][0]

        # Cria uma nova lista de tarefas, excluindo a tarefa com o ID selecionado.
        self.tarefas = [tarefa for tarefa in self.tarefas if tarefa['id'] != id_tarefa_a_remover] 

        self.atualizar_lista()  # Atualiza a exibição na Treeview.
        self.limpar_tarefa()    # Limpa os campos de entrada.
 
    def marcar_concluida(self):
        """
        Alterna o status de conclusão de uma tarefa selecionada.
        Se a tarefa estiver não concluída, marca como concluída, e vice-versa.
        """
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Nenhuma Seleção", "Selecione uma tarefa para marcar/desmarcar.")
            return

        # Obtém os valores do item selecionado na Treeview.
        item = self.tree.item(selecionado)
        id_tarefa_a_marcar = item['values'][0]

        # Itera sobre a lista de tarefas para encontrar e alternar o status.
        for opcao in self.tarefas:
            if opcao['id'] == id_tarefa_a_marcar:
                opcao['concluida'] = not opcao['concluida'] # Inverte o valor booleano.
                break

        self.atualizar_lista() # Atualiza a exibição na Treeview para refletir a mudança.
        self.limpar_tarefa()   # Limpa os campos de entrada.
 
    def limpar_tarefa(self):
        """
        Limpa todos os campos de entrada de tarefa na interface.
        Redefine a data para a data atual e a prioridade para "Média".
        """
        self.entrada_tarefa.delete(0, tk.END)
        self.entrada_descricao.delete(0, tk.END)
        self.prioridade.set('Média')
        self.entrada_data.delete(0, tk.END) # Limpa antes de inserir.
        self.entrada_data.insert(0, datetime.now().strftime('%d/%m/%Y')) 

    def atualizar_lista(self):
        """
        Atualiza a exibição da lista de tarefas na Treeview.
        Limpa todos os itens existentes na Treeview e os repopula com os dados
        mais recentes da lista 'self.tarefas'.
        """
        # Reatribui IDs sequenciais às tarefas para garantir que estejam sempre em ordem.
        for i, tarefa in enumerate(self.tarefas, 1):
            tarefa['id'] = i 

        # Limpa todos os itens atualmente na Treeview.
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insere cada tarefa da lista 'self.tarefas' na Treeview.
        for tarefa in self.tarefas:
            self.tree.insert('', tk.END, values=(
                tarefa['id'],
                tarefa['tarefa'],
                tarefa['descricao'],
                tarefa['prioridade'],
                tarefa['data'],
                'Sim' if tarefa['concluida'] else 'Não' # Exibe 'Sim' ou 'Não' para concluída.
            )) 

    def selecionar_tarefa(self, event):
        """
        Preenche os campos de entrada com os detalhes da tarefa selecionada na Treeview.
        Esta função é acionada quando um item é selecionado na Treeview.
        """
        selecionado = self.tree.selection()
        if not selecionado:
            return

        # Obtém os valores do item selecionado.
        item = self.tree.item(selecionado)
        valores = item['values']

        self.limpar_tarefa() # Limpa os campos de entrada antes de preencher.

        # Preenche os campos de entrada com os valores da tarefa selecionada.
        self.entrada_tarefa.insert(0, valores[1])      # Tarefa
        self.entrada_descricao.insert(0, valores[2])   # Descrição
        self.prioridade.set(valores[3])                # Prioridade
        self.entrada_data.insert(0, valores[4])        # Data de Vencimento
        # Não é necessário self.entrada_data.delete(0, tk.END) aqui, pois já limpamos.

# --- Inicialização do Aplicativo ---
if __name__ == "__main__":
    # Cria a janela principal do Tkinter.
    janela = tk.Tk()
    # Instancia a classe Gerenciador_Tarefas, passando a janela.
    app = Gerenciador_Tarefas(janela)
    # Inicia o loop principal de eventos do Tkinter, que mantém a janela aberta.
    janela.mainloop()