import pdfkit
import hebrewdates
from itertools import groupby


def replace_placeholders_with_parameters(jsonParameters, html):
    updated_html = html
    # Replace placeholders with values from the JSON
    for key, value in jsonParameters.items():
        # Assuming the placeholder is in the format {{placeholder_name}}
        updated_html = updated_html.replace(f'{{{{{key}}}}}', value)

    # replace date placeholders with the current date
    date = hebrewdates.getGregorianAndJewishDateInHebrew()
    for key, value in date.dict().items():
        updated_html = updated_html.replace(f'{key}', value)

    return updated_html


def generate_HTML_and_PDF_output(html, outputPath, outputName):
    html_out = f'{outputPath}/{outputName}.html'
    pdf_out = f'{outputPath}/{outputName}.pdf'
    # Save the modified HTML to a new file
    with open(html_out, 'w', encoding="utf-8") as f:
        f.write(str(html))

    print(f"Processed HTML saved to {html_out}")

    options = {
        'encoding': "UTF-8",
        'enable-local-file-access': True  # Needed to load local CSS/JS files in some environments
    }
    config = pdfkit.configuration(wkhtmltopdf="wkhtmltopdf\\bin\wkhtmltopdf.exe")
    # Generate PDF from the modified HTML
    pdfkit.from_file(html_out, pdf_out, configuration=config, options=options)
    print(f"PDF generated and saved to {pdf_out}")
