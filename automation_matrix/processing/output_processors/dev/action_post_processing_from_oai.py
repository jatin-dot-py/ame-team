import re
import ast
from bs4 import BeautifulSoup
from typing import Dict
from collections import defaultdict
from typing import List, Union

REMOVE_VALUES = True


def extract_bullet_point_content(text):
    """
    Extracts content from bullet points in a string.

    :param text: String containing the text to be processed.
    :return: List of strings, each containing the content of a bullet point.
    """
    # TODO not working as intended because it's pulling the list of LSIs, which is definitely not a bullet point. We need to be clear what a bullet point is
    # I think we need to be clear what a bullet point is, and then we can use this as a "parent" function that feeds others like extract_lists
    bullet_point_pattern = '(?:^\\s*[-*]\\s+.*(?:\\n|$))+'
    matches = re.findall(bullet_point_pattern, text, re.MULTILINE)
    bullet_points = [match.strip() for match in matches]
    return bullet_points



def extract_code_snippets(text: str) -> Dict[str, List[str]]:
    """
    Extracts code snippets enclosed in triple backticks along with their specified language.

    :param text: The raw output from AI.
    :return: Dictionary with language as key and list of code snippets in that language as value.
    """
    code_snippets = {}
    pattern = '```(\\w*)\\n([\\s\\S]*?)\\n```'
    matches = re.findall(pattern, text, re.MULTILINE)
    for language, code in matches:
        language = language if language else 'no_language'
        if language not in code_snippets:
            code_snippets[language] = []
        code_snippets[language].append(code.strip())
    return code_snippets



def process_urls(text: str, remove_values: bool = None) -> Union[List[str], str]:
    """
    Processes URLs in the text - either extracts them or removes them.

    :param text: String containing the text to be processed.
    :param remove_values: If True, removes URLs from the text else extracts them from the text.
                          If None, uses the value from the global REMOVE_VALUES variable.
    :return: List of extracted URLs or text without URLs based on remove_values.
    """
    # TODO note working and identifying even lsti lists as urls
    # Use global REMOVE_VALUES if remove_values is not provided
    if remove_values is None:
        remove_values = REMOVE_VALUES

    # Updated URL pattern to match more general web addresses
    url_pattern = r'\b(?:https?://)?(?:www\.)?[a-zA-Z0-9-]+(?:\.[a-zA-Z]{2,})+\b'

    if remove_values:
        return re.sub(url_pattern, '', text)
    else:
        return re.findall(url_pattern, text)



def parse_table(text: str) -> List[dict]:
    """
    Parses tabular data formatted with borders and pipes into a list of dictionaries.

    :param text: String containing the text to be processed.
    :return: List of dictionaries representing the table's rows.
    """
    table_pattern = '\\+-[+-]+\\+\\n(?:\\|.*\\|\\n)+\\+-[+-]+\\+'
    match = re.search(table_pattern, text)
    if not match:
        return []
    table = match.group().split('\n')[1:-1]
    headers = [header.strip() for header in table[0].split('|')[1:-1]]
    rows = [dict(zip(headers, [cell.strip() for cell in row.split('|')[1:-1
                                                        ]])) for row in table[1:]]
    return rows



def identify_python_dictionaries(text: str) -> List[dict]:
    """
    Searches for and interprets Python dictionary structures.

    :param text: String containing the text to be processed.
    :return: List of Python dictionaries extracted from the text.
    """
    dict_pattern = '\\{(?:[^{}]|(?:\\{.*?\\}))*\\}'
    matches = re.findall(dict_pattern, text)
    dictionaries = []
    for match in matches:
        try:
            dictionary = ast.literal_eval(match)
            if isinstance(dictionary, dict):
                dictionaries.append(dictionary)
        except (SyntaxError, ValueError):
            continue
    return dictionaries



