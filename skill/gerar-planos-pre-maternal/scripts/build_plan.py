#!/usr/bin/env python3
import argparse
import json
import re
from datetime import datetime, timedelta
from hashlib import sha256
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from lxml import etree


W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML = "http://www.w3.org/XML/1998/namespace"
NS = {"w": W}
TEMPLATE_SHA256 = "a2a0609bd044d144ba9b76b4c08110d3a5fd188a25acd3b3ad0199202ef9f388"

FIELD_LABELS = [
    ("eu-outro-nos", "O EU, O OUTRO E O NÓS"),
    ("corpo-gestos-movimentos", "CORPO, GESTOS E MOVIMENTOS"),
    ("tracos-sons-cores-formas", "TRAÇOS, SONS, CORES E FORMAS"),
    ("escuta-fala-pensamento-imaginacao", "ESCUTA, FALA, PENSAMENTO E IMAGINAÇÃO"),
    ("espacos-tempos-quantidades", "ESPAÇOS, TEMPOS, QUANTIDADES"),
]
RIGHT_LABELS = [
    ("conviver", "CONVIVER"),
    ("brincar", "BRINCAR"),
    ("participar", "PARTICIPAR"),
    ("explorar", "EXPLORAR"),
    ("expressar", "EXPRESSAR"),
    ("conhecer-se", "CONHECER-SE"),
]
WEEKDAYS = ["SEGUNDA-FEIRA", "TERÇA-FEIRA", "QUARTA - FEIRA", "QUINTA-FEIRA", "SEXTA-FEIRA"]
OBJECTIVE_CAPACITY = [3, 4, 3, 4, 3]
ROUTINE_CAPACITY = [4, 3, 2, 2, 2]
EXPECTED_ROWS = [9, 9, 8, 9, 9]
FIELD_BY_OBJECTIVE_AREA = {
    "EO": "eu-outro-nos",
    "CG": "corpo-gestos-movimentos",
    "TS": "tracos-sons-cores-formas",
    "EF": "escuta-fala-pensamento-imaginacao",
    "ET": "espacos-tempos-quantidades",
}


def fail(message):
    raise ValueError(message)


