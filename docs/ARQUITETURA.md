# Arquitetura e regras — Product Media Pipeline

Fontes: `media_pipeline/cli.py`, `pipeline.py`, `images.py`, manifest e README.

CLI → `process_directory` → Pillow/hash/normalização → JPGs + manifest JSON + contact sheet PNG. A CLI valida que a origem seja diretório e aceita canvas (default 1200); não executa serviço externo.

## Regras observadas

- Extensões aceitas: JPG/JPEG, PNG, WebP. Arquivos são ordenados e processados somente no nível imediato da pasta.
- Recorte considera bounding box alpha se houver transparência; em imagem opaca compara com o pixel do canto. É uma heurística, não segmentação semântica.
- Normalização usa margem default 110, thumbnail proporcional, canvas quadrado e composição com fundo fixo, retornando RGB.
- Nomes usam índice e slug ASCII do stem; vazio vira `product`.
- Dedupe combina SHA-256 dos bytes e equality de difference_hash visual; o manifest aponta `duplicate_of`, sem descartar o output.
- Manifest guarda dimensões entrada/saída, hashes e rastreabilidade. A contact sheet mostra resultado/duplicação quando há records.

A privacidade é a fronteira descrita no README. Não foram deduzidas decisões de negócio nem aprovados novos requisitos. [Estado atual](ESTADO-ATUAL.md).
