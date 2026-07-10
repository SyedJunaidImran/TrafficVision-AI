"""
TrafficVision AI
Report Generator Module

Generates PDF reports for traffic analysis.
"""

from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


class ReportGenerator:
    """
    Generates a PDF report containing
    traffic analysis statistics.
    """

    def __init__(
        self,
        output_path="data/reports/traffic_report.pdf"
    ):

        self.output_path = output_path

        self.styles = getSampleStyleSheet()

    def generate_report(
        self,
        vehicle_counts,
        density_stats,
    ):
        """
        Generate PDF traffic report.

        Parameters
        ----------
        vehicle_counts : dict
            Dictionary returned by counter.py

        density_stats : dict
            Dictionary returned by density.py
        """
        Path(self.output_path).parent.mkdir(
        parents=True,
        exist_ok=True
        )      
        document = SimpleDocTemplate(self.output_path)

        elements = []

        # -------------------------
        # Title
        # -------------------------

        title = Paragraph(
            "<b><font size='18'>TrafficVision AI Report</font></b>",
            self.styles["Title"],
        )

        elements.append(title)

        elements.append(Spacer(1, 20))

        # -------------------------
        # Date
        # -------------------------

        generated_time = Paragraph(
            f"Generated on: "
            f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
            self.styles["Normal"],
        )

        elements.append(generated_time)

        elements.append(Spacer(1, 20))

        # -------------------------
        # Statistics Table
        # -------------------------

        table_data = [

            ["Metric", "Value"],

            ["Total Vehicles", vehicle_counts["Total"]],

            ["Cars", vehicle_counts["Car"]],

            ["Motorcycles", vehicle_counts["Motorcycle"]],

            ["Buses", vehicle_counts["Bus"]],

            ["Trucks", vehicle_counts["Truck"]],

            ["Current Density", density_stats["current_density"]],

            ["Peak Density", density_stats["peak_density"]],

            ["Congestion Level", density_stats["congestion_level"]],
        ]

        table = Table(table_data)

        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                ]
            )
        )

        elements.append(table)

        elements.append(Spacer(1, 20))

        # -------------------------
        # Summary
        # -------------------------

        summary = Paragraph(
            """
            <b>Traffic Summary</b><br/><br/>

            This report was generated automatically by
            <b>TrafficVision AI</b> using YOLOv8 and ByteTrack.

            The report summarizes the detected vehicle counts,
            traffic density, and congestion level observed
            during video processing.

            Thank you for using TrafficVision AI.
            """,
            self.styles["BodyText"],
        )

        elements.append(summary)

        # -------------------------
        # Build PDF
        # -------------------------

        document.build(elements)

        return self.output_path


if __name__ == "__main__":

    vehicle_counts = {
        "Total": 124,
        "Car": 78,
        "Motorcycle": 26,
        "Bus": 12,
        "Truck": 8,
    }

    density_stats = {
        "current_density": 15,
        "peak_density": 24,
        "congestion_level": "HIGH",
    }

    report = ReportGenerator()

    pdf_path = report.generate_report(
        vehicle_counts,
        density_stats,
    )

    print(f"Report generated successfully: {pdf_path}")