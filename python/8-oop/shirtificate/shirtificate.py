from fpdf import FPDF


def main():
    create_pdf(input("Name: "))


def create_pdf(name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 24)
    pdf.cell(w=0, h=30, txt="CS50 Shirtificate", align="C")
    pdf.ln(h=40)
    pdf.image("shirtificate.png", w=pdf.epw)
    pdf.set_text_color(255)
    pdf.cell(w=0, h=-230, txt=f"{name} took CS50", align='C')
    pdf.output("shirtificate.pdf")


if __name__ == "__main__":
    main()