def extract_lists(text: str) -> List[List[str]]:
    """
    Identifies both bullet-point and numbered lists and extracts them.

    :param text: String containing the text to be processed.
    :return: List of lists extracted from the text.
    """

    # TODO it's identifying lists of LSIs but not capturing the name of what the list is
    list_pattern = '(?:^\\s*(?:[-*]|\\d+\\.)\\s+.*(?:\\n|$))+'
    matches = re.findall(list_pattern, text, re.MULTILINE)
    lists = []
    for match in matches:
        items = [item.strip() for item in re.split(
            '\\n\\s*(?:[-*]|\\d+\\.)\\s+', match.strip()) if item]
        lists.append(items)
    return lists



def parse_html_content(text: str) -> List[str]:
    """
    Extracts HTML content sections as they are from the text.

    :param text: String containing the text with HTML.
    :return: List of HTML content sections.
    """
    html_pattern = '<[^>]+>.*?</[^>]+>'
    html_sections = re.findall(html_pattern, text, re.DOTALL)
    return html_sections



def parse_markdown_content(text: str) -> List[str]:
    """
    Identifies markdown formatting and extracts it as separate sections.

    :param text: String containing the text with Markdown.
    :return: List of strings, each containing a Markdown-formatted section.
    """
    # TODO not sure exactly what markdown content should include but it's including LSIs, but maybe that makes sense
    # If that makes sense, we should make this like a "parent" function that feeds others like extract_lists
    markdown_pattern = (
        '(?:\\n|^)(?:\\#{1,6}\\s.*|[-*]\\s.*|\\d+\\.\\s.*|\\>\\s.*|```[\\s\\S]*?```)'
    )
    markdown_sections = re.findall(markdown_pattern, text, re.MULTILINE)
    return markdown_sections



def extract_latex_equations(text: str) -> List[str]:
    """
    Searches for LaTeX equation patterns (both inline and display mode) and extracts them.

    :param text: String containing the text to be processed.
    :return: List of LaTeX equations.
    """
    latex_pattern = '\\\\\\(.*?\\\\\\)|\\\\\\[.*?\\\\\\]'
    return re.findall(latex_pattern, text)



def extract_plain_text(text: str) -> str:
    """
    Extracts plain text content, filtering out any special formatting or structured content.

    :param text: String containing the text to be processed.
    :return: Plain text content.
    """
    # TODO Considering it pulled a list of LSIs as "plain text", I'm not sure this is working as intended
    # I think we need a set of initial checks that essentially breaks up the content into "major cateogries" without any overlap, or very little overlap
    # Then we can have a set of functions that are more specific to each category
    # Otherwise, we might end up with so much duplicate content that it will clutter the results and make it really hard to interpret or save to the db
    text = re.sub('```[\\s\\S]*?```', '', text)
    text = re.sub('\\[.*?\\]\\(.*?\\)', '', text)
    text = re.sub('\\\\\\(.*?\\\\\\)', '', text)
    text = BeautifulSoup(text, 'html.parser').get_text()
    return text.strip()



def identify_fill_in_blanks(text: str) -> List[str]:
    """
    Identifies sentences with fill-in-the-blank structures.

    :param text: String containing the text to be processed.
    :return: List of sentences with blanks.
    """
    blank_pattern = '[^\\.\\?\\!]*__+[^\\.\\?\\!]*[\\.|\\?|\\!]'
    return re.findall(blank_pattern, text)



def parse_multiple_choice_questions(text: str) -> List[str]:
    """
    Identifies and extracts multiple-choice questions.

    :param text: String containing the text to be processed.
    :return: List of multiple-choice questions with options.
    """
    mcq_pattern = '(?:\\n|^).*\\?\\n(?:\\s*[a-zA-Z]\\)\\s.*\\n)+'
    return [mcq.strip() for mcq in re.findall(mcq_pattern, text, re.MULTILINE)]



