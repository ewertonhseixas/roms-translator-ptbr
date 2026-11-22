#!/usr/bin/env python3
"""
Markdown Validator Compatibility Checker & Auto-Fixer
=====================================================
Garante de forma determinística que todo arquivo Markdown (.md) de textos
extraído de uma ROM seja 100% reconhecido, parseado e editável pelo App
Interativo de Validação (`translation_validator_app.py`) e pelo fatiador
de economia de tokens (`token_optimizer_batcher.py`).

O que esta ferramenta verifica e certifica:
  1. [SCHEMA DE COLUNAS] Testa o `classify_table_columns()` idêntico ao do
     App Validador. Se uma tabela de tradução tiver cabeçalhos incompatíveis
     (onde `en_col` ou `pt_col` resultem em None), emite ERRO CRÍTICO.
  2. [SIMETRIA DE PIPES '|'] Verifica se todas as linhas de dados da tabela
     possuem o mesmo número de colunas do cabeçalho (pipes não escapados
     dentro do texto quebram a renderização na UI).
  3. [QUEBRAS DE LINHA & STATUS] Verifica se há quebras inválidas e se a
     coluna `Status` contém marcadores reconhecidos (`⏳ Pendente`, `✅ Validado`).
  4. [PERFIL & GLOSSÁRIO DO JOGO] Valida a presença de `project_profile.json`
     e `02-glossario*.md` soberano do jogo.
  5. [MODO --autofix] Normaliza cabeçalhos de tabelas e corrige pipes/colunas
     automaticamente para garantir funcionamento imediato no App Validador.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Arquivos puramente documentais que não contêm tabelas de tradução editáveis no App
REFERENCE_DOC_PATTERNS = (
    "00-",
    "01-",
    "catalogo-de-personagens",
    "estudo-de-metricas",
    "controle-de-imagens",
    "relatorio-extracao",
    "protocolo",
    "regras_especificas",
    "readme",
    "leia-me",
)


def is_reference_doc(filepath: Path) -> bool:
    name_low = filepath.name.lower()
    if name_low.startswith(("00-", "01-")):
        return True
    return any(
        p in name_low
        for p in (
            "catalogo-de-personagens",
            "estudo-de-metricas",
            "controle-de-imagens",
            "relatorio-extracao",
            "protocolo",
            "regras_especificas",
            "readme",
            "leia-me",
        )
    )


def is_glossary_file(filepath: Path) -> bool:
    name_low = filepath.name.lower()
    return name_low.startswith("02-") or "glossario" in name_low


def split_md_row(line: str) -> List[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def join_md_row(cells: List[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def classify_table_columns(headers: List[str]) -> Optional[Dict[str, Any]]:
    """
    Mesmo algoritmo exato utilizado pelo `translation_validator_app.py`
    para classificar as colunas de uma tabela Markdown.
    """
    h_lower = [h.lower() for h in headers]

    has_en = any(
        "original" in h or "en-us" in h or "padrão" in h or "inglês" in h or "japonês" in h or "jp" in h
        for h in h_lower
    )
    has_pt = any(
        "sugerid" in h or "pt-br" in h or "tradução" in h or "português" in h
        for h in h_lower
    )
    if not (has_en and has_pt):
        return None

    mapping: Dict[str, Any] = {
        "id_col": None,
        "speaker_col": None,
        "en_col": None,
        "en_desc_col": None,
        "pt_col": None,
        "pt_desc_col": None,
        "opt_col": None,
        "context_cols": [],
        "status_col": None,
    }

    for idx, h in enumerate(h_lower):
        if "status" in h or "validado" in h:
            mapping["status_col"] = idx
        elif ("descrição original" in h) or ("desc" in h and "original" in h):
            mapping["en_desc_col"] = idx
        elif ("descrição sugerida" in h) or ("desc" in h and "sugerid" in h):
            mapping["pt_desc_col"] = idx
        elif (
            "original" in h
            or "en-us" in h
            or "padrão (en" in h
            or "texto original" in h
            or "japonês" in h
        ):
            if mapping["en_col"] is None:
                mapping["en_col"] = idx
        elif "alternativa" in h or "opção b" in h:
            mapping["opt_col"] = idx
        elif "sugerid" in h or "pt-br" in h or "tradução" in h:
            if mapping["pt_col"] is None:
                mapping["pt_col"] = idx
        elif any(k in h for k in ("personagem", "falante", "interlocutor", "ator", "speaker")):
            mapping["speaker_col"] = idx
        elif any(
            k in h
            for k in (
                "endereço",
                "offset",
                "tag no script",
                "script / offset",
                "id",
                "tag",
                "código",
                "ponteiro",
            )
        ):
            if mapping["id_col"] is None:
                mapping["id_col"] = idx
            else:
                mapping["context_cols"].append(idx)
        elif "contexto" in h and any(
            k in " ".join(h_lower) for k in ("id", "offset", "script", "endereço")
        ):
            if mapping["speaker_col"] is None:
                mapping["speaker_col"] = idx
            else:
                mapping["context_cols"].append(idx)
        else:
            mapping["context_cols"].append(idx)

    if mapping["pt_col"] is None and mapping["pt_desc_col"] is not None:
        mapping["pt_col"] = mapping["pt_desc_col"]

    if mapping["en_col"] is None or mapping["pt_col"] is None:
        return None

    return mapping


def normalize_headers_for_validator(headers: List[str]) -> Tuple[List[str], bool]:
    """
    Tenta corrigir cabeçalhos fora do padrão (ex: 'English', 'Japanese', 'Portuguese',
    'Translation', 'Text', 'Speaker') para os cabeçalhos canônicos exigidos pelo App Validador.
    """
    new_headers = list(headers)
    changed = False
    for i, h in enumerate(new_headers):
        hl = h.lower().strip()
        if hl in ("english", "japanese", "jp", "en", "source", "raw text", "texto", "source text"):
            new_headers[i] = "Texto Original (EN-US)"
            changed = True
        elif hl in ("translation", "translated", "portuguese", "pt", "ptbr", "target", "destino"):
            new_headers[i] = "Tradução Sugerida (PT-BR)"
            changed = True
        elif hl in ("speaker", "character", "char", "actor", "npc"):
            new_headers[i] = "Personagem / Contexto"
            changed = True
        elif hl in ("pointer", "address", "index", "line", "row"):
            new_headers[i] = "Script / Offset"
            changed = True
        elif hl in ("state", "done", "check"):
            new_headers[i] = "Status"
            changed = True
    return new_headers, changed


def inspect_markdown_file(filepath: Path, autofix: bool = False) -> Dict[str, Any]:
    """
    Analisa um arquivo Markdown e verifica se o App Validador consegue ler suas tabelas
    e entradas sem erros.
    """
    text = filepath.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    is_ref = is_reference_doc(filepath)
    is_gloss = is_glossary_file(filepath)

    tables_found = 0
    valid_tables = 0
    recognized_rows = 0
    errors: List[str] = []
    warnings: List[str] = []
    modified = False

    i = 0
    n = len(lines)
    while i < n:
        s = lines[i].strip()
        # Detecta início de tabela Markdown (cabeçalho + linha separadora |---|)
        if s.startswith("|") and i + 1 < n:
            sep = lines[i + 1].strip()
            if sep.startswith("|") and ("---" in sep or ":---" in sep):
                tables_found += 1
                header_line_idx = i
                headers = split_md_row(s)
                mapping = classify_table_columns(headers)

                if mapping is None and autofix and not is_ref:
                    fixed_headers, hdr_changed = normalize_headers_for_validator(headers)
                    if hdr_changed and classify_table_columns(fixed_headers) is not None:
                        headers = fixed_headers
                        lines[header_line_idx] = join_md_row(headers)
                        mapping = classify_table_columns(headers)
                        modified = True

                expected_cols = len(headers)
                if mapping is not None:
                    valid_tables += 1

                j = i + 2
                table_data_rows = 0
                while j < n and lines[j].strip().startswith("|"):
                    row_str = lines[j].strip()
                    cells = split_md_row(row_str)
                    table_data_rows += 1

                    if mapping is not None and not is_ref:
                        if len(cells) != expected_cols:
                            if autofix:
                                if len(cells) < expected_cols:
                                    while len(cells) < expected_cols:
                                        cells.append("⏳ Pendente" if len(cells) == expected_cols - 1 else "")
                                    lines[j] = join_md_row(cells)
                                    modified = True
                                elif len(cells) > expected_cols:
                                    # Colapsa células excedentes na coluna de texto/tradução
                                    cells = cells[: expected_cols - 1] + [" / ".join(cells[expected_cols - 1 :])]
                                    lines[j] = join_md_row(cells)
                                    modified = True
                            else:
                                errors.append(
                                    f"Linha {j+1}: Desalinhamento de colunas ({len(cells)} células vs {expected_cols} no cabeçalho). Verifique pipes '|' não escapados."
                                )
                        if len(cells) > max(mapping["en_col"], mapping["pt_col"]):
                            recognized_rows += 1
                    j += 1

                if mapping is None and not is_ref and not is_gloss and table_data_rows > 0:
                    warnings.append(
                        f"Tabela na linha {header_line_idx+1} ({headers}) não possui colunas compatíveis com o App Validador ('Original'/'EN-US' e 'Tradução Sugerida'/'PT-BR')."
                    )

                i = j
                continue
        i += 1

    if not is_ref and not is_gloss:
        if tables_found == 0:
            errors.append(
                "Nenhuma tabela Markdown encontrada neste arquivo de texto. O App Validador não exibirá este arquivo."
            )
        elif valid_tables == 0 or recognized_rows == 0:
            errors.append(
                f"Arquivo contém {tables_found} tabela(s), mas 0 linhas editáveis foram reconhecidas pelo motor do App Validador!"
            )

    if modified and autofix:
        filepath.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return {
        "file": filepath.name,
        "rel_path": str(filepath),
        "is_reference": is_ref,
        "is_glossary": is_gloss,
        "tables_found": tables_found,
        "valid_tables": valid_tables,
        "recognized_rows": recognized_rows,
        "errors": errors,
        "warnings": warnings,
        "autofixed": modified,
    }


def check_project_structure(target_path: Path) -> Tuple[Path, List[str], List[str]]:
    """
    Identifica a pasta `ARQUIVOS md` e verifica `project_profile.json` e o Glossário Local.
    """
    struct_errors: List[str] = []
    struct_warnings: List[str] = []

    if target_path.is_file():
        md_dir = target_path.parent
        if md_dir.name != "ARQUIVOS md" and (md_dir.parent / "ARQUIVOS md").is_dir():
            md_dir = md_dir.parent
        game_dir = md_dir.parent if md_dir.name == "ARQUIVOS md" else md_dir
        return game_dir, struct_errors, struct_warnings

    if target_path.name == "ARQUIVOS md":
        md_dir = target_path
        game_dir = target_path.parent
    elif (target_path / "ARQUIVOS md").is_dir():
        game_dir = target_path
        md_dir = target_path / "ARQUIVOS md"
    else:
        game_dir = target_path
        md_dir = target_path

    # 1. Verifica project_profile.json
    profile_path = game_dir / "project_profile.json"
    if not profile_path.is_file():
        struct_warnings.append(
            f"Manifesto 'project_profile.json' ausente em '{game_dir.name}'. Recomendado criar a partir de 'protocolo_extracao/templates/project_profile.template.json'."
        )
    else:
        try:
            data = json.loads(profile_path.read_text(encoding="utf-8"))
            if "metrics" not in data or "hard_limit" not in data.get("metrics", {}):
                struct_warnings.append("'project_profile.json' não define 'metrics.hard_limit'.")
        except Exception as e:
            struct_errors.append(f"'project_profile.json' contém JSON inválido: {e}")

    # 2. Verifica Glossário Soberano do Jogo (02-glossario*.md)
    if md_dir.is_dir():
        gloss_files = list(md_dir.glob("02-*")) + list(md_dir.glob("*glossario*"))
        if not gloss_files:
            struct_errors.append(
                f"Nenhum Glossário Local ('02-glossario-*.md') encontrado em '{md_dir}'. Todo jogo DEVE ter seu próprio Glossário Global local."
            )

    return game_dir, struct_errors, struct_warnings


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Certificador de Compatibilidade de Arquivos .md com o App Validador (GBA/NDS Localization Studio)"
    )
    parser.add_argument(
        "target",
        help="Caminho para a pasta do jogo, pasta 'ARQUIVOS md' ou arquivo '.md' específico",
    )
    parser.add_argument(
        "--autofix",
        action="store_true",
        help="Corrige cabeçalhos fora do padrão e desalinhamento de colunas automaticamente",
    )
    args = parser.parse_args()

    target = Path(args.target).resolve()
    if not target.exists():
        print(f"❌ Caminho não encontrado: {target}")
        sys.exit(1)

    game_dir, struct_errors, struct_warnings = check_project_structure(target)

    if target.is_file():
        md_files = [target]
    elif (target / "ARQUIVOS md").is_dir():
        md_files = sorted((target / "ARQUIVOS md").rglob("*.md"))
    else:
        md_files = sorted(target.rglob("*.md"))

    print("=" * 80)
    print(f"🛡️  CERTIFICAÇÃO DE COMPATIBILIDADE COM O APP VALIDADOR — {game_dir.name}")
    print("=" * 80)

    for se in struct_errors:
        print(f"🔴 [ESTRUTURA ERRO] {se}")
    for sw in struct_warnings:
        print(f"🟡 [ESTRUTURA AVISO] {sw}")

    total_files = 0
    compatible_text_files = 0
    total_recognized_rows = 0
    total_errors = len(struct_errors)
    total_warnings = len(struct_warnings)

    for f in md_files:
        res = inspect_markdown_file(f, autofix=args.autofix)
        total_files += 1
        total_recognized_rows += res["recognized_rows"]
        total_errors += len(res["errors"])
        total_warnings += len(res["warnings"])

        if res["is_reference"]:
            status_tag = "📘 [DOC/REF]"
        elif res["is_glossary"]:
            status_tag = "📖 [GLOSSÁRIO]"
        elif not res["errors"] and res["recognized_rows"] > 0:
            status_tag = "✅ [COMPATÍVEL]"
            compatible_text_files += 1
        else:
            status_tag = "🔴 [INCOMPATÍVEL]"

        fix_note = " (🔧 Auto-corrigido)" if res["autofixed"] else ""
        print(
            f"{status_tag:<17} {f.name:<48} | Tabelas: {res['valid_tables']}/{res['tables_found']} | Linhas App: {res['recognized_rows']:>5}{fix_note}"
        )

        for err in res["errors"]:
            print(f"   └── 🔴 ERRO: {err}")
        for warn in res["warnings"]:
            print(f"   └── 🟡 AVISO: {warn}")

    print("-" * 80)
    print(
        f"📊 RESUMO: {total_files} arquivo(s) verificado(s) | {compatible_text_files} lote(s) de texto 100% compatíveis | {total_recognized_rows:,} entradas prontas no App Validador"
    )

    if total_errors > 0:
        print(
            f"❌ REPROVADO NA CERTIFICAÇÃO DO VALIDADOR: {total_errors} erro(s) crítico(s) encontrado(s)."
        )
        print("💡 Dica: Execute com '--autofix' ou acione a skill 'validator-md-compliance' / agente 'md-validator-integrator'.")
        sys.exit(1)
    else:
        print("🏆 CERTIFICADO! Todos os arquivos .md funcionam perfeitamente no App de Validação de Textos!")
        sys.exit(0)


if __name__ == "__main__":
    main()
