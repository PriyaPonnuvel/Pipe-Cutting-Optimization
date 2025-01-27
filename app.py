import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from flask import Flask, request, render_template
from modules.data_acquisition import upload_and_validate_file
from modules.optimization_engine import best_fit_decreasing
from modules.results_display import visualize_cutting, cutting_efficiency, cut_distribution_histogram
from modules.feedback_module import generate_feedback

app = Flask(__name__)

AVAILABLE_PIPE_LENGTH = 6000
CUTTING_LOSS = 3

# Global variable for size-to-color mapping
size_to_color = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    name = request.form['name']  # Get name from the form
    address = request.form['address']  # Get address from the form
    try:
        # Step 1: Upload and validate file
        sizes_quantities = upload_and_validate_file(file)
        
        # Step 2: Run the optimization (this should return the pipes and quantity of pipes used)
        pipes, cutting_plan, total_pipes_used, total_remaining_length = best_fit_decreasing(AVAILABLE_PIPE_LENGTH, sizes_quantities, CUTTING_LOSS)
        
        
        # Step 3: Visualize cutting and get the size-to-color mapping
        img_path, total_used_length, total_waste, pie_chart_path = visualize_cutting(pipes, AVAILABLE_PIPE_LENGTH, CUTTING_LOSS, sizes_quantities)
        
        # Step 4: Generate the histogram based on the size-to-color mapping
        cut_dist_img = cut_distribution_histogram(sizes_quantities)
        
        # Step 5: Calculate efficiency
        total_length = AVAILABLE_PIPE_LENGTH * total_pipes_used
        efficiency = cutting_efficiency(total_used_length, total_waste, total_length)

        # Step 6: Generate feedback based on efficiency
        feedback = generate_feedback(efficiency)

        return render_template('results.html', 
                               img_path=img_path, 
                               efficiency=efficiency, 
                               feedback=feedback, 
                               cut_dist_img=cut_dist_img,
                               pie_chart_path=pie_chart_path, cutting_plan=cutting_plan,
                               total_remaining_length=total_remaining_length,
                               name= name,
                               address=address,
                               total_pipes_used = total_pipes_used)
    except Exception as e:
        return render_template('error.html', message=str(e))
    
import csv
from io import StringIO
from flask import Response

@app.route('/export/csv')
def export_csv():
    # Sample cutting plan data (replace this with your actual data)
    cutting_plan = [
        {"stock_pipe": "Pipe 1", "used_lengths": [500, 2000], "remaining_length": 2500},
        {"stock_pipe": "Pipe 2", "used_lengths": [1500, 1000], "remaining_length": 3500}
    ]

    # Create a CSV in memory
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Stock Pipe', 'Used Lengths', 'Remaining Length'])

    # Write rows
    for plan in cutting_plan:
        used_lengths_str = ', '.join(map(str, plan['used_lengths']))  # Join lengths with commas
        writer.writerow([plan['stock_pipe'], used_lengths_str, plan['remaining_length']])

    # Set the file pointer to the beginning of the StringIO object
    output.seek(0)

    # Create a response and return the CSV file
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=cutting_plan.csv"}
    )

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask import send_file
import io

@app.route('/export/pdf')
def export_pdf():
    # Sample cutting plan data (replace this with your actual data)
    cutting_plan = [
        {"stock_pipe": "Pipe 1", "used_lengths": [500, 2000], "remaining_length": 2500},
        {"stock_pipe": "Pipe 2", "used_lengths": [1500, 1000], "remaining_length": 3500}
    ]

    # Create a PDF in memory
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter  # Define the PDF size

    # Set title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 40, "Cutting Plan Summary")

    # Set table header
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 80, "Stock Pipe")
    c.drawString(200, height - 80, "Used Lengths")
    c.drawString(400, height - 80, "Remaining Length")

    # Set table content
    y_position = height - 100
    c.setFont("Helvetica", 12)
    for plan in cutting_plan:
        c.drawString(50, y_position, plan['stock_pipe'])
        c.drawString(200, y_position, ', '.join(map(str, plan['used_lengths'])))
        c.drawString(400, y_position, str(plan['remaining_length']))
        y_position -= 20

    # Save the PDF
    c.save()

    # Move to the beginning of the BytesIO buffer
    pdf_buffer.seek(0)

    # Send the PDF file as response
    return send_file(pdf_buffer, as_attachment=True, download_name="cutting_plan.pdf", mimetype="application/pdf")


if __name__ == '__main__':
    app.run(debug=True)
