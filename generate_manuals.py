from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_manual(filename, title, pages):
    os.makedirs('data', exist_ok=True)
    filepath = os.path.join('data', filename)
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    for page_num, content_lines in enumerate(pages):
        # Header / Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(72, height - 72, f"{title} - Page {page_num + 1}")

        # Content
        c.setFont("Helvetica", 11)
        y = height - 110
        for line in content_lines:
            c.drawString(72, y, line)
            y -= 18
            if y < 72:
                c.showPage()
                c.setFont("Helvetica", 11)
                y = height - 72

        # Footer
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(width - 150, 40, f"Confidential Repair Manual | Page {page_num + 1}")
        c.showPage() # End page

    c.save()
    print(f"Created {filepath} with {len(pages)} pages.")

if __name__ == "__main__":
    tesla_pages = [
        [
            "Tesla Model 3 High Voltage Architecture Overview",
            "================================================",
            "The High Voltage (HV) system operates at ~400V DC.",
            "Components include the HV Battery Pack, Drive Inverter, and PTC Heater.",
            "Safety Protocol: ALWAYS use Class 0 linesman gloves rated for 1000V.",
            "Before any service, disable the HV system by disconnecting the First Responder Loop."
        ],
        [
            "Error Code: BMS_a066 - High Voltage Battery Temperature High",
            "============================================================",
            "Description: The battery management system (BMS) has detected an abnormally high temperature.",
            "Diagnostic Steps:",
            "1. Access the Service Mode menu on the MCU.",
            "2. Navigate to 'Thermal' and check the coolant level in the battery thermal management system.",
            "3. Inspect the active louver aero shield for debris.",
            "4. Verify the operation of the radiator fan assembly.",
            "5. If coolant is low, check for leaks in the undercarriage near the battery manifold.",
            "Resolution: Refill coolant if low. Bleed the cooling system using the 'Coolant Purge' routine."
        ],
        [
            "Error Code: DI_a021 - Drive Inverter Communication Failure",
            "==========================================================",
            "Description: The vehicle logic board has lost CAN communication with the Drive Inverter.",
            "Diagnostic Steps:",
            "1. Remove the rear subframe aero shield.",
            "2. Inspect the low voltage logic connector (X042) on the inverter for water ingress.",
            "3. Measure resistance between CAN High and CAN Low on the diagnostic port (should be ~60 ohms).",
            "Resolution: If resistance is 120 ohms, check the terminating resistor in the drive unit."
        ]
    ]
    create_manual("tesla_model_3_deep_manual.pdf", "Tesla Model 3 Comprehensive Repair Guide", tesla_pages)

    nissan_pages = [
        [
            "Nissan Leaf ZE1 Series Technical Manual",
            "=======================================",
            "Platform: ZE1. Battery Capacity: 40kWh or 62kWh.",
            "The Power Delivery Module (PDM) integrates the onboard charger and DC/DC converter."
        ],
        [
            "Component: Power Delivery Module (PDM) & Inverter",
            "Issue: Motor won't start, Inverter Failure Warning Light On.",
            "Diagnostic Steps:",
            "1. Ensure the vehicle is turned OFF. Disconnect the 12V battery and wait 10 minutes.",
            "2. Wear high voltage PPE. Remove the high voltage service plug located behind the rear seats.",
            "3. Check the high voltage DC cables at the inverter for corrosion or looseness.",
            "4. Measure the resistance across the inverter power phases (U, V, W).",
            "   - Set multimeter to ohms. Probe U-V, V-W, and U-W.",
            "   - Expected resistance check: 0.1 to 0.5 ohms. If open circuit (OL), IGBT is blown.",
            "Resolution: If resistance is out of spec, the inverter assembly must be replaced."
        ]
    ]
    create_manual("nissan_leaf_deep_manual.pdf", "Nissan Leaf Inverter Replacement Steps", nissan_pages)

    chevy_pages = [
        [
            "Chevrolet Bolt EV Repair Guide",
            "Error Code: P0A80 - Replace Hybrid Battery Pack",
            "Description: Cell voltage variation is too high.",
            "Diagnostic Steps:",
            "1. Connect the GDS2 diagnostic tool to the OBD-II port.",
            "2. Read the Hybrid/EV Powertrain Control Module 2 data.",
            "3. View 'Hybrid/EV Battery Cell Voltage 1-96'.",
            "4. Identify the specific cell group with low voltage (variation > 0.05V is abnormal).",
            "5. Perform a battery capacity test using the EL-50332 Battery Depot Tester.",
            "Resolution: Replace the affected battery module. Do not attempt to replace individual pouch cells."
        ]
    ]
    create_manual("chevy_bolt_deep_manual.pdf", "Chevrolet Bolt EV Battery Diagnosis", chevy_pages)

    print("Mock deep EV repair manuals generated successfully.")
