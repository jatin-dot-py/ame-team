import asyncio
from markdown_it import MarkdownIt
from markdown_it.token import Token
import aiofiles
import json
from common import vcprint, pretty_print, get_sample_data
from automation_matrix import Processor
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin

from markdown_it.tree import SyntaxTreeNode  # Currently not using this but should


verbose = False


class Markdown(Processor):
    def __init__(self, style='asterisks'):
        self.md = MarkdownIt("commonmark")
        self.style = style  # Style of markdown ('asterisks' or 'hashes')
        #self.md.use(front_matter_plugin) # Currently not using front matter but should
        #self.md.use(footnote_plugin)  # Currently not using footnotes but should
        super().__init__()

    def parse_markdown(self, text: str):
        return self.md.parse(text)

    def _find_closing_token(self, tokens, start_idx, closing_type):
        for idx in range(start_idx + 1, len(tokens)):
            if tokens[idx].type == closing_type:
                return idx
        return start_idx

    def _extract_list_items(self, tokens):
        items = []
        i = 0
        while i < len(tokens):
            if tokens[i].type == 'list_item_open':
                end_idx = self._find_closing_token(tokens, i, 'list_item_close')
                item_content = ''.join(token.content for token in tokens[i + 1:end_idx] if token.type == 'inline')
                items.append(item_content)
                i = end_idx
            i += 1
        return items

    def _extract_ordered_list_items(self, tokens):
        items = []
        i = 0
        while i < len(tokens):
            if tokens[i].type == 'list_item_open':
                end_idx = self._find_closing_token(tokens, i, 'list_item_close')
                item_content = ''
                for j in range(i + 1, end_idx):
                    if tokens[j].type == 'inline':
                        item_content += tokens[j].content
                items.append(item_content.strip())
                i = end_idx
            i += 1
        return items

    #  This is where we can define unique markdown structures and styles and get them with specific methods
    def build_nested_structure(self, tokens, current_structure=None, level=0):
        if self.style == 'asterisks':  # This is the one I've been using a lot, but we need many more.
            return self._build_nested_asterisks_structure(tokens, current_structure, level)
        elif self.style == 'question_asterisks':  # Made this first, but the one above is doing this mostly now!
            return self._build_question_asterisks_structure(tokens, current_structure, level)
        elif self.style == 'hashes':
            return self._build_nested_hashes_structure(tokens, current_structure, level)
        else:
            raise ValueError(f"Unsupported style: {self.style}")

    def _build_nested_asterisks_structure(self, tokens: list[Token], current_structure=None, level=0) -> dict:
        if current_structure is None:
            current_structure = {
                'content': [],
                'sections': {}
            }

        current_heading = None
        i = 0
        while i < len(tokens):
            token = tokens[i]

            if token.type == 'inline':
                content_text = token.content.strip()
                if content_text.startswith("**"):
                    heading_text = content_text.strip("*").strip()
                    current_heading = heading_text
                    current_structure['sections'][current_heading] = {
                        'content': [],
                        'bullets': [],
                        'numbered_lists': []
                    }
                else:
                    if current_heading:
                        current_structure['sections'][current_heading]['content'].append(content_text)
                    else:
                        current_structure['content'].append(content_text)

            elif token.type == 'bullet_list_open':
                end_idx = self._find_closing_token(tokens, i, 'bullet_list_close')
                if current_heading:
                    list_items = self._extract_list_items(tokens[i + 1:end_idx])
                    current_structure['sections'][current_heading]['bullets'].extend(list_items)
                i = end_idx

            elif token.type == 'ordered_list_open' and current_heading:
                end_idx = self._find_closing_token(tokens, i, 'ordered_list_close')
                if current_heading:
                    ordered_list_items = self._extract_ordered_list_items(tokens[i + 1:end_idx])
                    current_structure['sections'][current_heading]['numbered_lists'].extend(ordered_list_items)
                i = end_idx

            i += 1

        return current_structure

    def _build_question_asterisks_structure(self, tokens: list[Token], current_structure=None, level=0) -> dict:
        if current_structure is None:
            current_structure = {
                'content': [],
                'sections': {}
            }

        current_heading = None
        i = 0
        while i < len(tokens):
            token = tokens[i]

            if token.type == 'inline':
                content_text = token.content.strip()
                if content_text.startswith("**"):
                    heading_text = content_text.strip("*").strip()
                    current_heading = heading_text
                    current_structure['sections'][current_heading] = {
                        'content': [],
                        'bullets': [],
                        'numbered_lists': []
                    }
                else:
                    if current_heading:
                        current_structure['sections'][current_heading]['content'].append(content_text)
                    else:
                        current_structure['content'].append(content_text)

            elif token.type == 'bullet_list_open':
                end_idx = self._find_closing_token(tokens, i, 'bullet_list_close')
                if current_heading:
                    list_items = self._extract_list_items(tokens[i + 1:end_idx])
                    current_structure['sections'][current_heading]['bullets'].extend(list_items)
                i = end_idx

            elif token.type == 'ordered_list_open':
                end_idx = self._find_closing_token(tokens, i, 'ordered_list_close')
                if current_heading:
                    ordered_list_items = self._extract_ordered_list_items(tokens[i + 1:end_idx])
                    current_structure['sections'][current_heading]['numbered_lists'].extend(ordered_list_items)
                i = end_idx

            i += 1

        return current_structure

    def _build_nested_hashes_structure(self, tokens, current_structure=None, level=0):
        # Implement the logic for parsing markdown structures using hashes (#, ##, ###) for headings
        pass

    def clean_up_text_and_organize(self, data):
        processed_data = {}

        for section, details in data.get("sections", {}).items():
            clean_section = section.replace("**", "")
            section_data = []

            for content_text in details.get("content", []):
                clean_content = content_text.replace("**", "")
                section_data.append(clean_content)

            # Format bullets with "- " at the start
            for bullet in details.get("bullets", []):
                clean_bullet = "- " + bullet.replace("**", "")
                section_data.append(clean_bullet)

            # Format numbered list items with their position and ". " at the start
            for i, ordered_list_item in enumerate(details.get("numbered_lists", []), start=1):
                clean_ordered_list_item = f"{i}. " + ordered_list_item.replace("**", "")
                section_data.append(clean_ordered_list_item)

            processed_data[clean_section] = section_data

        return processed_data

    # METHOD 1: All the work we do is for these two steps: This one gets it as plain, but organized clean text
    def get_section_as_text(self, data, section_number):
        sections = list(data.keys())
        try:
            section_title = sections[section_number - 1]
            children = data[section_title]
            section_text = f"{section_title}\n"
            for child in children:
                section_text += f"{child}\n"
            return section_text.strip()
        except IndexError:
            return f"Section number {section_number} is out of range. Please enter a valid section number."

    # METHOD 2: This one gets it as a nested structure so it's very easy to target whatever we want!
    async def process_markdown(self, text: str):
        loop = asyncio.get_running_loop()
        try:
            tokens = await loop.run_in_executor(None, self.parse_markdown, text)
            nested_structure = self.build_nested_structure(tokens)

            clean_structure = self.clean_up_text_and_organize(nested_structure)

            plain_text_sections = []
            for section_number in range(1, len(clean_structure) + 1):
                section_text = self.get_section_as_text(clean_structure, section_number)
                plain_text_sections.append(section_text)

            return {
                "nested_structure": clean_structure,
                "plain_text": plain_text_sections
            }
        except Exception as e:
            print(f"ERROR during markdown parsing: {str(e)}")
            return {
                "error": True,
                "message": f"Markdown parsing error: {str(e)}"
            }


