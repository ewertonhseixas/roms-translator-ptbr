# 🎮 GBA & Retro Localization Studio — Regras Globais de Engenharia & Tradução

Este repositório opera sob a arquitetura de estúdio em **3 Tiers** inspirada no *Claude-Code-Game-Studios*, governada pelo **[Protocolo Mestre de Extração](02_TRADUCAO_ROMS_GBA/protocolo_extracao/PROTOCOLO_MESTRE_EXTRACAO.md)** e pelo **[Protocolo Mestre de Tradução](02_TRADUCAO_ROMS_GBA/protocolo_traducao/PROTOCOLO_MESTRE_TRADUCAO.md)**.

---

## 🧭 0. Três Mandamentos Estruturais de Todo Projeto

1. **Cada ROM é um Caso à Parte de Engenharia (`project_profile.json` + `docs/REGRAS_ESPECIFICAS_DO_JOGO.md`):**
   - Ao iniciar qualquer novo projeto, os agentes e skills devem avaliar a ROM em questão, o console (`GBA`, `NDS`, `SNES`, `Mega Drive`, `PS1`), a arquitetura de ponteiros/compressão, a fonte (`VWF`, monoespaçada, `NFTR`) e selecionar/construir as ferramentas necessárias para aquele caso específico.
   - As particularidades e limites calibrados da ROM são registrados em `project_profile.json` e `docs/REGRAS_ESPECIFICAS_DO_JOGO.md`, podendo adaptar o comportamento dos agentes e skills para aquele jogo.
2. **Soberania do Glossário Global de Cada Jogo & Determinância de Série/Spinoffs:**
   - **Cada jogo DEVE ter o SEU Glossário Global Soberano** em `ARQUIVOS md/02-glossario-e-terminologias.md` (ou `02-glossario-*.md`).
   - Quando o jogo pertencer a uma série ou for um *spinoff* (ex: franquia *Summon Night*, franquia *Tales of*), seu glossário local deve estar sincronizado de forma determinante com o **Glossário Global daquela Série** (`protocolo_traducao/GLOSSARIO_GLOBAL_<SERIE>.md`, vinculado em `project_profile.json`), garantindo 100% de consistência entre títulos do mesmo universo sem jamais misturar franquias diferentes.
3. **Compatibilidade Determinística com o App de Validação de Textos (`md_validator_compat_check.py`):**
   - É **determinante** que todo arquivo `.md` de textos retirado da ROM funcione perfeitamente no App de Validação de Textos (`translation_validator_app.py`).
   - O agente `md-validator-integrator` e a skill `validator-md-compliance` devem validar todo `.md` extraído ou editado executando `md_validator_compat_check.py`.

---

## 🏛️ 1. Hierarquia de Personas e Agentes (`.agents/agents/`)

- **Tier 1 (Direção & Engenharia Reversa):**
  - `gba-localization-director`: Showrunner, guardião do Glossário Soberano de cada Jogo (e do Glossário da Série/Spinoffs), do Catálogo de Personagens e da Fase 0 obrigatória.
  - `gba-rom-hacking-director`: Arquiteto de engenharia reversa multi-console (ARM7TDMI, ARM9/NitroFS, etc.), ponteiros, fontes VWF/NFTR e compilação de ROMs.
  - `rom-reverse-engineering-scout`: Batedor técnico que diagnostica uma ROM nova do zero, avalia console/compressão/ferramentas e gera `project_profile.json` e `docs/REGRAS_ESPECIFICAS_DO_JOGO.md`.
- **Tier 2 (Liderança de Pipeline & Integração):**
  - `md-validator-integrator`: Guardião do App Validador (`translation_validator_app.py`), responsável por rodar `md_validator_compat_check.py --autofix` e garantir que 100% dos `.md` funcionem na UI.
  - `gba-narrative-lead`: Criador das fichas de voz (*Character Voice*), gestor da sincronia de glossários e fatiador de contexto cirúrgico (`token_optimizer_batcher.py`).
  - `gba-graphics-ui-lead`: Auditor de imagens com texto (`image_text_auditor.py`), fontes acentuadas e proteção do índice 0 de paleta.
  - `multimedia-fmv-lead`: Especialista em extração, transcrição, legendagem (`.srt`/`.ass`) e reinjeção de vídeos FMV (`Mobiclip` `.mods`/`MOC4`, `ffmpeg`).
