---
name: nds-new-game-kickoff
description: >-
  Inicia estruturadamente a extração e preparação de uma nova ROM de Nintendo DS (.nds)
  avaliando a engenharia da ROM caso a caso (NitroFS/ndspy/NARC/NFTR/Mobiclip): gera
  project_profile.json e docs/REGRAS_ESPECIFICAS_DO_JOGO.md, cria o Glossário Global
  Soberano do Jogo e certifica que todos os .md extraídos funcionem no App Validador.
---

# 🚀 Skill: Kickoff & Extração de Nova ROM NDS (`nds-new-game-kickoff`)

Este playbook executa o ciclo de inicialização de um projeto de tradução de Nintendo DS dentro de `03_TRADUCAO_ROMS_NDS/jogos/`, tratando cada ROM como um caso único de engenharia.

## 📋 Passo a Passo de Execução

### Passo 1: Estrutura Padronizada
1. Crie `03_TRADUCAO_ROMS_NDS/jogos/<Nome_Do_Jogo>/` com as subpastas: `rom/`, `extracted/`, `ARQUIVOS md/`, `docs/`, `tools/`, `build/`, `releases/`.
2. Garanta que o arquivo `.nds` original esteja dentro de `rom/`. **Jamais modifique a ROM original in-place.**

### Passo 2: Fingerprint, Auditoria NitroFS & `project_profile.json`
1. Execute o detector de recursos NDS (`ndspy`):
   ```powershell
   python "03_TRADUCAO_ROMS_NDS/_ferramentas_nds/nds_feature_detector.py" "03_TRADUCAO_ROMS_NDS/jogos/<Nome_Do_Jogo>/rom/<arquivo.nds>" -o "03_TRADUCAO_ROMS_NDS/jogos/<Nome_Do_Jogo>/docs/relatorio-extracao.md"
   ```
2. Estude os pacotes da ROM (arquivos `NARC`, overlays `arm9.bin`, fontes `NFTR`, vídeos `.mods` Mobiclip) e configure o `project_profile.json` e `docs/REGRAS_ESPECIFICAS_DO_JOGO.md` com os limites reais de caracteres da fonte do jogo e vínculo de franquia (`franchise_glossary`).

### Passo 3: Extração, Glossário Soberano & 5 Pilares Markdown
1. Extraia os arquivos do NitroFS para `extracted/` e desenvolva os extratores específicos da engine em `tools/`.
2. Popule `ARQUIVOS md/` com os 5 Pilares (`02-glossario-e-terminologias.md` soberano do jogo, `03-mensagens-do-sistema.md`, `06-itens-equipamentos-e-descricoes.md`, `catalogo-de-personagens.md` e lotes de diálogos).
3. Se o jogo pertencer a uma série/spinoff (ex: *Summon Night*, *Tales of*), acione `franchise-glossary-sync`.

### Passo 4: Certificação Obrigatória no App Validador & Quality Gate
1. Certifique que 100% dos `.md` extraídos funcionem no App de Validação de Textos (`translation_validator_app.py`):
   ```powershell
   python "02_TRADUCAO_ROMS_GBA/protocolo_extracao/tools/md_validator_compat_check.py" "03_TRADUCAO_ROMS_NDS/jogos/<Nome_Do_Jogo>" --autofix
   ```
2. Aplique `metrics_analyzer.py` e `qa_gate_hook.py` (que lerão automaticamente o `hard_limit` do `project_profile.json` do jogo de NDS).