async def get_markdown_asterisk_structure(markdown_text):
    processor = Markdown(style='asterisks')
    asterisk_structure_results = await processor.process_markdown(markdown_text)

    return asterisk_structure_results


async def save_object_as_text(filepath, obj):
    """Serializes an object to a text file in JSON format."""
    async with aiofiles.open(filepath, 'w', encoding='utf-8') as file:
        await file.write(json.dumps(obj, indent=2))


async def load_text_as_object(filepath):
    """Deserializes a text file containing JSON back into an object."""
    async with aiofiles.open(filepath, 'r', encoding='utf-8') as file:
        content = await file.read()
    return json.loads(content)


async def get_structure_from_file(filepath):
    async with aiofiles.open(filepath, 'r', encoding='utf-8') as file:
        content = await file.read()

    return content


def access_by_reference_with_key(reference, data_structure):
    """
    Access a nested dictionary entry along with its key based on a reference dictionary.

    :param reference: A dictionary with 'data' and 'key' where 'data' is the key to the main dictionary
                      and 'key' is the index to access within the nested dictionary.
    :param data_structure: The main data structure containing nested dictionaries.
    :return: A dictionary with the selected key and value, or None if not found.
    """
    nested_key = reference.get('data')
    index = reference.get('key') - 1  # Adjusting for 0-based indexing

    if nested_key in data_structure:
        nested_dict = data_structure[nested_key]
        keys = list(nested_dict.keys())
        if 0 <= index < len(keys):
            selected_key = keys[index]
            return {
                selected_key: nested_dict[selected_key]
            }  # Return the full key and its content

    return None  # Return None if the specified key/index is not found


