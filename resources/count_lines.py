import os
from pathlib import Path
from collections import defaultdict


def contar_linhas(caminho_pasta, extensoes=None, ignorar_vazias=False, ignorar_pastas=None):
    if ignorar_pastas is None:
        ignorar_pastas = []

    ignorar_pastas = [p.lower() for p in ignorar_pastas]
    total_linhas = 0
    total_arquivos = 0
    linhas_por_extensao = defaultdict(int)
    arquivos_por_extensao = defaultdict(int)

    pasta = Path(caminho_pasta)

    if not pasta.exists():
        print(f"Erro: Pasta '{caminho_pasta}' não encontrada!")
        return None

    for arquivo in pasta.rglob('*'):
        if arquivo.is_dir():
            continue

        partes_caminho = [p.lower() for p in arquivo.parts]
        if any(pasta_ignorar in partes_caminho for pasta_ignorar in ignorar_pastas):
            continue

        extensao = arquivo.suffix.lower()
        if extensoes and extensao not in extensoes:
            continue

        try:
            with open(arquivo, 'r', encoding='utf-8', errors='ignore') as f:
                if ignorar_vazias:
                    linhas = len([linha for linha in f if linha.strip()])
                else:
                    linhas = sum(1 for _ in f)

            total_linhas += linhas
            total_arquivos += 1
            linhas_por_extensao[extensao] += linhas
            arquivos_por_extensao[extensao] += 1

        except Exception as e:
            print(f"Não foi possível ler: {arquivo.name} ({e})")

    return {
        'total_linhas': total_linhas,
        'total_arquivos': total_arquivos,
        'linhas_por_extensao': dict(linhas_por_extensao),
        'arquivos_por_extensao': dict(arquivos_por_extensao)
    }


def exibir_resultados(resultados):
    if not resultados:
        return

    print("=" * 60)
    print("📊 RESULTADOS")
    print("=" * 60)
    print(f"Total de arquivos: {resultados['total_arquivos']}")
    print(f"Total de linhas: {resultados['total_linhas']:,}".replace(',', '.'))
    print("\n" + "-" * 60)
    print("Por tipo de arquivo:")
    print("-" * 60)

    extensoes_ordenadas = sorted(
        resultados['linhas_por_extensao'].items(),
        key=lambda x: x[1],
        reverse=True
    )

    for ext, linhas in extensoes_ordenadas:
        arquivos = resultados['arquivos_por_extensao'][ext]
        ext_nome = ext if ext else '(sem extensão)'
        print(f"{ext_nome:15} | {arquivos:5} arquivo(s) | {linhas:10,} linhas".replace(',', '.'))

    print("=" * 60)


if _name_ == "_main_":

    #TODO alterar pra o caminho certo
    CAMINHO = ""
    EXTENSOES = ['.cpp', '.h']
    IGNORAR_VAZIAS = False
    IGNORAR_PASTAS = ['test', 'tests', '_pycache_', 'node_modules', '.git', 'venv', 'env']

    resultados = contar_linhas(CAMINHO, EXTENSOES, IGNORAR_VAZIAS, IGNORAR_PASTAS)
    exibir_resultados(resultados)