---
name: gba-qa-gate
description: >-
  Executa o Funil de Qualidade, Compatibilidade com o App Validador e Auditoria Completa
  (Quality Gate) em arquivos ou pastas de tradução (.md). Combina md_validator_compat_check.py,
  qa_gate_hook.py e metrics_analyzer.py (calibrados pelo project_profile.json da ROM) com
  revisão pente-fino para eliminar overflows, choques de gênero, tags quebradas, orfandade
  textual e desvios do glossário do jogo.
---

# 🛡️ Skill: Funil de Qualidade, App Validador & Quality Gate (`gba-qa-gate`)

Inspirada nos *Quality Gates* de pré-commit e revisão do *Claude-Code-Game-Studios*, esta skill executa a bateria oficial de validação do **GBA & Retro Localization Studio**, respeitando os parâmetros específicos da ROM ativa (`project_profile.json`).

## 📋 Procedimento de Auditoria em 5 Etapas

### Etapa 1: Certificação Determinística no App Validador (`md_validator_compat_check.py`)
Garanta primeiro que todas as tabelas e linhas do arquivo ou pasta `ARQUIVOS md` são 100% reconhecidas pelo App de Validação de Textos (`translation_validator_app.py`):
```powershell
python "02_TRADUCAO_ROMS_GBA/protocolo_extracao/tools/md_validator_compat_check.py" "<caminho_alvo>" --autofix
```

### Etapa 2: Varredura com o `qa_gate_hook.py`
Execute o script de Quality Gate (que lê automaticamente o `hard_limit` e `soft_limit` do `project_profile.json` do jogo, ou aceita `-l <limite>`):
```powershell
python "02_TRADUCAO_ROMS_GBA/protocolo_extracao/tools/qa_gate_hook.py" "<caminho_alvo>"
```
O script verificará automaticamente:
- **Gate 1 (Tags):** Paridade exata de `{PLAYER}`, `{PARTNER}`, `[0x05]`, etc. entre original e PT-BR.
- **Gate 2 (Overflow):** Qualquer linha individual entre `<br>` acima do `hard_limit` de caracteres da ROM.
- **Gate 3 (Orfandade):** Artigos e preposições (`o`, `a`, `de`, `em`, `e`, `que`) pendurados no fim da linha antes de `<br>`.
- **Gate 4 (Abreviações):** Uso indevido de abreviações em lotes de história.
- **Gate 5 (Neutralidade & Inglês Residual):** Expressões suspeitas de marcação de gênero masculino no protagonista e inglês não traduzido.

### Etapa 3: Relatório Estatístico Global (`metrics_analyzer.py`)
Gere ou atualize o relatório `estudo-de-metricas-e-caracteres.md` do jogo para verificar a saúde estatística (Média, Máximo e Percentil 95 de largura de linha):
```powershell
python "02_TRADUCAO_ROMS_GBA/protocolo_extracao/tools/metrics_analyzer.py" -d "<pasta_ARQUIVOS_md>" -g "<Nome_do_Jogo>"
```

### Etapa 4: Correção Cirúrgica de Erros e Alertas
Para cada erro `🔴` ou alerta `🟡` relevante apontado nos passos anteriores:
1. Abra o arquivo `.md` nas linhas indicadas.
2. Reescreva a frase mantendo a naturalidade dramática, a consistência com o **Glossário Global do Jogo (`02-glossario-*.md`)** e o idioleto do personagem (`catalogo-de-personagens.md`), sem mutilar palavras.
3. Re-execute `qa_gate_hook.py` e `md_validator_compat_check.py` até que o resultado seja **0 erros críticos**.

### Etapa 5: Chancela de Validação
- Com todos os testes verdes, atualize o status das linhas revisadas para `✅ Validado` e informe ao usuário que o lote está pronto para visualização no App Validador e compilação na ROM (`gba-rom-build-verify`).
