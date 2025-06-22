import csv
import statistics
from fpdf import FPDF

# Grabbing that CSV !
with open("data.csv", "r", newline="") as file:
    data = list(csv.DictReader(file))  # getting data and converting it from CSV to a list of dictionaries

subjects = ["Phy", "Chem", "Maths"]


all_averages = []
for row in data:
    scores = [int(row[subj]) for subj in subjects]  
    avg = statistics.mean(scores)  
    row["Average"] = avg  
    all_averages.append(avg)  


data_analysis = {}
for subject in subjects:
    scores = [int(row[subject]) for row in data]
    data_analysis[subject] = {
        "average": statistics.mean(scores),  
        "max": max(scores),                 
        "min": min(scores),                  
        "top_student": max(data, key=lambda x: int(x[subject]))["Name"]  # Legend alert!
    }

# Creating pdf and making it look gud!
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=18)
pdf.add_page()

# Header – gotta flex a little
pdf.set_fill_color(44, 62, 80)  
pdf.rect(0, 0, 210, 24, 'F')
pdf.set_xy(0, 8)
pdf.set_text_color(255, 255, 255)
pdf.set_font("Helvetica", "B", 22)
pdf.cell(0, 10, "Student Marks Report", 0, 1, "C")
pdf.ln(12)  

# Dropping the summary 
pdf.set_font("Helvetica", "B", 16)
pdf.set_text_color(39, 174, 96)
pdf.cell(0, 10, "Summary", 0, 1, "L")
pdf.ln(2)
pdf.set_font("Helvetica", "", 12)
pdf.set_text_color(44, 62, 80)
pdf.cell(0, 8, f"Total Students: {len(data)}", 0, 1)  
pdf.cell(0, 8, f"Average Score: {statistics.mean(all_averages):.2f}", 0, 1)  
pdf.cell(0, 8, f"Highest Average: {max(all_averages):.2f}", 0, 1)  
pdf.cell(0, 8, f"Lowest Average: {min(all_averages):.2f}", 0, 1)   
pdf.ln(8)

# everyone's marks!
pdf.set_font("Helvetica", "B", 14)
pdf.set_text_color(41, 128, 185)
pdf.cell(0, 10, "Student Scores", 0, 1, "L")
pdf.ln(2)

student_headers = ["Name"] + subjects + ["Total", "Average"]
student_widths = [30, 25, 25, 25, 30, 30]

# Table header – gotta make it pop!
pdf.set_fill_color(39, 174, 96)
pdf.set_text_color(255, 255, 255)
pdf.set_font("Helvetica", "B", 12)
for i, header in enumerate(student_headers):
    pdf.cell(student_widths[i], 10, header, 1, 0, "C", fill=True)
pdf.ln()

# Table rows 
pdf.set_font("Helvetica", "", 11)
for idx, row in enumerate(data):
    fill = idx % 2 == 0  # Zebra stripes, because why not?
    if fill:
        pdf.set_fill_color(236, 240, 241)
    else:
        pdf.set_fill_color(255, 255, 255)
    pdf.set_text_color(44, 62, 80)
    total = sum(int(row[subj]) for subj in subjects)
    avg = total / len(subjects)
    row_data = [row["Name"]] + [row[subj] for subj in subjects] + [total, f"{avg:.2f}"]
    for i, item in enumerate(row_data):
        pdf.cell(student_widths[i], 10, str(item), 1, 0, "C", fill=fill)
    pdf.ln()

pdf.ln(8)

# Subject-wise stats
pdf.set_font("Helvetica", "B", 13)
pdf.set_text_color(39, 174, 96)
pdf.cell(0, 10, "Subject-wise Statistics", 0, 1, "L")
pdf.set_font("Helvetica", "", 11)
pdf.set_text_color(44, 62, 80)
for subject, stats in data_analysis.items():
    pdf.cell(0, 8,
        f"{subject}: Avg={stats['average']:.2f}, Max={stats['max']}, Min={stats['min']}, Topper={stats['top_student']}",
        0, 1)
pdf.ln(2)

# Saving the PDF
pdf.output("Report.pdf")