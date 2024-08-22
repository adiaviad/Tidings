import zipfile
import xml.etree.ElementTree as ET
import os
import shutil
import hebrewdates


# Function to replace placeholders in the XML content of the .docx file
def replace_placeholders_in_docx(_docx_path, _output_path, _replacements: dict):
    if "date" in _replacements.keys():
        _replacements["date"] = hebrewdates.getGregorianAndJewishDateInHebrew().hebrew.__str__()
    _replacements = dict(zip([f'<<{key}>>' for key in _replacements.keys()], _replacements.values()))

    # Create a temporary directory to extract the .docx contents
    temp_dir = 'temp_docx'

    # Extract the .docx file (which is a zip) into the temp directory
    with zipfile.ZipFile(_docx_path, 'r') as docx:
        docx.extractall(temp_dir)
    print("opening template docx")
    # Path to the main document XML file
    document_xml_path = os.path.join(temp_dir, 'word', 'document.xml')

    # Parse the XML
    tree = ET.parse(document_xml_path)
    root = tree.getroot()

    # Define the namespace used in the document.xml
    namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # Iterate over all text elements and replace the placeholders
    for node in root.findall('.//w:t', namespaces):
        text = node.text
        if text:
            # Replace any matching placeholders in the text
            for key, value in _replacements.items():
                if key in text:
                    node.text = text.replace(key, value)

    # Write the modified XML back to the file
    tree.write(document_xml_path)

    # Create a new zip file (output_path) with the modified contents
    with zipfile.ZipFile(_output_path, 'w') as new_docx:
        # Walk through the temp_dir and write the files back to a new .docx file
        for foldername, subfolders, filenames in os.walk(temp_dir):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path,
                                          temp_dir)  # Get the relative file path to maintain folder structure
                new_docx.write(file_path, arcname)

    # Clean up the temporary directory
    shutil.rmtree(temp_dir)
    print("program done, check output")


# Example usage:
docx_path = 'template/template.docx'  # Input document with placeholders
output_path = 'output/output.docx'  # Output document after replacement

# Dictionary with placeholders as keys and their replacements as values
replacements = {
    'name': 'John Doe',
    'date': 'August 21, 2024',
    'location': 'New York'
}

# Call the function to replace placeholders
replace_placeholders_in_docx(docx_path, output_path, replacements)
