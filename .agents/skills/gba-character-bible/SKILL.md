---
name: gba-character-bible
description: >-
  Executa a Fase 0 obrigatória do Protocolo Mestre de Tradução: verifica as regras
  específicas da ROM (project_profile.json), mapeia todos os falantes, pesquisa o lore
  oficial e constrói/atualiza o Catálogo de Personagens (catalogo-de-personagens.md) e
  o Glossário Global Soberano do Jogo (02-glossario), sincronizando-o com o Glossário
  da Série/Spinoffs quando aplicável. Use antes de traduzir novos capítulos.
---

# 🎭 Skill: Bíblia de Personagens & Glossário Soberano (`gba-character-bible`)

De acordo com a **Regra de Ouro da Pré-Tradução** ([PROTOCOLO_MESTRE_TRADUCAO.md](../../02_TRADUCAO_ROMS_GBA/protocolo_traducao/PROTOCOLO_MESTRE_TRADUCAO.md)), é terminantemente proibido traduzir diálogos sem antes catalogar os falantes e estabelecer o Glossário Soberano do Jogo. Esta skill guia a atuação do **Líder de Narrativa (`gba-narrative-lead`)** e do **Diretor de Localização (`gba-localization-director`)**.

## 📋 Passo a Passo de Execução

### Passo 0: Leitura do Perfil da ROM e Certificação do Validador
1. Leia `project_profile.json` e `docs/REGRAS_ESPECIFICAS_DO_JOGO.md` para confirmar o modo de gênero do protagonista (`selectable_neutral`, `fixed_male` ou `fixed_female`), limites de linha e se o jogo pertence a uma série/franquia (`franchise_id`).
2. Confirme que os arquivos `.md` extraídos já passaram pela certificação do App Validador (`md_validator_compat_check.py`).

### Passo 1: Varredura de Falantes nos Lotes
1. Escaneie a coluna `Personagem / Contexto` dos arquivos Markdown de diálogos em `ARQUIVOS md/`.
2. Compare a lista de falantes encontrados com os já cadastrados em `ARQUIVOS md/catalogo-de-personagens.md`.

### Passo 2: Pesquisa de Biografia Híbrida (In-Game + Web Canônica)
Para cada personagem ainda não catalogado (ou com ficha incompleta):
1. Analise suas falas em inglês/japonês no dump para identificar seu vocabulário, idade aparente e relação com `{PLAYER}`.
2. Use `search_web` se necessário para consultar wikis oficiais da franquia e confirmar gênero, classe social e lore.

### Passo 3: Fixação do Idioleto (*Character Voice*)
Adicione ou atualize a entrada do personagem em `catalogo-de-personagens.md` definindo explicitamente:
- **Papel / Arquétipo:** (ex: Mestre Ferreiro, Aprendiz, Espírito Guardião, Rival Aristocrata, Vilão).
- **Gênero e Concordância:** Masculino fixo, Feminino fixo, ou Variável/Epiceno (como `{PLAYER}` em jogos `selectable_neutral`).
- **Tom de Voz & Registro:**
  - *Mestres/Veteranos:* Solene, firme, paternal, rico em metáforas de ofício.
  - *Jovens/Aprendizes:* Coloquial limpo, ágil, energético, sem gírias datadas.
  - *Nobres/Rivais:* Elegante, altivo, irônico ou competitivo.
  - *Entidades/Fadas/Bestas:* Dengoso/infantil, arcaico/místico ou rústico/direto conforme a criatura.
- **Relações Interpessoais:** Como chama o protagonista e aliados.

### Passo 4: Sincronização com o Glossário Global Soberano do Jogo (e Franquia/Spinoffs)
- Registre todos os locais, títulos, organizações, raças, magias e materiais no **Glossário Global do Jogo** (`ARQUIVOS md/02-glossario-e-terminologias.md` ou `02-glossario-*.md`).
- Se o jogo pertencer a uma série ou for um *spinoff* (configurado em `franchise_glossary` no `project_profile.json`, como `GLOSSARIO_GLOBAL_SUMMON_NIGHT.md`), garanta 100% de alinhamento com os termos determinantes da franquia usando a skill `franchise-glossary-sync`.
