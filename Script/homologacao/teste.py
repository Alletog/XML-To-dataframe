import xml.etree.ElementTree as ET

# Carregar o arquivo XML
tree = ET.parse(r'entradas_xml\PEDIDO 01 - NF 116505.xml')  # Substitua pelo caminho do seu arquivo XML
root = tree.getroot()

# Namespace do XML
namespace = {'ns': 'http://www.dfpc.eb.mil.br'}

# Iterar sobre cada produto
for produto in root.findall('ns:produto', namespace):
    codigo_produto = produto.get('codigoProduto')
    nome_produto = produto.get('nome')
    peso_liquido = produto.get('pesoLiquido')
    peso_bruto = produto.get('pesoBruto')
    
    print(f"Código do Produto: {codigo_produto}")
    print(f"Nome do Produto: {nome_produto}")
    print(f"Peso Líquido: {peso_liquido}")
    print(f"Peso Bruto: {peso_bruto}")
    print('-' * 30)

    # Iterar sobre os itens do produto
    for item in produto.find('ns:itens', namespace).findall('ns:item', namespace):
        iis = item.get('iis')
        lote = item.get('lote')
        produzido = item.get('produzido')
        
        print(f"  Item IIS: {iis}")
        print(f"  Lote: {lote}")
        print(f"  Produzido em: {produzido}")
        print('  ' + '-' * 20)
