import pytesseract
import re
import json
from PIL import Image
import os
from common import pretty_print, cool_print
from common.utils.json_utils import save_to_json_from_base
from datetime import datetime
from common import print_link

'''
Functions
get_languages Returns all currently supported languages by Tesseract OCR.
get_tesseract_version Returns the Tesseract version installed in the system.
image_to_string Returns unmodified output as string from Tesseract OCR processing
image_to_boxes Returns result containing recognized characters and their box boundaries
image_to_data Returns result containing box boundaries, confidences, and other information. Requires Tesseract 3.05+. For more information, please check the Tesseract TSV documentation
image_to_osd Returns result containing information about orientation and script detection.
image_to_alto_xml Returns result in the form of Tesseract’s ALTO XML format.
run_and_get_output Returns the raw output from Tesseract OCR. Gives a bit more control over the parameters that are sent to tesseract.

Parameters

image_to_data(image, lang=None, config='', nice=0, output_type=Output.STRING, timeout=0, pandas_config=None)

image Object or String - PIL Image/NumPy array or file path of the image to be processed by Tesseract. If you pass object instead of file path, pytesseract will implicitly convert the image to RGB mode.

lang String - Tesseract language code string. Defaults to eng if not specified! Example for multiple languages: lang='eng+fra'

config String - Any additional custom configuration flags that are not available via the pytesseract function. For example: config='--psm 6'

nice Integer - modifies the processor priority for the Tesseract run. Not supported on Windows. Nice adjusts the niceness of unix-like processes.

output_type Class attribute - specifies the type of the output, defaults to string. For the full list of all supported types, please check the definition of pytesseract.Output class.

timeout Integer or Float - duration in seconds for the OCR processing, after which, pytesseract will terminate and raise RuntimeError.

pandas_config Dict - only for the Output.DATAFRAME type. Dictionary with custom arguments for pandas.read_csv. Allows you to customize the output of image_to_data.

'''


def image_to_text(image_path, config_options=''):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, config=config_options)
    return text


def image_to_boxes(image_path, config_options=''):
    img = Image.open(image_path)
    boxes = pytesseract.image_to_boxes(img, config=config_options)
    return boxes


def image_to_data(image_path, config_options=''):
    img = Image.open(image_path)
    data = pytesseract.image_to_data(img, config=config_options)
    return data


def image_to_osd(image_path, config_options=''):
    img = Image.open(image_path)
    osd = pytesseract.image_to_osd(img, config=config_options)
    return osd


def image_to_alto_xml(image_path, config_options=''):
    img = Image.open(image_path)
    alto_xml = pytesseract.image_to_alto_xml(img, config=config_options)
    return alto_xml


def run_and_get_output(image_path, config_options=''):
    img = Image.open(image_path)
    output = pytesseract.run_and_get_output(img, config=config_options)
    return output


def collect_and_format_results_optimized(image_path, config_options=''):
    img = Image.open(image_path)

    results = {
        "text": pytesseract.image_to_string(img, config=config_options),
        "boxes": pytesseract.image_to_boxes(img, config=config_options),
        "data": pytesseract.image_to_data(img, config=config_options),
        "osd": pytesseract.image_to_osd(img, config=config_options),
        "alto_xml": pytesseract.image_to_alto_xml(img, config=config_options),
        "run_and_get_output": pytesseract.run_and_get_output(img, config=config_options)
    }

    formatted_result = ""
    for key, value in results.items():
        formatted_result += f"---- {key.upper()} ----\n{value}\n\n"

    return formatted_result


def version_one():
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    lines = text.strip().splitlines()
    result = []

    for line in lines:
        parts = line.split()
        if len(parts) == 4:
            result.append({
                "value_1": int(parts[0]),
                "value_2": int(parts[3])
            })
    return result


def version_two(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, config="--psm 6")

    pattern = r"(\d+)\s*=\s*(\d+)"
    matches = re.findall(pattern, text)

    print("matches")
    print(matches)

    result = [
        {
            "value_1": int(match[0]),
            "value_2": int(match[1])
        } for match in matches
    ]
    return result


def save_to_json(json_results, filename_prefix="ocr_results"):
    save_directory_from_base = "temp/app_outputs/image_app_data"
    file_name = f"{save_directory_from_base}/{filename_prefix}.json"
    save_to_json_from_base(data=json_results, path_from_base=file_name, add_datetime=True)

def save_to_pdf(pdf, filename_prefix="ocr_results"):
    from aidream.settings import BASE_DIR
    file_name = f"{BASE_DIR}/temp/app_outputs/image_app_data/{filename_prefix}.pdf"

    with open(file_name, 'wb') as file:
        file.write(pdf)
    print_link(file_name)


def process_image(type, image_path, config_options='', save=False):
    functions = {
        'text': image_to_text,
        'boxes': image_to_boxes,
        'data': image_to_data,
        'osd': image_to_osd,
        'alto_xml': image_to_alto_xml,
        'output': run_and_get_output
    }

    if type in functions:
        result = functions[type](image_path, config_options)
        if save:
            save_to_json(result)
        return result
    else:
        raise ValueError(f"Unknown type: {type}")


if __name__ == "__main__":
    image_path = r"D:\OneDrive\Pictures\Screenshots\new4.png"
    filename_prefix = "ocr_results"
    type = 'text'
    config_options = '--psm 6'
    save = False

    # Need to figure out how to use the options, because they aren't working through this here.
    # result = collect_and_format_results_optimized(image_path=image_path, config_options='')
    # result_2 = version_two(image_path=image_path)

    result = process_image(type=type, image_path=image_path, config_options=config_options, save=save)
    print(result)

    pdf = pytesseract.image_to_pdf_or_hocr(image=image_path, extension='pdf')
    save_to_pdf(pdf, filename_prefix)
    # save_to_json(json_results, filename_prefix)
