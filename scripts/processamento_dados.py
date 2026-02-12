import json
import csv

class Dados:
    # Construtor da classe Dados, que recebe o caminho do arquivo e o tipo de dados (CSV, JSON ou lista em memória)
    def __init__(self, path, tipo_dados):
        self.path = path
        self.tipo_dados = tipo_dados
        self.dados = self.leitura_dados()
        self.nome_colunas = self.get_columns()
        self.qtd_linhas = self.size_data()

    # Função para ler os dados de um arquivo JSON e armazená-los em uma lista de dicionários
    def leitura_json(self):
        dados_json = []
        with open(self.path, 'r') as file:
            dados_json = json.load(file)
        return dados_json

    # Função para ler os dados de um arquivo CSV e armazená-los em uma lista de dicionários
    def leitura_csv(self):

        dados_csv = []
        with open(self.path, 'r') as file:
            spamreader = csv.DictReader(file, delimiter=',')
            for row in spamreader:
                dados_csv.append(row)

        return dados_csv

    # Função para ler os dados com base no tipo de dados especificado (CSV, JSON ou lista em memória)
    def leitura_dados(self):
        dados = []

        if self.tipo_dados == 'csv':
            dados = self.leitura_csv()
        
        elif self.tipo_dados == 'json':
            dados = self.leitura_json()

        elif self.tipo_dados == 'list':
            dados = self.path
            self.path = "lista em memoria"

        return dados

    # Função para obter os nomes das colunas dos dados
    def get_columns(self):
        return list(self.dados[-1].keys())

    # Função para renomear as colunas dos dados com base em um dicionário de mapeamento
    def rename_columns(self, key_mapping):
        new_dados = []

        for old_dict in self.dados:
            dict_temp = {}
            for old_key, value in old_dict.items():
                dict_temp[key_mapping[old_key]] = value
            new_dados.append(dict_temp)
        
        self.dados = new_dados
        self.nome_colunas = self.get_columns()

    # Função para obter a quantidade de linhas dos dados
    def size_data(self):
        return len(self.dados)

    # Função para combinar os dados de duas instâncias da classe Dados
    def join(dadosA, dadosB):
        combined_list = []
        combined_list.extend(dadosA.dados)
        combined_list.extend(dadosB.dados)
        
        return Dados(combined_list, 'list')

    # Função para transformar os dados combinados em uma tabela (lista de listas) para facilitar a escrita em CSV
    def transformando_dados_tabela(self):
        
        dados_combinados_tabela = [self.nome_colunas]

        for row in self.dados:
            linha = []
            for coluna in self.nome_colunas:
                linha.append(row.get(coluna, 'Indisponivel'))
            dados_combinados_tabela.append(linha)
        
        return dados_combinados_tabela
    
    # Função para salvar os dados combinados em um arquivo CSV 
    def salvando_dados(self, path):

        dados_combinados_tabela = self.transformando_dados_tabela()

        with open(path, 'w') as file:
            writer = csv.writer(file)
            writer.writerows(dados_combinados_tabela)