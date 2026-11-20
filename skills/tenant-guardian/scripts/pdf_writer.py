"""Dependency-free PDF writer: Helvetica text, filled shapes, lines and links. No network I/O.

Kept in-house so the skill stays offline and stdlib-only; producing a PDF never needs a pip install.
Text is limited to Windows-1252 (PDF WinAnsiEncoding); other characters render as '?'.
Coordinates are points measured from the top-left corner, which suits top-down report layout.
"""
import zlib

PAGE_W, PAGE_H = 612.0, 792.0  # US Letter

# Advance widths (1/1000 em) for codes 32..126, from the Adobe Core 14 AFM metrics.
_REGULAR = (
    278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278,
    556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 278, 278, 584, 584, 584, 556,
    1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778,
    667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556,
    333, 556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556,
    556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500, 334, 260, 334, 584,
)
_BOLD = (
    278, 333, 474, 556, 556, 889, 722, 238, 333, 333, 389, 584, 278, 333, 278, 278,
    556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 333, 333, 584, 584, 584, 611,
    975, 722, 722, 722, 722, 667, 611, 778, 722, 278, 556, 722, 611, 833, 722, 778,
    667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 333, 278, 333, 584, 556,
    333, 556, 611, 556, 611, 556, 333, 611, 611, 278, 278, 556, 278, 889, 611, 611,
    611, 611, 389, 556, 333, 611, 556, 778, 556, 556, 500, 389, 280, 389, 584,
)
# Windows-1252 punctuation the reports use: quotes, bullet, dashes, ellipsis, section, middle dot.
_EXTRA = {
    0x85: (1000, 1000), 0x91: (222, 278), 0x92: (222, 278), 0x93: (333, 500), 0x94: (333, 500),
    0x95: (350, 350), 0x96: (556, 556), 0x97: (1000, 1000), 0xA0: (278, 278), 0xA7: (556, 556),
    0xA9: (737, 737), 0xB0: (400, 400), 0xB7: (278, 278),
}
_KAPPA = 0.5523  # Bezier control-point ratio for quarter circles


def encode(text):
    """Map text to WinAnsi bytes; unsupported characters become '?' and control characters spaces."""
    clean = ''.join(' ' if ord(ch) < 32 or ord(ch) == 127 else ch for ch in str(text))
    return clean.encode('cp1252', errors='replace')


def text_width(text, size, bold=False):
    table = _BOLD if bold else _REGULAR
    total = 0
    for byte in encode(text):
        if 32 <= byte <= 126:
            total += table[byte - 32]
        else:
            total += _EXTRA.get(byte, (556, 556))[1 if bold else 0]
    return total * size / 1000.0


def wrap(text, size, width, bold=False):
    """Greedy word wrap; words longer than the line (URLs, hashes) are split by character."""
    lines = []
    for paragraph in str(text).split('\n'):
        line = ''
        for word in paragraph.split():
            candidate = f'{line} {word}' if line else word
            if text_width(candidate, size, bold) <= width:
                line = candidate
                continue
            if line:
                lines.append(line)
            while word and text_width(word, size, bold) > width:
                # Take at least one character per line so tiny or negative widths still terminate.
                cut, used = 0, 0.0
                for ch in word:
                    step = text_width(ch, size, bold)
                    if cut and used + step > width:
                        break
                    used += step
                    cut += 1
                lines.append(word[:cut])
                word = word[cut:]
            line = word
        lines.append(line)
    return lines


def _num(value):
    return ('%.2f' % value).rstrip('0').rstrip('.') or '0'