def access_by_reference_as_text(reference, data_structure):
    """
    Access a nested dictionary entry along with its key and return as plain text based on a reference dictionary.

    :param reference: A dictionary with 'data' and 'key' where 'data' is the key to the main dictionary
                      and 'key' is the index to access within the nested dictionary.
    :param data_structure: The main data structure containing nested dictionaries.
    :return: A string with the selected key and value formatted as plain text, or a message if not found.
    """
    nested_key = reference.get('data')
    index = reference.get('key') - 1  # Adjusting for 0-based indexing

    if nested_key in data_structure:
        nested_dict = data_structure[nested_key]
        keys = list(nested_dict.keys())
        if 0 <= index < len(keys):
            selected_key = keys[index]
            content = nested_dict[selected_key]
            content_str = '\n'.join(content)  # Joining list elements into a single string separated by new lines
            return f"{selected_key}:\n{content_str}"  # Formatting the key and content as plain text

    return "The specified entry was not found."  # Return this message if the specified key/index is not found


def access_data_by_reference(extraction_map, data_structure):
    """
    Access a nested dictionary entry based on a reference dictionary and return it as specified (text or dict).

    :param reference: A dictionary with 'data', 'key', and 'output' where 'data' is the key to the main dictionary,
                      'key' is the index to access within the nested dictionary (None for entire structure), and
                      'output' specifies the return format ('text' or 'dict').
    :param data_structure: The main data structure containing nested dictionaries.
    :return: The selected entry in the specified format, or a message if not found.

        # Sample entry to get the 3rd key as text
        reference_text_3rd = {"data": "nested_structure", "key": 1, "output": "text"}

        # Sample entry to get the 2nd key as a dict
        reference_dict_2nd = {"data": "nested_structure", "key": 1, "output": "dict"}

        # Sample entry to get the entire nested structure as text
        reference_entire_text = {"data": "nested_structure", "key": None, "output": "text"}

    """
    nested_key = extraction_map.get('key_identifier')
    index = extraction_map.get('key_index')
    output_format = extraction_map.get('output_type', 'text')

    if not index and index != 0:
        nested_dict = data_structure.get(nested_key, {})
        print(f"nested_dict: {nested_dict}")
        if output_format == 'text':
            print(f"Output format is text")
            result = '\n\n'.join(f"{key}:\n{'\n'.join(value)}" for key, value in nested_dict.items())
            print(result)
        else:
            result = nested_dict
    else:
        index -= 1  # Adjust for 0-based indexing
        if nested_key in data_structure:
            nested_dict = data_structure[nested_key]
            keys = list(nested_dict.keys())
            if 0 <= index < len(keys):
                selected_key = keys[index]
                content = nested_dict[selected_key]
                if output_format == 'text':
                    result = f"{selected_key}:\n{'\n'.join(content)}"
                else:
                    result = {
                        selected_key: content
                    }
            else:
                print("Error! Index out of range.")
                result = ""
        else:
            print("Error! Key not found: ", nested_key)
            result = ""

    return result


