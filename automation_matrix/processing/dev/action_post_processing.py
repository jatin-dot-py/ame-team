import re
import asyncio
from common import pretty_print

# This is a different implementation that uses re, instead of markdown-it. Not sure which is better. For now, they kind of get similar results.
# Keep this because it might be more flexible, but not sure.


async def process_description(content, count=None):
    # Function to recursively process bullet points and their nested content
    def process_bullet_points(lines):
        result = []
        stack = [result]  # Use stack to manage nested lists
        prev_indent = 0

        bullet_point_pattern = re.compile(r'^(\s*[\*\-\+•])\s+(.*)')

        for line in lines:
            match = bullet_point_pattern.match(line)
            if match:
                indent, item = len(match.group(1)), match.group(2).strip()
                # Determine the current level of nesting based on indentation
                current_level = indent // 2  # Assuming two spaces per indent level

                # Adjust the stack based on the current nesting level
                while current_level < len(stack) - 1:
                    stack.pop()
                while current_level > len(stack) - 1:
                    new_list = []
                    stack[-1].append({'nested': new_list})
                    stack.append(new_list)

                # Add the current item to the top of the stack
                if stack[-1] and isinstance(stack[-1][-1], dict) and stack[-1][-1]['nested'] == '':
                    stack[-1][-1]['nested'] = item
                else:
                    stack[-1].append(item)

                prev_indent = indent
            else:
                # Non-bullet point lines reset the stack to the top-level list
                stack = [result]
                prev_indent = 0

        return result

    # Improved stripping of triple quotes and surrounding whitespace/newlines
    content = re.sub(r'^\s*\'\'\'\s*|\s*\'\'\'\s*$', '', content, flags=re.MULTILINE).strip()

    # Normalize line endings and split into lines
    lines = content.replace('\r\n', '\n').replace('\r', '\n').split('\n')

    # Define a dictionary to hold the structured data
    structured_data = {}

    # Extract section headers and their content
    section_pattern = re.compile(r'^(#+)\s*(.+?):\n', re.MULTILINE)
    sections = section_pattern.split(content)

    for i in range(1, len(sections), 3):
        header_level, header_title, section_content = sections[i], sections[i+1], sections[i+2]
        section_lines = section_content.strip().split('\n')
        structured_data[header_title] = process_bullet_points(section_lines)

    return structured_data

description_content = '''
## Overall image description:
* The image is a photograph of a young woman standing against a white background.
* The woman is wearing a black and white bikini.
* She has long, wavy brown hair and is looking at the camera with a serious expression.

### Model Description:
* The model is a young woman with a slim figure.
* She has light skin and dark brown eyes.
* Her hair is long, wavy, and brown.
* She is wearing a black bikini with white trim.
* The bikini top is a halter style with a low neckline.
* The bikini bottoms are high-cut and have a tie side.
* The model is standing with her feet shoulder-width apart and her arms at her sides.
* She is looking at the camera with a serious expression.
* Her body is slightly curved, with her hips thrust forward and her shoulders back.

### Clothing Description:
* The bikini is made of a thin, stretchy material.
* The top is a halter style with a low neckline.
* The bottoms are high-cut and have a tie side.
* The bikini is black with white trim.
* The model is wearing a necklace with a small pendant.
* She is also wearing a bracelet on her right wrist.

### Additional Observations:
* The model's skin is flawless and smooth.
* Her hair is thick and shiny.
* Her eyes are dark and mysterious.
* Her lips are full and pouty.
* Her body is perfectly proportioned.
* She is a very attractive woman.

### Alt Text Options:
* A young woman in a black and white bikini is standing against a white background.
* A model is wearing a black and white bikini and looking at the camera with a serious expression.
* A woman with long, wavy brown hair is wearing a black and white bikini and looking at the camera with a serious expression.
'''




description_content_3 = '''
# Project Overview:
* Project Name: Solar Power Analysis
* Description: A comprehensive analysis of global solar power usage trends.
* Contributors: John Doe, Jane Smith

## Goals:
* Evaluate current solar power installations worldwide.
* Forecast future growth in solar energy.

### Sub-Goals:
* Identify leading countries in solar power.
* Analyze the impact of government policies on solar energy adoption.

## Data Sources:
* [Global Solar Power Database](https://solarpower.example.com)
* [Renewable Energy Statistics](https://renewablestats.example.com)

### Primary Data Source:
* Name: SolarDataHub
* URL: `https://solardatahub.example.com`
* Description: A repository of global solar energy usage data.

## Methodology:
* Data Collection: Using APIs and public datasets.
* Data Analysis: Statistical analysis with Python.
  - Tools:
    * Python 3.8
    * Pandas for data manipulation
    * Matplotlib for data visualization

### Detailed Steps:
1. Data Collection:
   - Download data from SolarDataHub using Python requests.
   - Aggregate data from multiple sources.
2. Data Cleaning:
   - Remove incomplete records.
   - Normalize data formats.
3. Data Analysis:
   - Calculate growth rates.
   - Compare data year-over-year.

## Results:
* Solar power usage has increased by 25% over the last five years.
* Government incentives significantly impact adoption rates.

### Key Findings:
* The top three countries in solar energy adoption are A, B, C.
* There's a strong correlation between policy support and installation rates.

## Conclusion:
* Solar energy is on a rapid growth path.
* Continued support and investment are crucial for future growth.

### Recommendations:
* Increase government incentives.
* Support research and development in solar technology.

## Appendices:
* Appendix A: Data Collection Scripts
```python
import requests

def download_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
```
* Appendix B: Data Analysis Code
```python
import pandas as pd
import matplotlib.pyplot as plt

def analyze_data(data):
    # Data analysis steps
    pass
```
'''
description_content_2 = '''
## Overall image description:
# One Hash
## Two Hash
### Three Hash
1. One Period
1- One Dash
1) One Parenthesis
- One Dash
* One Asterisk
  - indented dash
    * Indented Asterisk double indent
    - indented dash (double)
#### Four Hash
##### Five Hash
###### Six Hash
####### Seven Hash

### Alt Text Options:
* A young woman in a black and white bikini is standing against a white background.
* A model is wearing a black and white bikini and looking at the camera with a serious expression.
* A woman with long, wavy brown hair is wearing a black and white bikini and looking at the camera with a serious expression.
'''




async def main():

    # Run the async function and print the result
    result = await process_description(description_content)
    pretty_print(result)


if __name__ == "__main__":
    asyncio.run(main())

