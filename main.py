import json
from itertools import groupby

import argparse
import pdfkit
from pyluach import dates
from datetime import datetime
import locale


class myDateStr:
    def __init__(self, day: str, month: str, year: str):
        self.day = day
        self.month = month
        self.year = year

    def __str__(self):
        return f'{self.day} {self.month} {self.year}'


class HebrewAndGregorianDate:
    def __init__(self, hebrew: myDateStr, gregorian: myDateStr):
        self.hebrew = hebrew
        self.gregorian = gregorian

    def dict(self):
        return {"{{DateHebrewYear}}": self.hebrew.year, "{{DateHebrewDay}}": self.hebrew.day,
                "{{DateHebrewMonth}}": self.hebrew.month,
                "{{DateGregorianYear}}": self.gregorian.year, "{{DateGregorianDay}}": self.gregorian.day,
                "{{DateGregorianMonth}}": self.gregorian.month}


def getGregorianAndJewishDateInHebrew():
    # Set locale to Hebrew to display the month name in Hebrew
    gregorian_to_hebrew_months = {"January": "ינואר", "February": "פברואר", "March": "מרץ", "April": "אפריל",
                                  "May": "מאי", "June": "יוני", "July": "יולי", "August": "אוגוסט",
                                  "September": "ספטמבר", "October": "אוקטובר", "November": "נובמבר",
                                  "December": "דצמבר"}
    # Get the current Gregorian date
    gregorian_date = datetime.now()
    hebrew_date = dates.HebrewDate.today()
    # Get the current Hebrew date
    hebr = myDateStr(month=hebrew_date.month_name(True), day=hebrew_date.hebrew_day(True),
                     year=hebrew_date.hebrew_year(True, True))
    # Format the Gregorian date in Hebrew (year, month name, day)
    greg = myDateStr(gregorian_date.strftime('%Y'), gregorian_to_hebrew_months[gregorian_date.strftime('%B')],
                     gregorian_date.strftime('%d'))

    result = HebrewAndGregorianDate(hebrew=hebr, gregorian=greg)
    # Print the dates
    return result


def replace_placeholders_with_parameters(jsonParameters, html):
    updated_html = html
    # Replace placeholders with values from the JSON
    for key, value in jsonParameters.items():
        # Assuming the placeholder is in the format {{placeholder_name}}
        updated_html = updated_html.replace(f'{{{{{key}}}}}', value)

    # replace date placeholders with the current date
    date = getGregorianAndJewishDateInHebrew()
    for key, value in date.dict().items():
        updated_html = updated_html.replace(f'{key}', value)

    return updated_html


def generate_HTML_and_PDF_output(html, outputPath, outputName):
    html_out = f'{outputPath}/{outputName}.html'
    pdf_out = f'{outputPath}/{outputName}.pdf'
    # Save the modified HTML to a new file
    with open(html_out, 'w',encoding="utf-8") as f:
        f.write(str(html))

    print(f"Processed HTML saved to {html_out}")

    options = {
        'encoding':"UTF-8",
        'enable-local-file-access': True  # Needed to load local CSS/JS files in some environments
    }
    config = pdfkit.configuration(wkhtmltopdf="wkhtmltopdf\\bin\wkhtmltopdf.exe")
    # Generate PDF from the modified HTML
    pdfkit.from_file(html_out, pdf_out, configuration=config, options=options)
    print(f"PDF generated and saved to {pdf_out}")


if __name__ == "__main__":
    getGregorianAndJewishDateInHebrew()
    # Parse command-line arguments
    json_file = "input/parameters.json"
    html_file = "template/template.html"
    outputPath = "output"
    outputName = "report"
    # Load JSON data
    with open(json_file, 'r') as f:
        jsonParameters = json.load(f)

    # Load and parse the HTML
    with open(html_file, 'r') as f:
        html = f.read()

    updatedHTML = replace_placeholders_with_parameters(jsonParameters, html)
    generate_HTML_and_PDF_output(updatedHTML, outputPath, outputName)