def handle_OpenAIWrapperResponse(result):
    core_variable_name = result.get('variable_name', '') or 'no_variable_name'
    processed_values = result.get('processed_values', {}) or {}
    p_index = 0
    brokers = []

    print(f"Processing {core_variable_name}...")

    # Ensure the main 'result' dictionary will store all extracted values
    if result.get('processed_values'):
        print("Processing is still in progress.")
        for processor, processor_data in processed_values.items():
            p_index += 1  # This is for the processors
            e_index = 0  # This is for the individual extractors (eg. extracting multiple sections that have been processed)
            method_name = f"handle_{processor}"
            processor_value = processor_data.get('value', {}) or {}
            processor_nested_structure = processor_value.get('nested_structure', {}) or {}
            processor_plain_text = processor_value.get('plain_text', {}) or {}
            brokers.append({f"{core_variable_name}_NESTED_DICT_{p_index}": processor_nested_structure})
            brokers.append({f"{core_variable_name}_TEXT_DICT_{p_index}": processor_plain_text})

            if 'extraction' in processor_data:  # Triggers extraction, if extraction is listed as a method
                for extraction_map in processor_data['extraction']:
                    e_index += 1

                    if 'broker' in extraction_map:
                        broker_name = extraction_map['broker']
                    else:
                        broker_name = f"{p_index}_{e_index}_{core_variable_name}"

                    print(f"Processing broker name: {broker_name}")

                    try:
                        # Extract data by reference and store in the provided result dictionary
                        extraction_result = access_data_by_reference(extraction_map, processor_value)
                        new_entry = {broker_name: extraction_result}
                        brokers.append(new_entry)
                    except Exception as ex:
                        print(f"Error processing {broker_name} with {method_name}: {ex}")

    result['brokers'] = brokers
    return result


