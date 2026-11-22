---
name: gba-new-game-kickoff
description: >-
  Inicia estruturadamente a extração e preparação de uma nova ROM de Game Boy Advance
  (ou console retrô) avaliando a engenharia da ROM caso a caso: gera project_profile.json
  e docs/REGRAS_ESPECIFICAS_DO_JOGO.md, cria o Glossário Global Soberano do Jogo e
  certifica que todos os .md extraídos funcionem no App de Validação de Textos.
---

# 🚀 Skill: Kickoff & Extração de Nova ROM GBA (`gba-new-game-kickoff`)

Este playbook executa o ciclo completo de inicialização de um novo projeto de tradução dentro de `02_TRADUCAO_ROMS_GBA/jogos/`, garantindo aderência total ao [Protocolo Mestre de Extração](../../02_TRADUCAO_ROMS_GBA/protocolo_extracao/PROTOCOLO_MESTRE_EXTRACAO.md) e à regra de que **cada ROM é um caso à parte de engenharia**.

## 📋 Passo a Passo de Execução

### Passo 1: Clonagem do Template Padronizado
1. Verifique se a pasta do jogo já existe em `02_TRADUCAO_ROMS_GBA/jogos/<Nome_Do_Jogo>/`.
2. Caso não exista, copie a estrutura de `02_TRADUCAO_ROMS_GBA/jogos/_MODELO_NOVO_JOGO/` para `02_TRADUCAO_ROMS_GBA/jogos/<Nome_Do_Jogo>/`.
3. Confirme que o arquivo `.gba` original encontra-se dentro de `rom/`. **Jamais modifique a ROM original in-place.**

### Passo 2: Fingerprint, Estudo de Engenharia da ROM & `project_profile.json`
1. Execute o detector de recursos da suíte (`rom-reverse-engineering-scout`) para mapear cabeçalho, serial, espaço livre, compressões (LZ77/Huffman), tabelas de ponteiros e presença de vídeos (Mobiclip):
   ```powershell
   python "02_TRADUCAO_ROMS_GBA/protocolo_extracao/tools/rom_feature_detector.py" "02_TRADUCAO_ROMS_GBA/jogos/<Nome_Do_Jogo>/rom/<arquivo.gba>" -o "02_TRADUCAO_ROMS_GBA/jogos/<Nome_Do_Jogo>/docs/relatorio-extracao.md"
   ```
2. Configure o manifesto `project_profile.json` e o arquivo `docs/REGRAS_ESPECIFICAS_DO_JOGO.md` com os limites reais de tela/fonte da ROM, modo de gênero do protagonista (`selectable_neutral`, `fixed_male`, `fixed_female`) e vínculo de franquia (`franchise_glossary` se fizer parte de uma série/spinoff).

### Passo 3: Extração Estruturada para os 5 Pilares Markdown & Glossário Soberano
Construa ou execute os extratores específicos da engine na pasta `tools/` do jogo para popular `ARQUIVOS md/` com os arquivos obrigatórios compatíveis com o App Validador:
1. `02-glossario-e-terminologias.md` *(Glossário Global Soberano deste jogo, sincronizado via `franchise-glossary-sync` se pertencer a uma série/spinoff)*
2. `03-mensagens-do-sistema.md`
3. `06-itens-equipamentos-e-descricoes.md`
4. `catalogo-de-personagens.md`
5. Lotes sequenciais de diálogos (`08-`, `09-`, etc.) no formato:
   `| Script / Offset | Personagem / Contexto | Texto Original (EN-US) | Tradução Sugerida (PT-BR) | Status |`

### Passo 4: Certificação Determinística no App Validador (`validator-md-compliance`)
Garanta que 100% dos arquivos `.md` extraídos funcionem no App de Validação de Textos executando:
```powershell
python "02_TRADUCAO_ROMS_GBA/protocolo_extracao/tools/md_validator_compat_check.py" "02_TRADUCAO_ROMS_GBA/jogos/<Nome_Do_Jogo>" --autofix
```

### Passo 5: Calibração Matemática de Métricas e Imagens
1. Rode o analisador de métricas sobre os textos extraídos para confirmar o **Soft Limit** e o **Hard Limit** da caixa de diálogo:
   ```powershell
   python "02_TRADUCAO_ROMS_GBA/protocolo_extracao/tools/metrics_analyzer.py" -d "02_TRADUCAO_ROMS_GBA/jogos/<Nome_Do_Jogo>/ARQUIVOS md" -g "<Nome do Jogo>" -l 35
   ```
2. Se houver gráficos extraídos em `extracted/graphics`, gere a planilha de controle de imagens:
   ```powershell
   python "02_TRADUCAO_ROMS_GBA/protocolo_extracao/tools/image_text_auditor.py" -d "02_TRADUCAO_ROMS_GBA/jogos/<Nome_Do_Jogo>/extracted/graphics" -o "02_TRADUCAO_ROMS_GBA/jogos/<Nome_Do_Jogo>/ARQUIVOS md/controle-de-imagens-com-texto.md"
   ```

### Passo 6: Handoff para a Fase 0 (Pré-Tradução)
- Informe ao usuário o resumo técnico da ROM extraída e acione a skill `gba-character-bible` antes de traduzir qualquer diálogo.
