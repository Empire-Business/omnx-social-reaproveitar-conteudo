#!/usr/bin/env python3
"""Lê transcrições e confere trechos escolhidos, para que minutagem e citação saiam do texto real.

Uso:
  conferir_trechos.py listar <transcricao>
  conferir_trechos.py conferir <transcricao> <trechos.json>

Aceita .srt, .vtt, texto com minutagem no início da linha (12:03 ou [00:12:03]) e texto corrido.
trechos.json é uma lista: [{"id": "T1", "inicio": "12:03", "fim": "12:48"}, {"id": "T2", "citacao": "frase"}]
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

CUE = re.compile(r"(\d{1,2}:)?(\d{1,2}):(\d{2})[.,](\d{1,3})\s*-->\s*(\d{1,2}:)?(\d{1,2}):(\d{2})[.,](\d{1,3})")
LINHA_TEMPO = re.compile(r"^\s*[\[(]?(?:(\d{1,2}):)?(\d{1,2}):(\d{2})[\])]?\s*[-–:]?\s*(.+)$")
TAG = re.compile(r"<[^>]*>")


def seg(h, m, s):
    return int(h or 0) * 3600 + int(m) * 60 + int(s)


def formatar(t):
    t = int(t)
    h, m, s = t // 3600, (t % 3600) // 60, t % 60
    return f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def para_segundos(valor):
    """Converte '12:03', '01:12:03' ou '12:03,500' em segundos. Levanta ValueError se inválido."""
    if isinstance(valor, (int, float)) and not isinstance(valor, bool):
        return float(valor)
    m = re.fullmatch(r"\s*(?:(\d{1,3}):)?(\d{1,3}):(\d{2})(?:[.,]\d{1,3})?\s*", str(valor))
    if not m:
        raise ValueError(f"minutagem inválida: {valor}")
    return float(seg(m.group(1), m.group(2), m.group(3)))


def ler_texto(caminho):
    dados = Path(caminho).read_bytes()
    for cod in ("utf-8-sig", "latin-1"):
        try:
            return dados.decode(cod)
        except UnicodeDecodeError:
            continue
    return dados.decode("utf-8", "replace")


def ler_cues(texto):
    """Lê .srt ou .vtt. Devolve lista de segmentos, sem repetir linhas iguais seguidas (legenda automática repete)."""
    segmentos, atual, ultimo = [], None, None
    for linha in texto.splitlines():
        m = CUE.search(linha)
        if m:
            atual = {
                "inicio": seg((m.group(1) or "0:")[:-1], m.group(2), m.group(3)),
                "fim": seg((m.group(5) or "0:")[:-1], m.group(6), m.group(7)),
                "texto": [],
            }
            segmentos.append(atual)
            continue
        limpo = TAG.sub("", linha).strip()
        if not limpo:
            atual = None
            continue
        if atual is None:
            continue
        if limpo == ultimo:
            continue
        atual["texto"].append(limpo)
        ultimo = limpo
    resultado = []
    for s in segmentos:
        t = " ".join(s["texto"]).strip()
        if t:
            resultado.append({"inicio": s["inicio"], "fim": s["fim"], "texto": t})
    return resultado


def ler_txt_com_tempo(texto):
    segmentos = []
    for linha in texto.splitlines():
        m = LINHA_TEMPO.match(linha)
        if m:
            segmentos.append({"inicio": seg(m.group(1), m.group(2), m.group(3)), "fim": None, "texto": m.group(4).strip()})
        elif linha.strip() and segmentos:
            segmentos[-1]["texto"] += " " + linha.strip()
    for i, s in enumerate(segmentos):
        s["fim"] = segmentos[i + 1]["inicio"] if i + 1 < len(segmentos) else None  # fim da peça é desconhecido
    return segmentos


def carregar(caminho):
    """Devolve (formato, segmentos). Texto corrido vira parágrafos sem tempo."""
    texto = ler_texto(caminho)
    if CUE.search(texto):
        return ("vtt" if texto.lstrip().startswith("WEBVTT") else "srt"), ler_cues(texto)
    linhas = [l for l in texto.splitlines() if l.strip()]
    com_tempo = [l for l in linhas if LINHA_TEMPO.match(l)]
    if linhas and len(com_tempo) >= max(2, len(linhas) // 2):
        return "texto-com-minutagem", ler_txt_com_tempo(texto)
    paragrafos = [p.strip().replace("\n", " ") for p in re.split(r"\n\s*\n", texto) if p.strip()]
    return "texto-corrido", [{"inicio": None, "fim": None, "texto": p, "n": i + 1} for i, p in enumerate(paragrafos)]


def rotulo(s):
    return f"[p{s['n']}]" if s["inicio"] is None else f"[{formatar(s['inicio'])}]"


ASPAS = "\"'“”‘’"


def normalizar(t):
    t = unicodedata.normalize("NFC", t).casefold()
    t = "".join(c for c in t if c not in ASPAS)
    return re.sub(r"\s+", " ", t).strip()


def conferir_item(item, formato, segmentos):
    r = {"id": item.get("id", "?"), "ok": False}
    if "citacao" in item:
        alvo = normalizar(str(item["citacao"]))
        if not alvo:
            r["erro"] = "citação vazia"
            return r
        normal, origem, partes, pos = "", [], [], 0
        for s in segmentos:
            partes.append((pos, pos + len(s["texto"]), s))
            pos += len(s["texto"]) + 1
        original = " ".join(s["texto"] for s in segmentos)
        for i, ch in enumerate(unicodedata.normalize("NFC", original)):
            if ch in ASPAS:
                continue
            ch = " " if ch.isspace() else ch.casefold()
            if ch == " " and normal.endswith(" "):
                continue
            normal += ch
            origem.extend([i] * len(ch))
        achou = normal.find(alvo)
        if achou < 0:
            r["erro"] = "citação não encontrada no texto da peça"
            return r
        ini_o, fim_o = origem[achou], origem[achou + len(alvo) - 1] + 1
        r.update(ok=True, texto=unicodedata.normalize("NFC", original)[ini_o:fim_o])
        tocados = [s for a, b, s in partes if a < fim_o and b > ini_o]
        if tocados and tocados[0]["inicio"] is not None:
            r["inicio"] = formatar(tocados[0]["inicio"])
            if tocados[-1]["fim"] is not None:
                r["fim"] = formatar(tocados[-1]["fim"])
                r["duracao_seg"] = int(tocados[-1]["fim"] - tocados[0]["inicio"])
        elif tocados:
            r["paragrafos"] = [s["n"] for s in tocados]
        return r
    if formato == "texto-corrido":
        r["erro"] = "este texto não tem minutagem: use 'citacao'"
        return r
    try:
        ini = para_segundos(item.get("inicio"))
        fim = para_segundos(item.get("fim"))
    except ValueError as e:
        r["erro"] = str(e)
        return r
    if fim <= ini:
        r["erro"] = "o fim precisa ser depois do início"
        return r
    aberta = segmentos[-1]["fim"] is None  # texto com minutagem: não se sabe onde a peça termina
    total = max(s["inicio"] for s in segmentos) if aberta else max(s["fim"] for s in segmentos)
    if ini > total or (not aberta and ini >= total):
        r["erro"] = f"início depois do fim da peça ({formatar(total)})"
        return r
    if not aberta and fim > total:
        r["erro"] = f"fim depois do fim da peça ({formatar(total)})"
        return r
    dentro = [s for s in segmentos if (s["fim"] is None or s["fim"] > ini) and s["inicio"] < fim]
    if not dentro:
        r["erro"] = "não há fala nesse intervalo"
        return r
    r.update(ok=True, inicio=formatar(ini), fim=formatar(fim), duracao_seg=int(fim - ini),
             texto=" ".join(s["texto"] for s in dentro))
    return r


def main(argv):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if len(argv) < 3 or argv[1] not in ("listar", "conferir") or (argv[1] == "conferir" and len(argv) != 4):
        print(__doc__)
        return 2
    try:
        formato, segmentos = carregar(argv[2])
    except OSError:
        print(json.dumps({"ok": False, "erro": f"não encontrei o arquivo: {argv[2]}"}, ensure_ascii=False))
        return 2
    if not segmentos:
        print(json.dumps({"ok": False, "erro": "não encontrei texto no arquivo"}, ensure_ascii=False))
        return 1
    if argv[1] == "listar":
        print(f"# formato: {formato} | segmentos: {len(segmentos)}")
        for s in segmentos:
            print(f"{rotulo(s)} {s['texto']}")
        return 0
    try:
        itens = json.loads(ler_texto(argv[3]))
    except OSError:
        print(json.dumps({"ok": False, "erro": f"não encontrei o arquivo: {argv[3]}"}, ensure_ascii=False))
        return 2
    except json.JSONDecodeError as e:
        print(json.dumps({"ok": False, "erro": f"o JSON dos trechos está com erro na linha {e.lineno}"}, ensure_ascii=False))
        return 2
    if not isinstance(itens, list):
        print(json.dumps({"ok": False, "erro": "o JSON dos trechos precisa ser uma lista"}, ensure_ascii=False))
        return 2
    trechos = [conferir_item(i, formato, segmentos) if isinstance(i, dict) else {"id": "?", "ok": False, "erro": "item não é objeto"} for i in itens]
    problemas = sum(1 for t in trechos if not t["ok"])
    print(json.dumps({"formato": formato, "ok": problemas == 0, "com_problema": problemas, "trechos": trechos}, ensure_ascii=False, indent=2))
    return 0 if problemas == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