def _rgb(color):
    if isinstance(color, str):
        value = color.lstrip('#')
        return tuple(int(value[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    return color


def _color_op(color, op):
    return ' '.join(_num(c) for c in _rgb(color)) + ' ' + op


def _literal(data):
    out = []
    for byte in data:
        if byte in (0x28, 0x29, 0x5C):
            out.append('\\' + chr(byte))
        elif 32 <= byte < 127:
            out.append(chr(byte))
        else:
            out.append('\\%03o' % byte)
    return '(' + ''.join(out) + ')'


def _pdf_string(text):
    return _literal(encode(text))


def _info_string(text):
    # The Info dictionary uses PDFDocEncoding, not WinAnsi; UTF-16BE with a BOM is the portable form.
    text = str(text)
    if all(32 <= ord(ch) < 127 for ch in text):
        return _literal(text.encode('ascii'))
    return '<FEFF' + text.encode('utf-16-be', 'replace').hex().upper() + '>'


class PDF:
    def __init__(self, title='', author='', subject=''):
        self.meta = {'Title': title, 'Author': author, 'Subject': subject, 'Producer': 'Tenant Guardian pdf_writer'}
        self.pages = []

    def add_page(self):
        self.pages.append({'ops': [], 'links': []})
        return len(self.pages) - 1

    def _ops(self, page):
        return self.pages[page]['ops']

    def text(self, x, top, value, size=10, bold=False, color='#000000', page=-1):
        """One line of text whose baseline sits `top` points below the top edge."""
        font = 'F2' if bold else 'F1'
        self._ops(page).append(
            f'BT /{font} {_num(size)} Tf {_color_op(color, "rg")} {_num(x)} {_num(PAGE_H - top)} Td {_pdf_string(value)} Tj ET'
        )

    def rect(self, x, top, w, h, fill=None, stroke=None, line_width=0.75, radius=0, page=-1):
        if w <= 0 or h <= 0 or (fill is None and stroke is None):
            return
        ops = ['q']
        if fill is not None:
            ops.append(_color_op(fill, 'rg'))
        if stroke is not None:
            ops.append(_color_op(stroke, 'RG') + f' {_num(line_width)} w')
        y = PAGE_H - top - h
        r = min(radius, w / 2, h / 2)
        if r <= 0:
            ops.append(f'{_num(x)} {_num(y)} {_num(w)} {_num(h)} re')
        else:
            k = _KAPPA * r
            x2, y2 = x + w, y + h
            ops.append(' '.join([
                f'{_num(x + r)} {_num(y)} m', f'{_num(x2 - r)} {_num(y)} l',
                f'{_num(x2 - r + k)} {_num(y)} {_num(x2)} {_num(y + r - k)} {_num(x2)} {_num(y + r)} c',
                f'{_num(x2)} {_num(y2 - r)} l',
                f'{_num(x2)} {_num(y2 - r + k)} {_num(x2 - r + k)} {_num(y2)} {_num(x2 - r)} {_num(y2)} c',
                f'{_num(x + r)} {_num(y2)} l',
                f'{_num(x + r - k)} {_num(y2)} {_num(x)} {_num(y2 - r + k)} {_num(x)} {_num(y2 - r)} c',
                f'{_num(x)} {_num(y + r)} l',
                f'{_num(x)} {_num(y + r - k)} {_num(x + r - k)} {_num(y)} {_num(x + r)} {_num(y)} c h',
            ]))
        ops.append('B' if fill is not None and stroke is not None else 'f' if fill is not None else 'S')
        ops.append('Q')
        self._ops(page).append(' '.join(ops))

    def line(self, x1, top1, x2, top2, color='#000000', width=0.75, page=-1):
        self._ops(page).append(
            f'q {_color_op(color, "RG")} {_num(width)} w {_num(x1)} {_num(PAGE_H - top1)} m '
            f'{_num(x2)} {_num(PAGE_H - top2)} l S Q'
        )

    def link(self, x, top, w, h, url, page=-1):
        if str(url).startswith(('https://', 'http://')):
            self.pages[page]['links'].append((x, PAGE_H - top - h, x + w, PAGE_H - top, str(url)))

    def output(self):
        meta = ' '.join(f'/{k} {_info_string(v)}' for k, v in self.meta.items() if v)
        objects = {
            1: b'<< /Type /Catalog /Pages 2 0 R >>',
            3: b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>',
            4: b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>',
            5: f'<< {meta} >>'.encode('latin-1'),
        }
        next_id, kids = 6, []
        for page in self.pages:
            stream = zlib.compress('\n'.join(page['ops']).encode('latin-1'))
            content_id, next_id = next_id, next_id + 1
            objects[content_id] = (
                f'<< /Length {len(stream)} /Filter /FlateDecode >>\nstream\n'.encode('latin-1') + stream + b'\nendstream'
            )
            annots = []
            for x1, y1, x2, y2, url in page['links']:
                objects[next_id] = (
                    f'<< /Type /Annot /Subtype /Link /Rect [{_num(x1)} {_num(y1)} {_num(x2)} {_num(y2)}] '
                    f'/Border [0 0 0] /A << /S /URI /URI {_literal(url.encode("latin-1", errors="replace"))} >> >>'
                ).encode('latin-1')
                annots.append(next_id)
                next_id += 1
            annot_ref = f' /Annots [{" ".join(f"{a} 0 R" for a in annots)}]' if annots else ''
            objects[next_id] = (
                f'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {_num(PAGE_W)} {_num(PAGE_H)}] '
                f'/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents {content_id} 0 R{annot_ref} >>'
            ).encode('latin-1')
            kids.append(next_id)
            next_id += 1
        objects[2] = f'<< /Type /Pages /Kids [{" ".join(f"{k} 0 R" for k in kids)}] /Count {len(kids)} >>'.encode('latin-1')

        out = bytearray(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n')
        offsets = {}
        for number in range(1, next_id):
            offsets[number] = len(out)
            out += f'{number} 0 obj\n'.encode('latin-1') + objects[number] + b'\nendobj\n'
        xref = len(out)
        out += f'xref\n0 {next_id}\n0000000000 65535 f \n'.encode('latin-1')
        for number in range(1, next_id):
            out += f'{offsets[number]:010d} 00000 n \n'.encode('latin-1')
        out += f'trailer\n<< /Size {next_id} /Root 1 0 R /Info 5 0 R >>\nstartxref\n{xref}\n%%EOF\n'.encode('latin-1')
        return bytes(out)
