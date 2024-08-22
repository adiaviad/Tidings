import json
import pdf
import argparse

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
        html = f.read()

    updatedHTML = pdf.replace_placeholders_with_parameters(jsonParameters, html)
    pdf.generate_HTML_and_PDF_output(updatedHTML, outputPath, outputName)