def parse_date(value):
    for pattern in ("%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(value, pattern).date()
        except ValueError:
            pass
    fail(f"Data inválida: {value}")


def validate_payload(payload):
    days = payload.get("days")
    if not isinstance(days, list) or len(days) != 5:
        fail("A entrada deve conter exatamente cinco dias.")

    parsed_dates = [parse_date(day.get("date", "")) for day in days]
    if parsed_dates[0].weekday() != 0 or [date.weekday() for date in parsed_dates] != list(range(5)):
        fail("As datas devem formar uma semana de segunda a sexta.")
    if any(parsed_dates[i] + timedelta(days=1) != parsed_dates[i + 1] for i in range(4)):
        fail("As cinco datas devem ser consecutivas.")

    valid_fields = {key for key, _ in FIELD_LABELS}
    valid_rights = {key for key, _ in RIGHT_LABELS}
    for index, day in enumerate(days):
        fields = day.get("fields")
        rights = day.get("rights")
        objectives = day.get("objectives")
        routine = day.get("routine")
        evaluation = day.get("evaluation")

        if not isinstance(fields, list) or not fields or set(fields) - valid_fields:
            fail(f"Dia {index + 1}: campos de experiências inválidos.")
        if not isinstance(rights, list) or not rights or set(rights) - valid_rights:
            fail(f"Dia {index + 1}: direitos de aprendizagem inválidos.")
        if not isinstance(objectives, list) or len(objectives) != OBJECTIVE_CAPACITY[index]:
            fail(f"Dia {index + 1}: usar {OBJECTIVE_CAPACITY[index]} objetivos.")
        if not all(re.match(r"^EI02(?:EO|CG|TS|EF|ET)\d{2}\s+–\s+", item) for item in objectives):
            fail(f"Dia {index + 1}: todos os objetivos devem começar com um código EI02 e travessão.")
        required_fields = {
            FIELD_BY_OBJECTIVE_AREA[re.match(r"^EI02(EO|CG|TS|EF|ET)", item).group(1)]
            for item in objectives
        }
        if required_fields - set(fields):
            fail(f"Dia {index + 1}: marque os campos correspondentes a todos os objetivos escolhidos.")
        if not isinstance(routine, list) or len(routine) != ROUTINE_CAPACITY[index]:
            fail(f"Dia {index + 1}: usar {ROUTINE_CAPACITY[index]} parágrafos de rotina.")
        if not routine[0].startswith("RODA DE CONVERSA") or not routine[1].startswith("ATIVIDADE DIRIGIDA"):
            fail(f"Dia {index + 1}: iniciar a rotina com RODA DE CONVERSA e ATIVIDADE DIRIGIDA.")
        if not isinstance(evaluation, list) or len(evaluation) != 6:
            fail(f"Dia {index + 1}: usar uma introdução e cinco critérios de avaliação.")

    return days, parsed_dates


def paragraph_text(paragraph):
    return "".join(paragraph.xpath(".//w:t/text()", namespaces=NS))


def run_is_bold(run):
    bold = run.find("./w:rPr/w:b", namespaces=NS)
    if bold is None:
        return False
    return bold.get(f"{{{W}}}val") not in {"0", "false", "off"}


def set_node_text(node, text):
    node.text = text
    if text.startswith(" ") or text.endswith(" "):
        node.set(f"{{{XML}}}space", "preserve")
    else:
        node.attrib.pop(f"{{{XML}}}space", None)


def replace_paragraph(paragraph, text, *, labeled=False, objective=False):
    nodes = paragraph.xpath(".//w:t", namespaces=NS)
    if not nodes and not text:
        return
    if not nodes:
        fail("O modelo contém um parágrafo sem espaço de texto reutilizável.")

    for node in nodes:
        set_node_text(node, "")
    if not text:
        return

    bold_nodes = []
    normal_nodes = []
    for run in paragraph.xpath("./w:r", namespaces=NS):
        target = bold_nodes if run_is_bold(run) else normal_nodes
        target.extend(run.xpath(".//w:t", namespaces=NS))

    separator = " – " if " – " in text else " - "
    if (labeled or objective) and separator in text and bold_nodes and normal_nodes:
        label, body = text.split(separator, 1)
        set_node_text(bold_nodes[0], label + separator)
        set_node_text(normal_nodes[0], body)
        return

    set_node_text(nodes[0], text)


def replace_cell(cell, texts, *, labeled=False, objective=False):
    paragraphs = cell.xpath("./w:p", namespaces=NS)
    if len(paragraphs) != len(texts):
        fail(f"Capacidade divergente: modelo={len(paragraphs)}, conteúdo={len(texts)}")
    for paragraph, text in zip(paragraphs, texts):
        replace_paragraph(paragraph, text, labeled=labeled, objective=objective)


def checkbox_lines(selected, labels):
    chosen = set(selected)
    return [f"({'X' if key in chosen else '   '}) {label}" for key, label in labels]


def patch_document(xml_bytes, payload, days, dates):
    root = etree.fromstring(xml_bytes, etree.XMLParser(remove_blank_text=False))
    metadata = payload.get("metadata") or {}
    week = f"{dates[0].strftime('%d/%m/%y')} a {dates[-1].strftime('%d/%m/%y')}"

    for paragraph in root.xpath("//w:body/w:p", namespaces=NS):
        text = paragraph_text(paragraph)
        if text.startswith("SEMANA:"):
            replace_paragraph(paragraph, f"SEMANA: {week}")
        elif text.startswith("TURMA:") and metadata.get("class"):
            replace_paragraph(paragraph, f"TURMA: {metadata['class'].upper()}")
        elif text.startswith("PROFESSORAS:") and metadata.get("teachers"):
            replace_paragraph(paragraph, f"PROFESSORAS: {metadata['teachers'].upper()}")

    tables = root.xpath("//w:body/w:tbl", namespaces=NS)
    if len(tables) != 5:
        fail("O modelo deve conter exatamente cinco tabelas.")

    for index, (table, day, date) in enumerate(zip(tables, days, dates)):
        rows = table.xpath("./w:tr", namespaces=NS)
        if len(rows) != EXPECTED_ROWS[index]:
            fail(f"Tabela {index + 1}: estrutura de linhas incompatível.")

        date_text = f"DATA: {date.strftime('%d/%m/%y')} – {WEEKDAYS[index]}"
        objectives = list(day["objectives"])
        if index == 0:
            objectives.insert(0, "")

        replace_cell(rows[0].xpath("./w:tc", namespaces=NS)[0], [date_text])
        replace_cell(rows[2].xpath("./w:tc", namespaces=NS)[1], checkbox_lines(day["fields"], FIELD_LABELS))
        replace_cell(rows[4].xpath("./w:tc", namespaces=NS)[0], checkbox_lines(day["rights"], RIGHT_LABELS))
        replace_cell(rows[4].xpath("./w:tc", namespaces=NS)[1], objectives, objective=True)
        replace_cell(rows[6].xpath("./w:tc", namespaces=NS)[0], day["routine"], labeled=True)
        replace_cell(rows[-1].xpath("./w:tc", namespaces=NS)[0], day["evaluation"])

    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def build(input_path, output_path, template_path):
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    days, dates = validate_payload(payload)

    if template_path.name == "modelo-planejamento-semanal.docx":
        current_hash = sha256(template_path.read_bytes()).hexdigest()
        if current_hash != TEMPLATE_SHA256:
            fail("O modelo oficial foi alterado; restaure-o antes de gerar o plano.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(template_path, "r") as source:
        patched = patch_document(source.read("word/document.xml"), payload, days, dates)
        with ZipFile(output_path, "w", compression=ZIP_DEFLATED) as target:
            for item in source.infolist():
                content = patched if item.filename == "word/document.xml" else source.read(item.filename)
                target.writestr(item, content)

    with ZipFile(output_path, "r") as result:
        if result.testzip() is not None:
            fail("O DOCX gerado está corrompido.")
    return output_path


def main():
    skill_dir = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Gera um plano semanal fiel ao modelo do Pré-Maternal.")
    parser.add_argument("--input", required=True, type=Path, help="JSON com os cinco dias")
    parser.add_argument("--output", required=True, type=Path, help="DOCX de saída")
    parser.add_argument("--template", type=Path, default=skill_dir / "assets" / "modelo-planejamento-semanal.docx")
    args = parser.parse_args()
    print(build(args.input.resolve(), args.output.resolve(), args.template.resolve()))


if __name__ == "__main__":
    main()
