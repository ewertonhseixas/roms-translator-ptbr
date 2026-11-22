---
name: gba-rom-build-verify
description: >-
  Executa o pipeline seguro de compilação da ROM PT-BR (GBA, NDS ou multi-console conforme
  project_profile.json), certificação pré-build dos .md no App Validador, auditoria de
  imagens com texto (image_text_auditor.py), geração de patch IPS/BPS/xdelta e verificação pós-build.
---

# 🎮 Skill: Compilação Segura da ROM & Verificação (`gba-rom-build-verify`)

Este playbook coordena a etapa final do pipeline de engenharia do **GBA & Retro Localization Studio**, garantindo que textos e gráficos validados sejam injetados na ROM de acordo com as ferramentas específicas daquele projeto (`project_profile.json` e `docs/REGRAS_ESPECIFICAS_DO_JOGO.md`), sem corromper ponteiros ou transparências de hardware.

## 📋 Passo a Passo de Compilação e Verificação

### Passo 1: Pré-Build Quality Gate & Compatibilidade do Validador
Antes de injetar qualquer texto na ROM, execute a verificação nos arquivos `.md` que foram modificados recentemente:
```powershell
python "02_TRADUCAO_ROMS_GBA/protocolo_extracao/tools/md_validator_compat_check.py" "<pasta_ARQUIVOS_md_ou_arquivo>"
python "02_TRADUCAO_ROMS_GBA/protocolo_extracao/tools/qa_gate_hook.py" "<pasta_ARQUIVOS_md_ou_arquivo>"
```

### Passo 2: Auditoria de Gráficos e Vídeos Editados (Se Aplicável)
Se houve edição de PNGs (Tela de Título, Menus, Game Over), audite a integridade das dimensões e paletas antes da reinjeção:
```powershell
python "02_TRADUCAO_ROMS_GBA/protocolo_extracao/tools/image_text_auditor.py" -d "<pasta_graphics>" -o "<pasta_ARQUIVOS_md>/controle-de-imagens-com-texto.md"
```
- Confirme que nenhuma imagem teve sua resolução alterada e que o índice 0 da paleta permaneceu intacto (transparente).

### Passo 3: Compilação da ROM PT-BR e Geração do Patch (`.ips` / `.bps` / `.xdelta`)
1. Verifique em `project_profile.json` e `docs/REGRAS_ESPECIFICAS_DO_JOGO.md` qual é o script compilador oficial daquela ROM (ex: `Compilar_ROM_PTBR.bat` ou o script Python correspondente em `tools/`).
2. Execute o build e verifique no log de saída:
   - Total de strings/blocos injetados com sucesso.
   - Ausência de erros de estouro de buffer, desalinhamento de bytes ou colisão de ponteiros.
   - Confirmação de que a ROM original em `rom/` permaneceu 100% intocada e que a nova ROM traduzida (`*_PTBR.gba`, `*_PTBR.nds`, etc.) e o patch em `releases/` foram gerados.

### Passo 4: Atualização de Versionamento e Changelog
- Se for uma entrega de marco ou lote concluído, registre as mudanças no `CHANGELOG.md` e `VERSION.json` do projeto do jogo.
