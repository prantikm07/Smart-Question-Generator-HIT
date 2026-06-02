import os
import io
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv

from retriever import DocumentRetriever
from generator import PaperGenerator


current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '..', '.env')

load_dotenv(env_path)

app = Flask(__name__)
CORS(app)

retriever = DocumentRetriever(db_path="./vector_store")
generator = PaperGenerator()


@app.route('/api/connect', methods=['GET'])
def test_connection():
    return jsonify({"status": "healthy", "message": "Server is awake and ready!"}), 200

@app.route('/api/generate-paper', methods=['POST'])
def generate_paper():
    data = request.json
    subject = data.get('subject', 'Computer Science')
    mcq_count = int(data.get('mcq_count', 10))
    short_count = int(data.get('short_count', 3))
    long_count = int(data.get('long_count', 4))

    context = retriever.get_context(subject)
    if not context:
        return jsonify({"error": "No context found in the database."}), 404

    try:
        sections = generator.generate_sections(context, subject, mcq_count, short_count, long_count)
        return jsonify(sections)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate-pdf', methods=['POST'])
def generate_pdf():

    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.enums import TA_CENTER, TA_LEFT

    data = request.json
    subject   = data.get('subject', '')
    marks     = data.get('marks', 70)
    section_a = data.get('section_a', '')
    section_b = data.get('section_b', '')
    section_c = data.get('section_c', '')

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=20*mm, rightMargin=20*mm,
                            topMargin=20*mm, bottomMargin=20*mm)

    styles = getSampleStyleSheet()
    title_style   = ParagraphStyle('Title',   fontSize=14, alignment=TA_CENTER, fontName='Helvetica-Bold', spaceAfter=4)
    sub_style     = ParagraphStyle('Sub',     fontSize=12, alignment=TA_CENTER, fontName='Helvetica-Bold', spaceAfter=6)
    meta_style    = ParagraphStyle('Meta',    fontSize=11, fontName='Helvetica-Bold', spaceAfter=4)
    italic_style  = ParagraphStyle('Italic',  fontSize=10, alignment=TA_CENTER, fontName='Helvetica-Oblique', spaceAfter=12)
    section_style = ParagraphStyle('Section', fontSize=12, alignment=TA_CENTER, fontName='Helvetica-Bold', spaceAfter=8, spaceBefore=16, underline=1)
    q_style       = ParagraphStyle('Q',       fontSize=11, fontName='Helvetica-Bold', spaceAfter=2, spaceBefore=10)
    opt_style     = ParagraphStyle('Opt',     fontSize=11, leftIndent=16, spaceAfter=1)
    normal        = ParagraphStyle('Normal',  fontSize=11, spaceAfter=2)

    story = []
    story.append(Paragraph("HALDIA INSTITUTE OF TECHNOLOGY", title_style))
    story.append(Paragraph(subject.upper(), sub_style))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(f"Time Allotted: 3 Hours &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Full Marks: {marks}", meta_style))
    story.append(Paragraph("The figures in the margin indicate full marks.<br/>Candidates are required to give their answers in their own words as far as practicable.", italic_style))

    def render_section(title, text):
        story.append(Paragraph(title, section_style))
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                story.append(Spacer(1, 2*mm))
                continue
            # Question line
            if (line[:2].rstrip('.').isdigit() or line.upper().startswith('Q')):
                story.append(Paragraph(line, q_style))
            # Option line a) b) c) d)
            elif len(line) >= 2 and line[0].lower() in 'abcd' and line[1] in ')':
                story.append(Paragraph(line, opt_style))
            else:
                story.append(Paragraph(line, normal))

    render_section("GROUP - A<br/>(Multiple Choice Type Questions)", section_a)
    render_section("GROUP - B<br/>(Short Answer Type Questions)", section_b)
    render_section("GROUP - C<br/>(Long Answer Type Questions)", section_c)

    doc.build(story)
    buf.seek(0)
    filename = subject.replace(' ', '_') + '_Question_Paper.pdf'
    return send_file(buf, mimetype='application/pdf',
                     as_attachment=True, download_name=filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)