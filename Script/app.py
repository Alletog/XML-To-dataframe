# importando bibliotecas
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

# função main para extrair dados especificos do xml 
def extrair_dados_xml(caminho_xml):
    # log 
    logging.info(f'Iniciando a leitura do arquivo: {caminho_xml}')
    try:
        # Definir o namespace do XML
        ns = {'ns': 'http://www.dfpc.eb.mil.br'}
        tree = ET.parse(caminho_xml)
        root = tree.getroot()

        dados = []

        # Navegar pelos nós XML para extrair os dados desejados
        for produto in root.findall('ns:produto', ns):
            for item in produto.findall('.//ns:item', ns):
                item_dados = {
                    'tipoDeEmbalagem.embalagem.Attribute:nivel': root.attrib.get('embalagem nivel'),

                    'dataExportacao': root.attrib.get('dataExportacao', ''),
                    'cnpjDeVendedor': root.attrib.get('cnpjDeVendedor', ''),
                    'numeroNotaFiscal': root.attrib.get('numeroNotaFiscal', ''),
                    'serieNotaFiscal': root.attrib.get('serieNotaFiscal', ''),
                    'guiaDeTrafego': root.attrib.get('guiaDeTrafego', ''),
                    'cnpjDeComprador': root.attrib.get('cnpjDeComprador', ''),
                    'produto_codigo': produto.attrib.get('codigoProduto', ''),
                    'produto_nome': produto.attrib.get('nome', ''),
                    'produto_pesoLiquido': produto.attrib.get('pesoLiquido', ''),
                    'item_iis': item.attrib.get('iis', ''),
                    'item_lote': item.attrib.get('lote', ''),
                    'item_produzido': item.attrib.get('produzido', '')
                }
                dados.append(item_dados)

        logging.info(f'Extração de dados concluída para o arquivo: {caminho_xml}')
        return dados

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