- **Tier 3 (Especialistas de Execução):**
  - `gba-dialogue-translator`: Tradutor dramatúrgico de lotes de história (respeitando o `hard_limit` do `project_profile.json`, gênero neutro para `{PLAYER}` quando selecionável, zero abreviações).
  - `gba-system-arsenal-translator`: Especialista em UI, menus e equipamentos (`03-` e `06-`), utilizando a Tabela Canônica de Abreviações.
  - `gba-strict-qa-auditor`: Auditor implacável que executa `md_validator_compat_check.py`, `qa_gate_hook.py` e `metrics_analyzer.py`.

### ⚡ Skills Operacionais (`.agents/skills/`)
- `rom-project-kickoff`: Kickoff universal multi-console com estudo de engenharia da ROM, criação do `project_profile.json`, Glossário do Jogo e certificação no App Validador.
- `gba-new-game-kickoff` & `nds-new-game-kickoff`: Playbooks específicos de extração e preparação para GBA e Nintendo DS.
- `validator-md-compliance`: Certificação e reparo automático de tabelas `.md` para o App de Validação de Textos.
- `franchise-glossary-sync`: Sincronização terminológica entre o Glossário Soberano do Jogo e o Glossário da Série/Spinoffs.
- `gba-character-bible`: Fase 0 obrigatória (mapeamento de falantes, *Character Voice* e glossário antes da tradução).
- `gba-translate-sprint`: Orquestração de sprints de tradução com Contexto Cirúrgico (*Token Economy*) e validação imediata.
- `gba-qa-gate`: Funil completo de auditoria (`md_validator_compat_check.py` + `qa_gate_hook.py` + `metrics_analyzer.py`).
- `gba-rom-build-verify`: Pipeline seguro de compilação da ROM PT-BR, auditoria gráfica e geração de patch.

---

## 🔒 2. Regras Invioláveis por Escopo de Arquivo (Path-Scoped Guidelines)

### A. Ao editar Lotes de Diálogos de História (`**/ARQUIVOS md/*.md`, exceto `02-`, `03-`, `06-`)
1. **Fase 0 e Perfil da ROM Obrigatórios:** Consulte sempre `project_profile.json`, `docs/REGRAS_ESPECIFICAS_DO_JOGO.md`, `catalogo-de-personagens.md` e o Glossário Soberano do Jogo (`02-glossario-*.md`) antes de traduzir.
2. **Métricas de Linha:** Separe linhas na mesma caixa exclusivamente com `<br>`. Mantenha cada linha dentro do `ideal_limit` (1–32 chars) ou `soft_limit` (33–35 chars), jamais ultrapassando o `hard_limit` definido no `project_profile.json` da ROM (padrão: **35 caracteres** no GBA).
3. **Neutralidade de Gênero Sistêmica:** Quando o protagonista tiver gênero selecionável (`selectable_neutral`), jamais use adjetivos masculinos/femininos diretos para `{PLAYER}` (ex: proibido *"cansado"*, *"pronto"*, *"corajoso"*, *"bem-vindo"*, *"obrigado/a"*). Use substantivos e locuções neutras (*"O cansaço bateu?"*, *"Tudo pronto?"*, *"Você agiu com muita coragem!"*, *"Boas-vindas!"*, *"Agradeço de coração!"*).
4. **Proibição Absoluta de Abreviações:** Nunca use `vc`, `tb`, `pq`, `atq.`, `esp.` em diálogos narrativos.
5. **Prevenção de Orfandade:** Nunca deixe artigos ou preposições curtas (`o`, `a`, `de`, `do`, `da`, `em`, `e`, `que`) isolados no fim de uma linha antes de `<br>`.

### B. Ao editar Menus e Equipamentos (`**/03-mensagens-do-sistema.md`, `**/06-itens-*.md`)
1. Elimine 100% do inglês (*Victory -> Vitória*, *Equip -> Equipar*, *Guard -> Defesa*, *Miss -> Errou*).
2. Utilize apenas as abreviações canônicas quando houver restrição de largura: `ATQ`, `DEF`, `AGI`, `DUR`, `HP`, `Recup.`, `Esp.`, `Elem.`, `Mach.`, `Lanç.`, `Soq.`, `Broc.`, `Min.`, `Nv.`, `A` (Andar).

### C. Quality Gate & Certificação do Validador Obrigatórios Pós-Edição
- Sempre que concluir a extração, tradução ou edição de um arquivo `.md`, execute o Quality Gate e o Certificador do App Validador antes de dar a tarefa por encerrada:
  1. `python "02_TRADUCAO_ROMS_GBA/protocolo_extracao/tools/md_validator_compat_check.py" "<caminho_do_arquivo.md>"`
  2. `python "02_TRADUCAO_ROMS_GBA/protocolo_extracao/tools/qa_gate_hook.py" "<caminho_do_arquivo.md>"`
