import json
from bs4 import BeautifulSoup
import argparse
import pdfkit


def replace_placeholders_with_parameters(jsonParameters, htmlSoup):
    # Replace placeholders with values from the JSON
    for key, value in jsonParameters.items():
        # Assuming the placeholder is in the format {{placeholder_name}}
        placeholder = htmlSoup.find_all(string=f'{{{{{key}}}}}')
        for element in placeholder:
            element.replace_with(value)
    return htmlSoup


def generate_HTML_and_PDF_output(htmlSoup, outputPath, outputName):
    html_out = f'{outputPath}/{outputName}.html'
    pdf_out = f'{outputPath}/{outputName}.pdf'
    # Save the modified HTML to a new file
    with open(html_out, 'w') as f:
        f.write(str(htmlSoup))

    print(f"Processed HTML saved to {html_out}")

    options = {
        'enable-local-file-access': True  # Needed to load local CSS/JS files in some environments
    }
    config = pdfkit.configuration(wkhtmltopdf="wkhtmltopdf\\bin\wkhtmltopdf.exe")
    # Generate PDF from the modified HTML
    pdfkit.from_file(html_out, pdf_out, configuration=config,options=options)
    print(f"PDF generated and saved to {pdf_out}")


if __name__ == "__main__":
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
        htmlSoup = BeautifulSoup(f, 'html.parser')

    updatedHTML = replace_placeholders_with_parameters(jsonParameters, htmlSoup)
    generate_HTML_and_PDF_output(updatedHTML, outputPath, outputName)
