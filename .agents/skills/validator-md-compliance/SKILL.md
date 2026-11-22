---
name: validator-md-compliance
description: >-
  Garante de forma determinística que todo arquivo .md de textos extraído da ROM funcione
  100% no App de Validação de Textos (translation_validator_app.py). Executa o verificador
  md_validator_compat_check.py, corrige cabeçalhos e pipes desalinhados (--autofix),
  valida o project_profile.json e homologa o atalho .bat do App Validador.
---

# 🖥️ Skill: Certificação de Compatibilidade com o App Validador (`validator-md-compliance`)

É uma regra determinante do estúdio que **todo arquivo `.md` de textos retirado de uma ROM funcione perfeitamente no App de Validação de Textos (`translation_validator_app.py`)**. Use esta skill imediatamente após extrair textos de uma ROM ou sempre que criar/modificar tabelas Markdown de tradução.

## 📋 Passo a Passo de Certificação

### Passo 1: Execução do Verificador e Auto-Fixer (`md_validator_compat_check.py`)
Execute a ferramenta oficial de certificação sobre a pasta do jogo ou pasta `ARQUIVOS md/`:
```powershell
python "02_TRADUCAO_ROMS_GBA/protocolo_extracao/tools/md_validator_compat_check.py" "<caminho_da_pasta_do_jogo_ou_arquivo.md>" --autofix
```

O script validará automaticamente:
1. **Reconhecimento de Colunas (`classify_table_columns`):** Confirma se todas as tabelas de texto possuem pares válidos `Original (EN-US/JP)` ↔ `Tradução Sugerida (PT-BR)`, além de `Script / Offset`, `Personagem / Contexto` e `Status`.
2. **Simetria de Células e Pipes (`|`):** Garante que nenhuma linha tenha pipes não escapados que desalinhem as colunas no navegador.
3. **Presença do `project_profile.json` e do Glossário Local (`02-glossario-*.md`).**

### Passo 2: Padrão de Cabeçalhos Exigido pelo App Validador
Se algum extrator gerou tabelas personalizadas que não foram reconhecidas automaticamente, ajuste o script extrator ou o cabeçalho da tabela para um dos dois formatos canônicos do `translation_validator_app.py`:

#### A. Formato para Diálogos, Menus e Sistema (`03-`, `08-`, `09-`, etc.):
```markdown
| Script / Offset | Personagem / Contexto | Texto Original (EN-US) | Tradução Sugerida (PT-BR) | Status |
| :--- | :--- | :--- | :--- | :---: |
| `0x001A` | **Herói** | `Linha 1`<br>`Linha 2` | `Linha 1`<br>`Linha 2` | ⏳ Pendente |
```

#### B. Formato Dual para Itens, Armas, Equipamentos e Bestiário (`06-`, `07-`):
```markdown
| ID / Offset | Nome Original (EN-US) | Nome Sugerido (PT-BR) | Descrição Original (EN-US) | Descrição Sugerida (PT-BR) | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `0x01` | `Iron Sword` | `Espada de Ferro` | `A sturdy sword.` | `Uma espada firme.` | ⏳ Pendente |
```

### Passo 3: Homologação do Servidor e Atalho `.bat`
1. Certifique-se de que `tools/translation_validator_app.py` e `tools/validator_ui.html` estão atualizados na pasta `tools/` do jogo.
2. Verifique se existe o atalho rápido em `00_APPS_E_ATALHOS/validator_ui_<sigla>.bat` apontando para o diretório do jogo.
3. Re-execute `md_validator_compat_check.py` sem flags e confirme o selo:
   `🏆 CERTIFICADO! Todos os arquivos .md funcionam perfeitamente no App de Validação de Textos!`
