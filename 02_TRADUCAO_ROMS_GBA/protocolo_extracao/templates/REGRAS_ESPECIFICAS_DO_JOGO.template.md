# 🛠️ Regras Específicas de Engenharia e Localização do Jogo

> [!IMPORTANT]
> **Cada ROM é um caso à parte de engenharia.** Este documento registra as particularidades binárias, métricas de janela, opcodes de controle e exceções terminológicas exclusivas desta ROM. **Todos os Agents e Skills devem ler este arquivo e o `project_profile.json` antes de extrair, traduzir, auditar ou compilar.**

---

## 🎮 1. Identificação do Projeto & Console
- **Título do Jogo:** `[Preencher Nome do Jogo]`
- **Console / Plataforma:** `[GBA / NDS / SNES / Mega Drive / PS1]`
- **Serial / Game Code:** `[Ex: AGB-XXXX-USA / NTR-XXXX-JPN]`
- **Franquia / Universo:** `[Ex: Summon Night / Tales of / Jogo Independente]`
- **Glossário Global do Jogo:** `ARQUIVOS md/02-glossario-e-terminologias.md` *(Soberano para este jogo)*
- **Glossário da Franquia/Série (Herança):** `[Nenhum ou caminho para protocolo_traducao/GLOSSARIO_GLOBAL_<SERIE>.md]`

---

## 📐 2. Parâmetros de Tela, Fonte e Limites (`project_profile.json`)
- **Tipo de Fonte:** `[VWF Proporcional / Monoespaçada 8x8 / NFTR NDS]`
- **Ideal Limit (Zona Verde):** `1 a 32 caracteres`
- **Soft Limit (Zona Amarela):** `33 a 35 caracteres`
- **Hard Limit (Teto Físico Estrito):** `35 caracteres` *(ajustar conforme medição real da fonte na VRAM)*
- **Máximo de Linhas por Caixa:** `3 linhas` (separadas exclusivamente por `<br>`)
- **Limite de Nomes de Itens / Monstros:** `16 chars` (Itens) / `14 chars` (Monstros)

---

## 🔧 3. Particularidades de Engenharia da ROM e Ferramentas Locais
- **Codificação de Texto:** `[ASCII / Shift-JIS / UTF-8 / Tabela .tbl customizada]`
- **Tags e Variáveis Protegidas da Engine:** `{PLAYER}`, `{PARTNER}`, `[0x05]`, `<page>` *(listar todas as tags que jamais podem ser alteradas)*
- **Estrutura de Ponteiros e Compressão:** `[Descrever tabelas de ponteiros, alinhamento de bytes, NARC/NitroFS, LZ77, Huffman, etc.]`
- **Scripts de Extração e Build (`tools/`):**
  - Extrator: `tools/...`
  - Reinjetor / Compilador: `Compilar_ROM_PTBR.bat`
  - Validador Web: `Iniciar_Validador_Traducao.bat` (`tools/translation_validator_app.py`)

---

## 🎭 4. Diretrizes Narrativas e Exceções Específicas deste Jogo
- **Modo de Gênero do Protagonista:**
  - `[selectable_neutral]` Protagonista de gênero selecionável (exige **Neutralidade de Gênero Sistêmica** em falas compartilhadas para `{PLAYER}`).
  - *(Ou `[fixed_male]` / `[fixed_female]` quando o protagonista do jogo possui gênero único e fixo na obra).*
- **Regras Especiais de Adaptação para este Jogo:**
  - `[Registrar aqui quaisquer regras customizadas para os agents gba-dialogue-translator, gba-system-arsenal-translator e gba-strict-qa-auditor neste projeto]`
