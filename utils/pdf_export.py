"""PDF report generator for CaloriQ using fpdf2."""

from datetime import datetime


def generate_pdf(predictions: list, stats: dict = None) -> bytes:
    """Generate a PDF report from predictions data.

    Args:
        predictions: list of prediction dicts
        stats: optional dict with total_count, total_cal, avg_cal, max_cal, min_cal

    Returns:
        PDF file content as bytes.
    """
    try:
        from fpdf import FPDF
    except ImportError:
        return None

    class CaloriQPDF(FPDF):
        def header(self):
            self.set_font('Helvetica', 'B', 16)
            self.set_text_color(0, 153, 125)
            self.cell(0, 10, 'CaloriQ - Laporan Aktivitas', new_x="LMARGIN", new_y="NEXT", align='C')
            self.set_font('Helvetica', '', 9)
            self.set_text_color(128, 128, 128)
            self.cell(0, 6, f'Dibuat: {datetime.now().strftime("%d-%m-%Y %H:%M")}',
                      new_x="LMARGIN", new_y="NEXT", align='C')
            self.ln(4)
            self.set_draw_color(0, 153, 125)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(6)

        def footer(self):
            self.set_y(-15)
            self.set_font('Helvetica', 'I', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f'CaloriQ - Halaman {self.page_no()}/{{nb}}', align='C')

    pdf = CaloriQPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ── Summary statistics ──
    if stats:
        pdf.set_font('Helvetica', 'B', 13)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 10, 'Ringkasan Statistik', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        pdf.set_font('Helvetica', '', 10)

        items = [
            ('Total Prediksi',   str(stats.get('total_count', 0))),
            ('Total Kalori',     f"{stats.get('total_cal', 0):.1f} kcal"),
            ('Rata-rata / Sesi', f"{stats.get('avg_cal', 0):.1f} kcal"),
            ('Kalori Tertinggi', f"{stats.get('max_cal', 0):.1f} kcal"),
            ('Kalori Terendah',  f"{stats.get('min_cal', 0):.1f} kcal"),
        ]
        for label, value in items:
            pdf.set_text_color(80, 80, 80)
            pdf.cell(55, 7, label)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(0, 7, value, new_x="LMARGIN", new_y="NEXT")
            pdf.set_font('Helvetica', '', 10)
        pdf.ln(6)

    # ── Data table ──
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 10, 'Detail Riwayat Prediksi', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    headers = ['Waktu', 'Gender', 'Usia', 'Durasi', 'HR', 'Kalori', 'Intensitas']
    widths  = [38, 18, 14, 20, 14, 22, 24]

    # Header row
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_fill_color(0, 153, 125)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(headers):
        pdf.cell(widths[i], 8, h, border=1, fill=True, align='C')
    pdf.ln()

    # Data rows
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(0, 0, 0)
    for idx, row in enumerate(predictions):
        if not isinstance(row, dict):
            continue
        fill = idx % 2 == 0
        if fill:
            pdf.set_fill_color(240, 248, 245)

        ts = str(row.get('timestamp', ''))[:16]
        values = [
            ts,
            str(row.get('gender', '')),
            str(row.get('age', '')),
            f"{row.get('duration', '')} min",
            str(row.get('heart_rate', '')),
            f"{row.get('calories', 0):.1f}",
            str(row.get('intensity', '')),
        ]
        for i, v in enumerate(values):
            pdf.cell(widths[i], 7, v, border=1, fill=fill, align='C')
        pdf.ln()

    return pdf.output()
