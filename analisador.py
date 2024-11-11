import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, Button, Label, Entry, filedialog, messagebox


class ExemploJanela:
    def __init__(self, master):
        self.master = master
        master.title("Avaliação da Satisfação do Paciente")

        # Define o tamanho da janela
        master.geometry("800x600")

        # Texto explicativo da tela inicial
        self.texto_inicial = Label(master, text="Bem-vindo ao projeto de Avaliação da Satisfação do Paciente.\n\n\n"
                                                 "O modelo de Parasuraman, também conhecido como SERVQUAL, foi desenvolvido\n"
                                                 "para medir a qualidade do serviço, e sua aplicação na área da saúde destaca\n"
                                                 "que um atendimento de qualidade é essencial para garantir um tratamento e\n"
                                                 "recuperação eficientes. Este modelo se baseia em cinco dimensões principais \n"
                                                 "tangibilidade, confiabilidade, responsividade, empatia e segurança que\n"
                                                 "influenciam diretamente a percepção dos pacientes sobre a qualidade do atendimento.\n\n"
                                                 "Nosso objetivo é analisar as reclamações dos pacientes em relação aos\n"
                                                 "serviços de saúde, categorizando-as e avaliando as médias de satisfação\n"
                                                 "em diferentes períodos. Com isso, buscamos identificar áreas que necessitam\n"
                                                 "de atenção e aprimoramento, visando aumentar a qualidade do atendimento.\n\n"
                                                 "Clique no botão abaixo para prosseguir.", justify="center")
        self.texto_inicial.pack(pady=50)

        # Botão para prosseguir
        self.botao_prosseguir = Button(master, text="Próximo", command=self.mostrar_interface)
        self.botao_prosseguir.pack(pady=20)

        # Elementos da interface que serão exibidos após o botão ser clicado
        self.botao_carregar = Button(master, text="Carregar Arquivo", command=self.carregar_arquivo)
        self.label_ano_inicial = Label(master, text="Ano Inicial:")
        self.ano_inicial_entry = Entry(master)
        self.label_ano_final = Label(master, text="Ano Final:")
        self.ano_final_entry = Entry(master)
        self.botao_gerar_grafico = Button(master, text="Gerar Gráfico", command=self.gerar_grafico)
        self.rotulo_dimensoes = Label(master, text="")
        self.dados = None

    def mostrar_interface(self):
        # Esconde os elementos da tela inicial
        self.texto_inicial.pack_forget()
        self.botao_prosseguir.pack_forget()

        # Mostra os elementos da interface principal
        self.botao_carregar.pack(pady=20)
        self.label_ano_inicial.pack()
        self.ano_inicial_entry.pack(pady=5)
        self.label_ano_final.pack()
        self.ano_final_entry.pack(pady=5)
        self.botao_gerar_grafico.pack(pady=20)
        self.rotulo_dimensoes.pack(pady=10)

    def carregar_arquivo(self):
        # Abrindo a caixa de diálogo para seleção do arquivo
        arquivo = filedialog.askopenfilename(title="Selecionar Arquivo", filetypes=(("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")))
        if arquivo:
            try:
                # Carregar dados a partir do arquivo
                if arquivo.endswith('.csv'):
                    self.dados = pd.read_csv(arquivo)
                elif arquivo.endswith('.txt'):
                    self.dados = pd.read_csv(arquivo, sep="\t")  # Lê TXT com separador de tabulação
                self.rotulo_dimensoes.config(text=f"Arquivo carregado: {arquivo}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar o arquivo: {e}")

    def gerar_grafico(self):
        if self.dados is None:
            messagebox.showwarning("Aviso", "Por favor, carregue um arquivo primeiro.")
            return

        try:
            ano_inicial = int(self.ano_inicial_entry.get())
            ano_final = int(self.ano_final_entry.get())

            # Extraindo o ano da coluna 'data'
            self.dados['ano'] = self.dados['data'].str[:4].astype(int)

            # Filtra os dados de acordo com os anos
            dados_filtrados = self.dados[(self.dados['ano'] >= ano_inicial) & (self.dados['ano'] <= ano_final)]

            if dados_filtrados.empty:
                messagebox.showinfo("Informação", "Nenhum dado encontrado para o período especificado.")
                return

            # Contagem de reclamações
            contagem_reclamacoes = dados_filtrados['reclamação'].value_counts()

            # Média de satisfação
            media_satisfacao = dados_filtrados['satisfação'].mean()

            # Gerar gráfico com cor básica
            contagem_reclamacoes.plot(kind='bar', color='#6CA0DC')  # Azul claro voltado à saúde
            plt.title(f'Reclamações de {ano_inicial} a {ano_final}\nMédia de Satisfação: {media_satisfacao:.2f}')
            plt.xlabel('Tipo de Reclamação')
            plt.ylabel('Frequência')
            plt.xticks(rotation=0)  # Rótulos do eixo x sem inclinação
            plt.tight_layout()
            plt.show()

        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira anos válidos.")


if __name__ == "__main__":
    root = Tk()
    app = ExemploJanela(root)
    root.mainloop()
