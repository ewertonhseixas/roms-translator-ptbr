---
name: rom-project-kickoff
description: >-
  Inicia um novo projeto de tradução avaliando a ROM caso a caso: identifica o console
  (GBA, NDS, SNES, Mega Drive, PS1), seleciona as ferramentas de engenharia, gera o
  project_profile.json e docs/REGRAS_ESPECIFICAS_DO_JOGO.md, cria o Glossário Global
  Soberano do Jogo (herdando a base do Jogo-Matriz da série e adicionando apenas termos
  novos) e certifica que todos os .md extraídos funcionem no App de Validação de Textos.
---

# 🚀 Skill: Kickoff Universal de Projeto & Engenharia por ROM (`rom-project-kickoff`)

> [!IMPORTANT]
> **Premissa Inviolável:** Cada ROM é um caso à parte de engenharia a ser estudado e aplicado. Nenhum projeto novo deve usar limites cegos ou glossários de outra franquia sem antes passar por este protocolo de diagnóstico e configuração.

## 📋 Passo a Passo de Execução

### Passo 1: Avaliação do Console, ROM e Estrutura de Pastas
1. Identifique o console da ROM fornecida pelo usuário:
   - **GBA (`.gba`):** Crie a pasta em `02_TRADUCAO_ROMS_GBA/jogos/<Nome_Do_Jogo>/` copiando a estrutura de `02_TRADUCAO_ROMS_GBA/jogos/_MODELO_NOVO_JOGO/`.
   - **NDS (`.nds`):** Crie a pasta em `03_TRADUCAO_ROMS_NDS/jogos/<Nome_Do_Jogo>/` com `rom/`, `extracted/`, `ARQUIVOS md/`, `docs/`, `tools/`, `releases/`.
   - **Outros Consoles:** Estruture o diretório equivalente com as mesmas subpastas padronizadas.
2. Garanta que a ROM original esteja protegida dentro de `rom/`. **Jamais modifique a ROM original in-place.**

### Passo 2: Diagnóstico de Engenharia Reversa e Seleção de Ferramentas (`rom-reverse-engineering-scout`)
1. Execute o detector correspondente ao console:
   - **GBA:** `python "02_TRADUCAO_ROMS_GBA/protocolo_extracao/tools/rom_feature_detector.py" "<caminho_rom.gba>" -o "<pasta_jogo>/docs/relatorio-extracao.md"`
   - **NDS:** `python "03_TRADUCAO_ROMS_NDS/_ferramentas_nds/nds_feature_detector.py" "<caminho_rom.nds>" -o "<pasta_jogo>/docs/relatorio-extracao.md"`
2. Estude a arquitetura específica da ROM (tabelas de ponteiros, compressão LZ77/Huffman/NARC, codificação `.tbl`/Shift-JIS/ASCII, largura da fonte VWF/monoespaçada/NFTR e presença de vídeos FMV/Mobiclip).
3. Selecione ou desenvolva em `tools/` os scripts extratores e compiladores necessários para aquela engine.

### Passo 3: Configuração do `project_profile.json` e `docs/REGRAS_ESPECIFICAS_DO_JOGO.md`
1. Preencha o `project_profile.json` na raiz do jogo definindo:
   - `platform`, `product_code`, `franchise_id` e `franchise_glossary` (apenas se pertencer a uma série/spinoff existente; caso contrário, `null`).
   - `metrics`: `ideal_limit`, `soft_limit`, `hard_limit`, `max_lines_per_box`, `item_name_limit` e `monster_name_limit` calibrados pela fonte real da ROM.
   - `protagonist`: `gender_mode` (`selectable_neutral`, `fixed_male` ou `fixed_female`), nomes dos heróis e `player_tags`.
2. Documente em `docs/REGRAS_ESPECIFICAS_DO_JOGO.md` todas as particularidades da ROM e eventuais adaptações de regras para os agentes naquele jogo.

### Passo 4: Inicialização do Glossário Global Soberano do Jogo (`02-glossario-*.md`)
- Todo jogo **DEVE** ter o seu próprio Glossário Global em `ARQUIVOS md/02-glossario-e-terminologias.md` (ou `02-glossario-personagens-e-locais.md`).
- Se o jogo fizer parte de uma franquia ou for um *spinoff* (ex: série *Summon Night*), acione a skill `franchise-glossary-sync`: **o primeiro jogo (*Summon Night: Swordcraft Story 1*) é o que manda para todas as referências gerais**, e os novos jogos da série herdam 100% dessa base e apenas adicionam novos termos exclusivos de suas tramas (respeitando o ciclo `Termo Inteiro > Forma Abreviada nos Diálogos`).

### Passo 5: Extração Textual e Certificação Obrigatória no App Validador (`validator-md-compliance`)
1. Extraia os textos da ROM para `ARQUIVOS md/` (`02-glossario`, `03-mensagens-do-sistema`, `06-itens-equipamentos-e-descricoes`, `catalogo-de-personagens` e lotes de história `08-`, `09-`, etc.).
2. **OBRIGATÓRIO:** Execute o certificador de compatibilidade do App Validador:
   ```powershell
   python "02_TRADUCAO_ROMS_GBA/protocolo_extracao/tools/md_validator_compat_check.py" "<pasta_do_jogo>" --autofix
   ```
3. Verifique as métricas estatísticas com `metrics_analyzer.py` e audite gráficos com `image_text_auditor.py`.
4. Crie/atualize o atalho `00_APPS_E_ATALHOS/validator_ui_<codigo_jogo>.bat` e passe o bastão para a Fase 0 (`gba-character-bible`).
