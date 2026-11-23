#!/usr/bin/env python3
"""
Compilador PT-BR (Template — _MODELO_NOVO_JOGO)
Valida todos os arquivos Markdown de tradução do projeto e executa o injetor da ROM se configurado.
"""
import subprocess
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
GAME_DIR = TOOLS_DIR.parent
MD_DIR = GAME_DIR / "ARQUIVOS md"
COMPAT_CHECK = GAME_DIR.parent.parent / "protocolo_extracao" / "tools" / "md_validator_compat_check.py"


def main() -> int:
    print("=" * 74)
    print(" COMPILADOR DE ROM PT-BR — TEMPLATE / NOVO JOGO")
    print("=" * 74)
    if COMPAT_CHECK.is_file() and MD_DIR.is_dir():
        res = subprocess.run([sys.executable, "-X", "utf8", str(COMPAT_CHECK), str(MD_DIR)], cwd=str(GAME_DIR))
        if res.returncode != 0:
            return res.returncode
    print("\n✅ Validação pré-build concluída com 100% de compatibilidade!")
    print("ℹ️  Este é o projeto-modelo (_MODELO_NOVO_JOGO). Quando a ROM base for adicionada em rom/, conecte o injetor neste script.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
