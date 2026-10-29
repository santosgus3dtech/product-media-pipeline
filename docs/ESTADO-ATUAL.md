# Estado atual — Product Media Pipeline

Revisão documental: **13/10/2026**, America/Sao_Paulo. Git inicial limpo em `main`.

## Observado

`pyproject.toml` requer Python >=3.10 e Pillow >=11,<13; publica entrada `product-media`. Os módulos `images`, `pipeline` e `cli` tratam normalização, hashes, processamento e argumentos.

`process_directory` ordena imagens da pasta sem recursão, normaliza e exporta JPG, registra dimensions/hash/duplicate_of, grava manifest e contact sheet. Duplicados são marcados, mas **também exportados**; não há remoção automática. `normalize` usa alpha ou pixel de canto como fundo de referência.

Existem testes `test_images.py`/`test_pipeline.py`. README descreve fixtures geradas e fronteira de privacidade. Nenhuma imagem, manifest existente ou conteúdo comercial foi aberto.

## Operação

O README documenta `python scripts/generate_demo_assets.py`, `python -m media_pipeline.cli examples/input generated` e `pytest -q`, além de editable install. Todos **não executado nesta tarefa**. Não se geraram outputs nem instalaram bibliotecas.

O pipeline escreve nomes determinísticos no destino e regrava manifest; não há confirmação de overwrite no trecho lido. É necessário considerar esse efeito ao escolher destino em execução futura.

## Retomada

Última etapa comprovada: organização documental e conferência de arquivos/links. Qualidade visual, semântica de duplicação e preservação de detalhes de produto não foram validadas.

Sugestões não aprovadas:

1. Em validação autorizada, usar fixtures e destino isolado.
2. Conferir casos de fundo/transparência e falsos positivos do hash visual.
3. Registrar verificações reais e parâmetros da normalização antes de aplicar a catálogo privado.

[Arquitetura](ARQUITETURA.md) e [índice](INDEX.md).
