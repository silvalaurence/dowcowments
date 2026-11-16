#!/usr/bin/env python3
"""Build a formal Word document from a simple markdown file.

Usage: python build_doc.py input.md output.docx

Format: Arial 12 pt, 1.15 line spacing, 1 inch margins, 0.5 inch first-line
indent on body paragraphs, numbered bold headings, info table on top,
page numbers in the footer.

Extra markdown supported on top of headings, paragraphs, lists and tables:
    ![Caption text](path/to/image.png)   picture, path relative to the .md file
    <pagebreak>                          start a new page
"""
import os
import re
import sys

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

FONT = "Arial"
SIZE = Pt(12)
SPACING = 1.15


def set_font(run, bold=None, italic=None, size=SIZE):
    run.font.name = FONT
    run.font.size = size
    run._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), FONT)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic


def style_document(doc):
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, side, Inches(1))
    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = SIZE
    normal.element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), FONT)
    pf = normal.paragraph_format
    pf.line_spacing = SPACING
    pf.space_before = Pt(0)
    pf.space_after = Pt(6)


def add_runs(par, text, bold=False):
    """Add text, supporting **bold** inside the line."""
    for i, part in enumerate(re.split(r"\*\*(.+?)\*\*", text)):
        if part:
            set_font(par.add_run(part), bold=bold or i % 2 == 1)


def add_page_number(doc):
    par = doc.sections[0].footer.paragraphs[0]
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = par.add_run()
    set_font(run)
    for kind, text in (("begin", None), (None, "PAGE"), ("end", None)):
        if kind:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), kind)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = text
        run._r.append(el)


def make_table(doc, rows, header=True, bold_first_col=False):
    table = doc.add_table(rows=len(rows), cols=len(rows[0]))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r, row in enumerate(rows):
        for c, text in enumerate(row):
            cell = table.cell(r, c)
            par = cell.paragraphs[0]
            par.paragraph_format.space_after = Pt(2)
            par.paragraph_format.space_before = Pt(2)
            add_runs(par, text, bold=(header and r == 0) or (bold_first_col and c == 0))
            if header and r == 0:
                shade = OxmlElement("w:shd")
                shade.set(qn("w:val"), "clear")
                shade.set(qn("w:fill"), "D9D9D9")
                cell._tc.get_or_add_tcPr().append(shade)
    if header:  # repeat header row on every page
        trPr = table.rows[0]._tr.get_or_add_trPr()
        el = OxmlElement("w:tblHeader")
        el.set(qn("w:val"), "true")
        trPr.append(el)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return table


def parse_front_matter(lines):
    meta = {}
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return meta, lines[i + 1:]
            if ":" in lines[i]:
                k, v = lines[i].split(":", 1)
                meta[k.strip().lower()] = v.strip()
    return {}, lines


def parse_table_block(block):
    rows = []
    for line in block:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
            continue
        rows.append(cells)
    width = max(len(r) for r in rows)
    return [r + [""] * (width - len(r)) for r in rows]


def build(src, dst):
    with open(src, encoding="utf-8") as f:
        meta, body = parse_front_matter(f.read().splitlines())
    base_dir = os.path.dirname(os.path.abspath(src))

    doc = Document()
    style_document(doc)
    add_page_number(doc)

    # Title block
    for text, size, space in ((meta.get("project", ""), Pt(14), 0),
                              (meta.get("title", "Document"), Pt(20), 6)):
        if text:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(space)
            set_font(p.add_run(text), bold=True, size=size)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)

    # Document info table
    info = [["Version", meta.get("version", "1.0")],
            ["Date", meta.get("date", "")],
            ["Prepared by", meta.get("author", "")]]
    if meta.get("status"):
        info.append(["Status", meta["status"]])
    make_table(doc, info, header=False, bold_first_col=True)

    # Body
    counters = [0, 0, 0]
    para_buf = []
    list_no = 0  # running number for the current numbered list

    def flush():
        if para_buf:
            p = doc.add_paragraph()
            p.paragraph_format.first_line_indent = Inches(0.5)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            add_runs(p, " ".join(para_buf))
            para_buf.clear()

    i = 0
    while i < len(body):
        line = body[i].rstrip()
        stripped = line.strip()
        is_numbered = bool(re.match(r"^\s*\d+[.)]\s+", line))
        if not is_numbered:
            list_no = 0

        if not stripped:
            flush()
        elif stripped == "<pagebreak>":
            flush()
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        elif re.match(r"^!\[.*\]\(.+\)$", stripped):
            flush()
            alt, path = re.match(r"^!\[(.*)\]\((.+)\)$", stripped).groups()
            if not os.path.isabs(path):
                path = os.path.join(base_dir, path)
            if os.path.exists(path):
                pic_par = doc.add_paragraph()
                pic_par.alignment = WD_ALIGN_PARAGRAPH.CENTER
                pic_par.paragraph_format.keep_with_next = True
                pic_par.add_run().add_picture(path, width=Inches(6.5))
                if alt:
                    cap = doc.add_paragraph()
                    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    set_font(cap.add_run(alt), italic=True)
            else:
                print(f"WARNING: image not found: {path}", file=sys.stderr)
        elif stripped.startswith("|"):
            flush()
            block = []
            while i < len(body) and body[i].strip().startswith("|"):
                block.append(body[i])
                i += 1
            make_table(doc, parse_table_block(block))
            continue
        elif re.match(r"^#{1,3}\s", stripped):
            flush()
            level = len(stripped.split()[0])
            title = stripped[level:].strip()
            counters[level - 1] += 1
            for j in range(level, 3):
                counters[j] = 0
            number = ".".join(str(n) for n in counters[:level])
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(12 if level == 1 else 8)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.keep_with_next = True
            set_font(p.add_run(f"{number}  {title}"), bold=True)
        elif re.match(r"^\s*[-*]\s+", line):
            flush()
            indent = (len(line) - len(line.lstrip())) // 2
            p = doc.add_paragraph(style="List Bullet")
            p.paragraph_format.left_indent = Inches(0.5 + 0.25 * indent)
            p.paragraph_format.first_line_indent = Inches(-0.25)
            p.paragraph_format.space_after = Pt(2)
            add_runs(p, re.sub(r"^\s*[-*]\s+", "", line))
        elif is_numbered:
            flush()
            list_no += 1
            p = doc.add_paragraph()  # typed numbers, so every list restarts at 1
            p.paragraph_format.left_indent = Inches(0.5)
            p.paragraph_format.first_line_indent = Inches(-0.25)
            p.paragraph_format.tab_stops.add_tab_stop(Inches(0.5))
            p.paragraph_format.space_after = Pt(2)
            add_runs(p, f"{list_no}.\t" + re.sub(r"^\s*\d+[.)]\s+", "", line))
        else:
            para_buf.append(stripped)
        i += 1
    flush()

    doc.core_properties.title = meta.get("title", "")
    doc.core_properties.author = meta.get("author", "")
    doc.save(dst)
    print(f"Built {dst}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: python build_doc.py input.md output.docx")
    build(sys.argv[1], sys.argv[2])
