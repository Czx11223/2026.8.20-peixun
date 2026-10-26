"""面试报告 PDF 生成（ReportLab）。

中文字体：使用 ReportLab 内置 Adobe CID 字体 STSong-Light（宋体），
无需外部字体文件、离线可用；默认 Helvetica 不支持中文（导出后中文空白/黑块）。
"""
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

# 注册内置中文字体（Adobe CID：STSong-Light 宋体）
FONT_CN = "STSong-Light"
pdfmetrics.registerFont(UnicodeCIDFont(FONT_CN))


def generate_report_pdf(report: dict) -> bytes:
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=18 * mm, bottomMargin=18 * mm,
                            leftMargin=18 * mm, rightMargin=18 * mm, title="面知 面试报告")
    h1 = ParagraphStyle("h1", fontName=FONT_CN, fontSize=20, leading=28,
                        textColor=colors.HexColor("#1D1D1F"))
    h2 = ParagraphStyle("h2", fontName=FONT_CN, fontSize=14, leading=20,
                        textColor=colors.HexColor("#007AFF"), spaceBefore=8, spaceAfter=4)
    body = ParagraphStyle("body", fontName=FONT_CN, fontSize=10, leading=15,
                          textColor=colors.HexColor("#1D1D1F"))

    story = [
        Paragraph("面知 · AI 面试陪练报告", h1),
        Spacer(1, 6),
        Paragraph(f"岗位：{report['job_name']}　|　模式：{'压力面' if report['mode'] == 'pressure' else '普通面'}　|　日期：{report['date']}", body),
        Spacer(1, 10),
        Paragraph(f"综合得分：{report['total_score']} 分　等级：{report['grade']}", body),
        Spacer(1, 8),
        Paragraph("综合评价", h2),
        Paragraph(report["summary"], body),
        Spacer(1, 10),
        Paragraph("维度得分", h2),
    ]

    dim_rows = [["维度", "得分"]] + [[d["name"], str(d["score"])] for d in report["dimensions"]]
    dim_table = Table(dim_rows, colWidths=[120 * mm, 40 * mm])
    dim_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), FONT_CN),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6F1FB")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#007AFF")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E5EA")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F5F7")]),
    ]))
    story.append(dim_table)
    story.append(Spacer(1, 12))

    story.append(Paragraph("逐题复盘", h2))
    for i, a in enumerate(report["answers"], 1):
        story.append(Paragraph(f"Q{i}. {a['question']}（{a['score']} 分 / {a['grade']}）", body))
        story.append(Paragraph(f"你的回答：{a['answer']}", body))
        story.append(Paragraph(f"AI 点评：{a['comment']}", body))
        story.append(Paragraph(f"优化建议：{a['suggestion']}", body))
        story.append(Spacer(1, 6))

    doc.build(story)
    return buf.getvalue()