response_data = {
    "signature": "OpenAIWrapperResponse",
    "processing": "True",
    "variable_name": "FIVE_BLOG_IDEAS_FULL_RESPONSE_1001",
    "value": "1. **Headline:** \"Unlocking the Power of Plants: A Gastroenterologist's Guide to Transforming Your Digestive Health\"\n   - **Overview:** This post will explain how a plant-based diet influences digestive health from a gastroenterologist's viewpoint.\n   - **Target Audience:** Individuals suffering from digestive issues or anyone interested in understanding the health benefits of a plant-based diet.\n   - **Unique Angle:** Insight from a vegan gastroenterologist combines medical expertise with personal dietary choices.\n   - **Value Proposition:** Readers will gain a clear understanding of how a plant-based diet can prevent and treat common gastrointestinal issues.\n   - **Key Takeaways:** Importance of dietary fiber, ideal plant-based foods for gut health, and real patient success stories.\n   - **Engagement Triggers:** Questions about readers' current dietary habits and their impact on digestive health.\n   - **SEO Keywords:** Vegan gastroenterologist, plant-based digestive health doctor, digestive system diagnostics.\n   - **Tone and Style:** Informative, supportive, and empowering with patient success stories for a personal touch.\n\n2. **Headline:** \"The Science Behind Plant-Based Diets and Gut Health: A Gastroenterologist's Deep Dive\"\n   - **Overview:** An exploration of the scientific principles that make plant-based diets beneficial for the gastrointestinal system.\n   - **Target Audience:** Science-minded individuals and skeptics of plant-based diets.\n   - **Unique Angle:** A deep scientific analysis backed by research and clinical findings from a gastroenterology expert.\n   - **Value Proposition:** The reader will obtain a detailed understanding of the gut microbiome's response to plant-based diets.\n   - **Key Takeaways:** How plant-based diets influence gut flora, the science of digestion and absorption in context, and preventive aspects against chronic diseases.\n   - **Engagement Triggers:** Scientific evidence and case studies that debunk common myths about plant-based diets.\n   - **SEO Keywords:** Plant-based diet gastroenterologist, gastrointestinal health screening, digestive system diagnostics.\n   - **Tone and Style:** Analytical, detailed, with a focus on breaking down complex scientific concepts into accessible insights.\n\n3. **Headline:** \"A Gastroenterologist's Meal Planner: Nourishing Your Gut with Plant-Based Choices\"\n   - **Overview:** Provides a week-long meal plan created by a vegan gastroenterologist focusing on gut health.\n   - **Target Audience:** Anyone looking to transition to a plant-based diet or seeking to incorporate more plant-based meals for better digestion.\n   - **Unique Angle:** Personalized and professional dietary advice directly from a plant-based gastroenterology specialist.\n   - **Value Proposition:** Practical, easy-to-follow meal plans with recipes that promote optimal digestive health.\n   - **Key Takeaways:** Daily meal plans with nutrient-dense recipes, tips for meal prep, and advice on portion control for optimal gut health.\n   - **Engagement Triggers:** Interactive meal plan customization based on readers' dietary restrictions or preferences.\n   - **SEO Keywords:** Vegetarian gastroenterology specialist, plant-based nutrition advising, dietary consultation.\n   - **Tone and Style:** Approachable, encouraging, filled with actionable tips, and visually engaging meal ideas.\n\n4. **Headline:** \"Confronting Digestive Disorders with a Plant-Based Diet: A Gastroenterologist's Healing Journey\"\n   - **Overview:** An in-depth look at how transitioning to a plant-based diet can significantly impact various digestive disorders.\n   - **Target Audience:** Individuals diagnosed with or experiencing symptoms of digestive disorders.\n   - **Unique Angle:** Personal stories of recovery and scientific insights from a gastrointestinal doctor specializing in plant-based diets.\n   - **Value Proposition:** Hope and actionable advice for those struggling with digestive disorders who have not found relief in conventional treatments.\n   - **Key Takeaways:** Understanding common digestive disorders, testimonials of dietary changes leading to improvement, and steps to start a plant-based diet.\n   - **Engagement Triggers:** Invitation to share personal experiences and struggles with digestive health in the comments section.\n   - **SEO Keywords:** Digestive disorders physician, plant-based diet gastroenterologist, gastrointestinal consultant.\n   - **Tone and Style:** Inspiring, compassionate, with a mix of personal narratives and expert advice.\n\n5. **Headline:** \"Beyond Digestion: The Role of a Plant-Based Diet in Holistic Health According to a Gastroenterologist\"\n   - **Overview:** Explores the broader health benefits of a plant-based diet beyond the digestive system, including mental health and chronic disease prevention.\n   - **Target Audience:** Health-conscious individuals seeking a comprehensive approach to well-being.\n   - **Unique Angle:** A holistic view on health from a plant-based gastroenterologist, integrating physical, mental, and emotional health aspects.\n   - **Value Proposition:** A broader understanding of the systemic benefits of a plant-based diet, inspiring readers to consider their overall health.\n   - **Key Takeaways:** Connections between gut health and mental health, the role of diet in managing stress, and preventing chronic diseases with nutrition.\n   - **Engagement Triggers:** Encouragement to reflect on and share their holistic health journeys and dietary habits.\n   - **SEO Keywords:** Holistic health management, plant-based digestive health doctor, dietary consultation.\n   - **Tone and Style:** Comprehensive, engaging, with an emphasis on whole-person wellness and preventive care.",
    "processed_values": {
        "get_markdown_asterisk_structure": {
            "value": {
                "nested_structure": {
                    "Headline: \"Unlocking the Power of Plants: A Gastroenterologist's Guide to Transforming Your Digestive Health\"": [
                        "Overview: This post will explain how a plant-based diet influences digestive health from a gastroenterologist's viewpoint.",
                        "Target Audience: Individuals suffering from digestive issues or anyone interested in understanding the health benefits of a plant-based diet.",
                        "Unique Angle: Insight from a vegan gastroenterologist combines medical expertise with personal dietary choices.",
                        "Value Proposition: Readers will gain a clear understanding of how a plant-based diet can prevent and treat common gastrointestinal issues.",
                        "Key Takeaways: Importance of dietary fiber, ideal plant-based foods for gut health, and real patient success stories.",
                        "Engagement Triggers: Questions about readers' current dietary habits and their impact on digestive health.",
                        "SEO Keywords: Vegan gastroenterologist, plant-based digestive health doctor, digestive system diagnostics.",
                        "Tone and Style: Informative, supportive, and empowering with patient success stories for a personal touch."
                    ],
                    "Headline: \"The Science Behind Plant-Based Diets and Gut Health: A Gastroenterologist's Deep Dive\"": [
                        "Overview: An exploration of the scientific principles that make plant-based diets beneficial for the gastrointestinal system.",
                        "Target Audience: Science-minded individuals and skeptics of plant-based diets.",
                        "Unique Angle: A deep scientific analysis backed by research and clinical findings from a gastroenterology expert.",
                        "Value Proposition: The reader will obtain a detailed understanding of the gut microbiome's response to plant-based diets.",
                        "Key Takeaways: How plant-based diets influence gut flora, the science of digestion and absorption in context, and preventive aspects against chronic diseases.",
                        "Engagement Triggers: Scientific evidence and case studies that debunk common myths about plant-based diets.",
                        "SEO Keywords: Plant-based diet gastroenterologist, gastrointestinal health screening, digestive system diagnostics.",
                        "Tone and Style: Analytical, detailed, with a focus on breaking down complex scientific concepts into accessible insights."
                    ],
                    "Headline: \"A Gastroenterologist's Meal Planner: Nourishing Your Gut with Plant-Based Choices\"": [
                        "Overview: Provides a week-long meal plan created by a vegan gastroenterologist focusing on gut health.",
                        "Target Audience: Anyone looking to transition to a plant-based diet or seeking to incorporate more plant-based meals for better digestion.",
                        "Unique Angle: Personalized and professional dietary advice directly from a plant-based gastroenterology specialist.",
                        "Value Proposition: Practical, easy-to-follow meal plans with recipes that promote optimal digestive health.",
                        "Key Takeaways: Daily meal plans with nutrient-dense recipes, tips for meal prep, and advice on portion control for optimal gut health.",
                        "Engagement Triggers: Interactive meal plan customization based on readers' dietary restrictions or preferences.",
                        "SEO Keywords: Vegetarian gastroenterology specialist, plant-based nutrition advising, dietary consultation.",
                        "Tone and Style: Approachable, encouraging, filled with actionable tips, and visually engaging meal ideas."
                    ],
                    "Headline: \"Confronting Digestive Disorders with a Plant-Based Diet: A Gastroenterologist's Healing Journey\"": [
                        "Overview: An in-depth look at how transitioning to a plant-based diet can significantly impact various digestive disorders.",
                        "Target Audience: Individuals diagnosed with or experiencing symptoms of digestive disorders.",
                        "Unique Angle: Personal stories of recovery and scientific insights from a gastrointestinal doctor specializing in plant-based diets.",
                        "Value Proposition: Hope and actionable advice for those struggling with digestive disorders who have not found relief in conventional treatments.",
                        "Key Takeaways: Understanding common digestive disorders, testimonials of dietary changes leading to improvement, and steps to start a plant-based diet.",
                        "Engagement Triggers: Invitation to share personal experiences and struggles with digestive health in the comments section.",
                        "SEO Keywords: Digestive disorders physician, plant-based diet gastroenterologist, gastrointestinal consultant.",
                        "Tone and Style: Inspiring, compassionate, with a mix of personal narratives and expert advice."
                    ],
                    "Headline: \"Beyond Digestion: The Role of a Plant-Based Diet in Holistic Health According to a Gastroenterologist\"": [
                        "Overview: Explores the broader health benefits of a plant-based diet beyond the digestive system, including mental health and chronic disease prevention.",
                        "Target Audience: Health-conscious individuals seeking a comprehensive approach to well-being.",
                        "Unique Angle: A holistic view on health from a plant-based gastroenterologist, integrating physical, mental, and emotional health aspects.",
                        "Value Proposition: A broader understanding of the systemic benefits of a plant-based diet, inspiring readers to consider their overall health.",
                        "Key Takeaways: Connections between gut health and mental health, the role of diet in managing stress, and preventing chronic diseases with nutrition.",
                        "Engagement Triggers: Encouragement to reflect on and share their holistic health journeys and dietary habits.",
                        "SEO Keywords: Holistic health management, plant-based digestive health doctor, dietary consultation.",
                        "Tone and Style: Comprehensive, engaging, with an emphasis on whole-person wellness and preventive care."
                    ]
                },
                "plain_text": [
                    "Headline: \"Unlocking the Power of Plants: A Gastroenterologist's Guide to Transforming Your Digestive Health\"\n- Overview: This post will explain how a plant-based diet influences digestive health from a gastroenterologist's viewpoint.\n- Target Audience: Individuals suffering from digestive issues or anyone interested in understanding the health benefits of a plant-based diet.\n- Unique Angle: Insight from a vegan gastroenterologist combines medical expertise with personal dietary choices.\n- Value Proposition: Readers will gain a clear understanding of how a plant-based diet can prevent and treat common gastrointestinal issues.\n- Key Takeaways: Importance of dietary fiber, ideal plant-based foods for gut health, and real patient success stories.\n- Engagement Triggers: Questions about readers' current dietary habits and their impact on digestive health.\n- SEO Keywords: Vegan gastroenterologist, plant-based digestive health doctor, digestive system diagnostics.\n- Tone and Style: Informative, supportive, and empowering with patient success stories for a personal touch.",
                    "Headline: \"The Science Behind Plant-Based Diets and Gut Health: A Gastroenterologist's Deep Dive\"\n- Overview: An exploration of the scientific principles that make plant-based diets beneficial for the gastrointestinal system.\n- Target Audience: Science-minded individuals and skeptics of plant-based diets.\n- Unique Angle: A deep scientific analysis backed by research and clinical findings from a gastroenterology expert.\n- Value Proposition: The reader will obtain a detailed understanding of the gut microbiome's response to plant-based diets.\n- Key Takeaways: How plant-based diets influence gut flora, the science of digestion and absorption in context, and preventive aspects against chronic diseases.\n- Engagement Triggers: Scientific evidence and case studies that debunk common myths about plant-based diets.\n- SEO Keywords: Plant-based diet gastroenterologist, gastrointestinal health screening, digestive system diagnostics.\n- Tone and Style: Analytical, detailed, with a focus on breaking down complex scientific concepts into accessible insights.",
                    "Headline: \"A Gastroenterologist's Meal Planner: Nourishing Your Gut with Plant-Based Choices\"\n- Overview: Provides a week-long meal plan created by a vegan gastroenterologist focusing on gut health.\n- Target Audience: Anyone looking to transition to a plant-based diet or seeking to incorporate more plant-based meals for better digestion.\n- Unique Angle: Personalized and professional dietary advice directly from a plant-based gastroenterology specialist.\n- Value Proposition: Practical, easy-to-follow meal plans with recipes that promote optimal digestive health.\n- Key Takeaways: Daily meal plans with nutrient-dense recipes, tips for meal prep, and advice on portion control for optimal gut health.\n- Engagement Triggers: Interactive meal plan customization based on readers' dietary restrictions or preferences.\n- SEO Keywords: Vegetarian gastroenterology specialist, plant-based nutrition advising, dietary consultation.\n- Tone and Style: Approachable, encouraging, filled with actionable tips, and visually engaging meal ideas.",
                    "Headline: \"Confronting Digestive Disorders with a Plant-Based Diet: A Gastroenterologist's Healing Journey\"\n- Overview: An in-depth look at how transitioning to a plant-based diet can significantly impact various digestive disorders.\n- Target Audience: Individuals diagnosed with or experiencing symptoms of digestive disorders.\n- Unique Angle: Personal stories of recovery and scientific insights from a gastrointestinal doctor specializing in plant-based diets.\n- Value Proposition: Hope and actionable advice for those struggling with digestive disorders who have not found relief in conventional treatments.\n- Key Takeaways: Understanding common digestive disorders, testimonials of dietary changes leading to improvement, and steps to start a plant-based diet.\n- Engagement Triggers: Invitation to share personal experiences and struggles with digestive health in the comments section.\n- SEO Keywords: Digestive disorders physician, plant-based diet gastroenterologist, gastrointestinal consultant.\n- Tone and Style: Inspiring, compassionate, with a mix of personal narratives and expert advice.",
                    "Headline: \"Beyond Digestion: The Role of a Plant-Based Diet in Holistic Health According to a Gastroenterologist\"\n- Overview: Explores the broader health benefits of a plant-based diet beyond the digestive system, including mental health and chronic disease prevention.\n- Target Audience: Health-conscious individuals seeking a comprehensive approach to well-being.\n- Unique Angle: A holistic view on health from a plant-based gastroenterologist, integrating physical, mental, and emotional health aspects.\n- Value Proposition: A broader understanding of the systemic benefits of a plant-based diet, inspiring readers to consider their overall health.\n- Key Takeaways: Connections between gut health and mental health, the role of diet in managing stress, and preventing chronic diseases with nutrition.\n- Engagement Triggers: Encouragement to reflect on and share their holistic health journeys and dietary habits.\n- SEO Keywords: Holistic health management, plant-based digestive health doctor, dietary consultation.\n- Tone and Style: Comprehensive, engaging, with an emphasis on whole-person wellness and preventive care."
                ]
            },
            "depends_on": "content",
            "args": {},
            "extraction": [
                {
                    "key_identifier": "nested_structure",
                    "key_index": 1,
                    "output_type": "text",
                    "broker": "BLOG_IDEA_1"
                },
                {
                    "key_identifier": "nested_structure",
                    "key_index": 2,
                    "output_type": "text",
                    "broker": "BLOG_IDEA_2"

                },
                {
                    "key_identifier": "nested_structure",
                    "key_index": 3,
                    "output_type": "text",
                    "broker": "BLOG_IDEA_3"
                },
                #  I have commented out Blog Idea 4 for demonstration purposes as though the request was to get blogs 1, 2, 3, and 5, but NOT 4
                # {
                #    "key_identifier": "nested_structure",
                #    "key_index": 4,
                #    "output_type": "text",
                #    "broker": "BLOG_IDEA_4"
                # },
                {
                    "key_identifier": "nested_structure",
                    "key_index": 5,
                    "output_type": "text",
                    "broker": "BLOG_IDEA_5"
                }
            ]
        }
    }
}


