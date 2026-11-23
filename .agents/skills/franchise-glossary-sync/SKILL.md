---
name: franchise-glossary-sync
description: >-
  Gerencia o Glossário Global Soberano de cada jogo (ARQUIVOS md/02-glossario-e-terminologias.md)
  e sua sincronização determinante com o Glossário Global da Série/Franquia e Spinoffs
  (protocolo_traducao/GLOSSARIO_GLOBAL_<SERIE>.md). Use ao iniciar um jogo de uma franquia,
  ao criar termos novos ou ao unificar terminologias entre jogos da mesma série.
---

# 📖 Skill: Gestão de Glossário do Jogo & Sincronização de Franquia (`franchise-glossary-sync`)

Esta skill implementa a regra determinante de terminologia do estúdio:
1. **Cada jogo DEVE ter o SEU Glossário Global Soberano** (`ARQUIVOS md/02-glossario-*.md`).
2. **Soberania do Jogo-Matriz na Série (*Summon Night: Swordcraft Story 1* do GBA):**
   - Na franquia *Summon Night*, o **Glossário Global da Série** (`02_TRADUCAO_ROMS_GBA/protocolo_traducao/GLOSSARIO_GLOBAL_SUMMON_NIGHT.md`) é focado **estritamente** no primeiro ***Summon Night: Swordcraft Story 1* (GBA)**, onde toda a localização, diálogos, itens, equipamentos, magias e bestiário foram trabalhados com maior nível de detalhe.
   - Muitos termos são introduzidos no jogo por extenso e usados de forma abreviada nos diálogos:
     - `Craftknight > Cavaleiro Forjador > Cavaleiro`
     - `Craftlord > Lorde Forjador > Lorde`
     - `Stray Summon > Invocação Errante > Errante`
   - **O primeiro jogo é o que manda para todas as referências gerais.** Os outros jogos da série (*Swordcraft Story 2*, *Swordcraft Story 3*, *Summon Night NDS*, etc.) herdam 100% dessa base e apenas adicionam novos termos exclusivos de suas tramas, sem jamais alterar ou sobrescrever os termos estabelecidos no primeiro jogo.

## 📋 Passo a Passo de Execução

### Passo 1: Verificação do Vínculo de Franquia no `project_profile.json`
1. Abra o arquivo `project_profile.json` na raiz do jogo ativo.
2. Verifique os campos:
   - `"franchise_id"`: Identificador da série (ex: `"SUMMON_NIGHT"`, `"TALES_OF"`, ou `"STANDALONE"` para jogo único).
   - `"franchise_glossary"`: Caminho para o glossário da série (ex: `"protocolo_traducao/GLOSSARIO_GLOBAL_SUMMON_NIGHT.md"`) ou `null` caso seja o único jogo daquele universo.
   - `"local_glossary"`: Caminho para o glossário soberano do jogo (`"ARQUIVOS md/02-glossario-personagens-e-locais.md"` ou `"ARQUIVOS md/02-glossario-e-terminologias.md"`).

### Passo 2: Semeadura Inicial (Ao Iniciar Novo Jogo de uma Série ou Spinoff)
Quando um novo jogo pertencer a uma série já existente no estúdio:
1. Varra os termos originais (locais, títulos, classes, elementos, itens recorrentes, magias e personagens retornantes) extraídos da nova ROM.
2. Cruze com o `GLOSSARIO_GLOBAL_<FRANQUIA>.md` da série (cuja base soberana em *Summon Night* é o `Swordcraft Story 1` do GBA).
3. Popule o `ARQUIVOS md/02-glossario-*.md` do novo jogo mantendo **exatamente** as traduções canônicas do Jogo-Matriz (Fase 1: Apresentação Completa, Fase 2: Uso Abreviado nos Diálogos, Fase 3: Abreviação de Menu).

### Passo 3: Adição de Novos Termos Exclusivos (Sem Sobrescrever o Jogo-Matriz)
Quando o `gba-localization-director` aprovar novos termos durante a Fase 0 ou durante a tradução de uma sequência/spinoff:
1. Verifique primeiro se o termo já existe no Jogo-Matriz (*Summon Night: Swordcraft Story 1*): **se já existir, a tradução do primeiro jogo prevalece obrigatoriamente.**
2. Se for um termo inédito introduzido pela sequência/spinoff, registre-o no Glossário Soberano do Jogo (`ARQUIVOS md/02-glossario-*.md`) e adicione-o na seção de suplementos/adições do `GLOSSARIO_GLOBAL_<FRANQUIA>.md`.

### Passo 4: Validação de Compatibilidade no App Validador
Após atualizar qualquer arquivo `02-glossario-*.md`, execute:
```powershell
python "02_TRADUCAO_ROMS_GBA/protocolo_extracao/tools/md_validator_compat_check.py" "<pasta_do_jogo>/ARQUIVOS md"
```
para confirmar que o App Validador carrega todos os termos do glossário em tempo real.
