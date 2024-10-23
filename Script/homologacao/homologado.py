
import os
import xml.etree.ElementTree as ET
import pandas as pd
import logging

diretorio_logs = r'C:\Users\Pedra\Desktop\script xml\log'

# verifica se o diretorio existe, senão cria ele
if not os.path.exists(diretorio_logs):
    os.makedirs(diretorio_logs)

# define o caminho absoluto do arquivo de log
caminho_log = os.path.join(diretorio_logs, 'processamento_xml.log')

# configuração de log 
logging.basicConfig(
    filename=caminho_log,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# função para extrair dados do XML com tratamento do namespace
def extrair_dados_xml(caminho_xml):
    logging.info(f'Iniciando a leitura do arquivo: {caminho_xml}')
    try:
        # Definir o namespace do XML
        ns = {'ns': 'http://www.dfpc.eb.mil.br'}
        tree = ET.parse(caminho_xml)
        root = tree.getroot()

        dados = []

        # Navegar pelos nós XML para extrair os dados desejados
        # Verifique se o caminho XPath está correto para o seu XML
        for produto in root.findall('ns:produto', ns):
            # variaveis dos atributos a serem extraidos
            codigo_produto = produto.get('codigoProduto')
            nome_produto = produto.get('nome')
            peso_liquido = produto.get('pesoLiquido')
            peso_bruto = produto.get('pesoBruto')






            for embalagem in produto.find('.//ns:tipoDeEmbalagem/embalagem', ns).findall('ns:itens/ns:item', ns):
                # variaveis dos atributos a serem extraidos

                nivel = embalagem.get('nivel')
                tipo_embalagem = embalagem.get('tipoEmbalagem')
                quantidade_subniveis = embalagem.get('quantidadeDeSubniveis') 
                iis = embalagem.get('iis')
                lote = embalagem.get('lote')
                produzido = embalagem.get('produzido')


                # Log para verificar os valores extraídos
                logging.info(f'Extraído: Nivel={nivel}, TipoEmbalagem={tipo_embalagem}, Subniveis={quantidade_subniveis}')

                item_embalados_dados = {
                    'tipoDeEmbalagem.embalagem.Attribute:nivel': nivel,
                    'tipoDeEmbalagem.embalagem.Attribute:tipoEmbalagem': tipo_embalagem,
                    'tipoDeEmbalagem.embalagem.Attribute:quantidadeDeSubniveis': quantidade_subniveis,
                    'item_iis': iis,
                    'item_lote': lote,
                    'item_produzido': produzido
                }
                dados.append(item_embalados_dados)

        logging.info(f'Extração de dados concluída para o arquivo: {caminho_xml}')
        return dados

    except Exception as e:
        logging.error(f'Erro ao processar o arquivo {caminho_xml}: {e}')
        return []

    except Exception as e:
        logging.error(f'Erro ao processar o arquivo {caminho_xml}: {e}')
        return []

# função para processar vários arquivos XML e gerar uma planilha Excel
def processar_xml_para_excel(diretorio_xml, arquivo_saida):
    #log
    logging.info(f'Iniciando o processamento dos arquivos XML no diretório: {diretorio_xml}')
    # array vazia para carregar os dados extraidos
    todos_os_dados = []

    try:
        # Percorrer os arquivos XML no diretório
        for arquivo in os.listdir(diretorio_xml):
            if arquivo.endswith('.xml'):
                caminho_xml = os.path.join(diretorio_xml, arquivo)
                # log
                logging.info(f'Processando o arquivo: {caminho_xml}')

                dados = extrair_dados_xml(caminho_xml)
                if dados:
                    todos_os_dados.extend(dados)
                else:
                    # log
                    logging.warning(f'Nenhum dado foi extraído do arquivo: {caminho_xml}')

        # verifica se os dados foram extraidos e chamando a array vazia agora com os dados
        if todos_os_dados:
            # converter os dados para um dataframe do pandas
            df = pd.DataFrame(todos_os_dados)

            # salva os dados em um arquivo Excel
            df.to_excel(arquivo_saida, index=False)
            logging.info(f'Arquivo Excel gerado com sucesso: {arquivo_saida}')
        else:
            logging.warning('Nenhum dado foi extraído de nenhum arquivo XML.')

    except Exception as e:
        logging.error(f'Erro ao processar o diretório {diretorio_xml} ou ao gerar o Excel: {e}')

# Exemplo de uso
diretorio_xml = r'C:\Users\Pedra\Desktop\script xml\entradas_xml'
arquivo_saida = r'C:\Users\Pedra\Desktop\script xml\saida/tabela_mesclada.xlsx'

# Executa a função para gerar o Excel
processar_xml_para_excel(diretorio_xml, arquivo_saida)


# mesclando dados