async def main(data):
    style = 'asterisks'
    # processor = Markdown(style)
    # content = await get_structure_from_file(filepath)
    # results = await processor.process_markdown(content)
    # nested_results = await processor.process_markdown(content)
    # root = results.get('processed_value')

    # response_data = response_data

    # Sample entry to get the 3rd key as text
    # reference_text_3rd = {"key_identifier": "nested_structure", "key_index": 1, "output_type": "text"}
    # Sample entry to get the 2nd key as a dict
    # reference_dict_2nd = {"key_identifier": "nested_structure", "key_index": 1, "output_type": "dict"}
    # Sample entry to get the entire nested structure as text
    # reference_entire_text = {"key_identifier": "nested_structure", "key_index": None, "output_type": "text"}

    # Results
    # pretty_print(access_data_by_reference(reference_text_3rd, nested_results))
    # pretty_print(access_data_by_reference(reference_dict_2nd, nested_results))
    # pretty_print(access_data_by_reference(reference_entire_text, nested_results))

    extraction_results = handle_OpenAIWrapperResponse(data)
    # pretty_print(extraction_results)

    # pretty_print(result)


if __name__ == "__main__":
    # sample_data = get_sample_data(app_name='automation_matrix', data_name='sample_1', sub_app='sample_openai_responses')
    # sample_markdown_processor_output = get_sample_data(app_name='automation_matrix', data_name='sample_markdown_processor_output', sub_app='sample_processing_data')
    # pretty_print(sample_markdown_processor_output)

    extraction_result = handle_OpenAIWrapperResponse(response_data)
    pretty_print(extraction_result)

    # asyncio.run(main_async(filepath=filepath))

    # asyncio.run(get_structure_from_file(filepath=filepath, count=2))

    # asyncio.run(main_async())

    # Testing fine tuning data
    # sample_data = get_sample_fine_tuning_response()
    # asyncio.run(main(sample_data))
