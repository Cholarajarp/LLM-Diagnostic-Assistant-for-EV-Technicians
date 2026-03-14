from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_manual(filename, title, content_lines):
    os.makedirs('data', exist_ok=True)
    filepath = os.path.join('data', filename)
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 72, title)

    # Content
    c.setFont("Helvetica", 12)
    y = height - 100
    for line in content_lines:
        c.drawString(72, y, line)
        y -= 20
        if y < 72:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = height - 72

    c.save()
    print(f"Created {filepath}")

if __name__ == "__main__":
    tesla_content = [
        "Tesla Model 3 Diagnostic Manual",
        "Error Code: BMS_a066 - High Voltage Battery Temperature High",
        "Description: The battery management system has detected a high temperature.",
        "Diagnostic Steps:",
        "1. Check the coolant level in the battery thermal management system.",
        "2. Inspect the radiator fan for proper operation.",
        "3. Verify the temperature sensors on the battery module using Toolbox.",
        "4. If coolant is low, check for leaks in the undercarriage.",
        "Resolution: Refill coolant if low. Replace faulty sensors or radiator fan as needed."
    ]
    create_manual("tesla_model_3_battery.pdf", "Tesla Model 3 High Voltage Battery Error Codes", tesla_content)

    nissan_content = [
        "Nissan Leaf Service Manual",
        "Component: Inverter",
        "Issue: Motor won't start, Inverter Failure Warning Light On.",
        "Diagnostic Steps:",
        "1. Disconnect the 12V battery and wait 10 minutes.",
        "2. Remove the high voltage service plug.",
        "3. Check the high voltage connections at the inverter for corrosion or looseness.",
        "4. Measure the resistance across the inverter power phases.",
        "Resolution: If resistance is out of spec, the inverter assembly must be replaced."
    ]
    create_manual("nissan_leaf_inverter.pdf", "Nissan Leaf Inverter Replacement Steps", nissan_content)

    chevy_content = [
        "Chevrolet Bolt EV Repair Guide",
        "Error Code: P0A80 - Replace Hybrid Battery Pack",
        "Description: Cell voltage variation is too high.",
        "Diagnostic Steps:",
        "1. Connect the GDS2 diagnostic tool and read the cell voltage data.",
        "2. Identify the specific cell group with low voltage.",
        "3. Perform a battery capacity test.",
        "Resolution: Replace the affected battery module. Do not replace individual cells."
    ]
    create_manual("chevy_bolt_battery.pdf", "Chevrolet Bolt EV Battery Diagnosis", chevy_content)

    print("Mock EV repair manuals generated successfully.")