def extract_paragraphs(text: str) -> List[str]:
    """
    Extracts paragraph-style text content.

    :param text: String containing the text to be processed.
    :return: List of paragraphs.
    """
    # TODO Not working as intended because it's pulling the list of LSIs, which is definitely not a paragraph. We need to be clear what a paragraph is
    paragraphs = re.split('\\n{2,}', text)
    return [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]



def identify_html_markdown_structured_text(text: str) -> Dict[str, List[str]]:
    """
    Specifically looks for and extracts structured text marked as HTML or Markdown.

    :param text: String containing the text to be processed.
    :return: Dictionary with HTML and Markdown content categorized.
    """
    # TODO Even through it actually returned empty results, they still printed, which might be a debugging print, but these should return nothing if they're empty
    # By providing resopnses with empty dictionaries, we're creating a lot more work for later, unless that was the intention - Need to review
    structured_content = {'html': [], 'markdown': []}
    html_pattern = '```html\\n([\\s\\S]*?)\\n```'
    markdown_pattern = '```markdown\\n([\\s\\S]*?)\\n```'
    html_matches = re.findall(html_pattern, text)
    structured_content['html'].extend(html_matches)
    markdown_matches = re.findall(markdown_pattern, text)
    structured_content['markdown'].extend(markdown_matches)
    return structured_content



def extract_prompts_questions(text: str) -> List[str]:
    """
    Extracts prompts and questions designed for user interaction.

    :param text: String containing the text to be processed.
    :return: List of prompts and questions.
    """
    prompt_question_pattern = '[^\\.\\?\\!]*\\?\\s*(?:\\n|$)'
    return re.findall(prompt_question_pattern, text)



def find_words_after_triple_quotes(s):
    pattern = re.compile("\\'\\'\\'(\\w+)")
    matches = re.findall(pattern, s)
    word_count = defaultdict(int)
    for word in matches:
        word_count[word] += 1
    return word_count



def assess_content_types(given_content):
    def print_section(title, content):
        if content:
            print(f"\n|||||Debug||||| Printing section {title}")
            print(f'\n========= {title} =========')
            print(f'\n{content}\n========= End {title} =========\n')

    code_snippets = extract_code_snippets(given_content)
    if code_snippets:
        print_section('Code Snippets', code_snippets)

    urls = process_urls(given_content)
    if urls:
        print_section('URLs', urls)

    table_data = parse_table(given_content)
    if table_data:
        print_section('Table Data', table_data)

    python_dicts = identify_python_dictionaries(given_content)
    if python_dicts:
        print_section('Python Dictionaries', python_dicts)

    lists = extract_lists(given_content)
    if lists:
        print_section('Lists', lists)

    html_content = parse_html_content(given_content)
    if html_content:
        print_section('HTML Content', html_content)

    markdown_content = parse_markdown_content(given_content)
    if markdown_content:
        print_section('Markdown Content', markdown_content)

    latex_equations = extract_latex_equations(given_content)
    if latex_equations:
        print_section('LaTeX Equations', latex_equations)

    plain_text = extract_plain_text(given_content)
    if plain_text:
        print_section('Plain Text', plain_text)

    fill_in_blanks = identify_fill_in_blanks(given_content)
    if fill_in_blanks:
        print_section('Fill in Blanks', fill_in_blanks)

    multiple_choice_questions = parse_multiple_choice_questions(given_content)
    if multiple_choice_questions:
        print_section('Multiple Choice Questions', multiple_choice_questions)

    paragraphs = extract_paragraphs(given_content)
    if paragraphs:
        print_section('Paragraphs', paragraphs)

    structured_text = identify_html_markdown_structured_text(given_content)
    if structured_text:
        print_section('Structured Text', structured_text)

    prompts_questions = extract_prompts_questions(given_content)
    if prompts_questions:
        print_section('Prompts and Questions', prompts_questions)

    words_after_triple_quotes = find_words_after_triple_quotes(given_content)
    if words_after_triple_quotes:
        print_section('Words After Triple Quotes', dict(words_after_triple_quotes))
