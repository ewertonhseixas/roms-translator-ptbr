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
1. **Cada jogo DEVE ter o SEU Glossário Global Soberano** (`ARQUIVOS md/02-glossario-e-terminologias.md`).
2. **Determinância entre Jogos da Mesma Série e Spinoffs:** Jogos que compartilham o mesmo universo/franquia (ex: *Summon Night 1, 2, 3 e NDS*; série *Tales of*, etc.) possuem um **Glossário Global da Franquia** em `02_TRADUCAO_ROMS_GBA/protocolo_traducao/GLOSSARIO_GLOBAL_<FRANQUIA>.md` que garante 100% de consistência em termos herdados, sem jamais contaminar jogos de outras franquias.

## 📋 Passo a Passo de Execução

### Passo 1: Verificação do Vínculo de Franquia no `project_profile.json`
1. Abra o arquivo `project_profile.json` na raiz do jogo ativo.
2. Verifique os campos:
   - `"franchise_id"`: Identificador da série (ex: `"SUMMON_NIGHT"`, `"TALES_OF"`, ou `"STANDALONE"` para jogo único).
   - `"franchise_glossary"`: Caminho para o glossário da série (ex: `"protocolo_traducao/GLOSSARIO_GLOBAL_SUMMON_NIGHT.md"`) ou `null` caso seja o primeiro/único jogo daquele universo.
   - `"local_glossary"`: Caminho para o glossário soberano do jogo (`"ARQUIVOS md/02-glossario-e-terminologias.md"`).

### Passo 2: Semeadura Inicial (Ao Iniciar Novo Jogo de uma Série ou Spinoff)
Quando um novo jogo pertencer a uma série já existente no estúdio:
1. Varra os termos originais (locais, títulos, classes, elementos, itens recorrentes, magias e personagens retornantes) extraídos da nova ROM.
2. Cruze com o `GLOSSARIO_GLOBAL_<FRANQUIA>.md` da série.
3. Popule o `ARQUIVOS md/02-glossario-e-terminologias.md` do novo jogo mantendo **exatamente** as traduções canônicas já consagradas na série/spinoffs (Fase 1: Apresentação Completa, Fase 2: Uso Comum em Diálogo, Fase 3: Abreviação de Menu).

### Passo 3: Promoção de Novos Termos Canônicos (Jogo ➔ Franquia)
Quando o `gba-localization-director` aprovar novos termos universais daquele mundo durante a Fase 0 ou durante a tradução de um jogo:
1. Registre imediatamente o termo no Glossário Soberano do Jogo (`ARQUIVOS md/02-glossario-e-terminologias.md`).
2. Se o termo fizer parte do lore compartilhado da franquia (raças, magias, divindades, organizações, itens clássicos), promova-o também para o `GLOSSARIO_GLOBAL_<FRANQUIA>.md` para que futuros títulos e spinoffs da série já o herdem automaticamente.

### Passo 4: Validação de Compatibilidade no App Validador
Após atualizar qualquer arquivo `02-glossario-*.md`, execute:
```powershell
python "02_TRADUCAO_ROMS_GBA/protocolo_extracao/tools/md_validator_compat_check.py" "<pasta_do_jogo>/ARQUIVOS md"
```
para confirmar que o App Validador carrega todos os termos do glossário em tempo real.
