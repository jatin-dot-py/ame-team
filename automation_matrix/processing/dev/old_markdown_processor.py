import asyncio
from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode


class MarkdownProcessor:
    def __init__(self):
        self.md = MarkdownIt("commonmark")

    def init_markdown_parser(self):
        return self.md

    def get_text_content(self, node):
        if node.type == 'text':
            return node.content
        elif node.children:
            return ' '.join(self.get_text_content(child) for child in node.children)
        return ''

    def parse_markdown(self, text):
        if not text:
            print("ERROR: parse_markdown received empty text.")
            return {}
        md = self.init_markdown_parser()
        tokens = md.parse(text)
        root_node = SyntaxTreeNode(tokens)  # Ensure SyntaxTreeNode is defined or imported
        return self.build_simple_structure(root_node.children)

    def build_simple_structure(self, nodes, content_dict=None, current_key='root'):
        if content_dict is None:
            content_dict = {
                current_key: []
            }

        for node in nodes:
            if node.type.startswith('heading'):
                current_key = self.get_text_content(node).strip()
                content_dict[current_key] = []
            elif node.type in ['paragraph', 'inline', 'text']:
                text = self.get_text_content(node).strip()
                if text:
                    content_dict[current_key].append(text)
            elif node.type in ['bullet_list', 'ordered_list']:
                for child in node.children:
                    if child.type == 'list_item':
                        list_item_text = self.get_text_content(child).strip()
                        if list_item_text:
                            content_dict[current_key].append(list_item_text)

        # pretty_print(content_dict)
        return content_dict

    def parse_markdown_nested(self, text):
        if not text:
            print("ERROR: parse_markdown received empty text.")
            return {}
        md = self.init_markdown_parser()
        tokens = md.parse(text)
        root_node = SyntaxTreeNode(tokens)
        return self.build_nested_structure(root_node.children)

    def build_nested_structure(self, nodes, content_dict=None, current_key='root'):
        if content_dict is None:
            content_dict = {
                current_key: {}
            }

        for node in nodes:
            if node.type.startswith('heading'):
                current_key = self.get_text_content(node).strip()
                content_dict[current_key] = {}
            elif node.type in ['paragraph', 'inline', 'text']:
                text = self.get_text_content(node).strip()
                if text:
                    if 'content' not in content_dict[current_key]:
                        content_dict[current_key]['content'] = []
                    content_dict[current_key]['content'].append(text)
            elif node.type in ['bullet_list', 'ordered_list']:
                content_dict[current_key]['sections'] = []
                for child in node.children:
                    if child.type == 'list_item':
                        list_item_text = self.get_text_content(child).strip()
                        if list_item_text:
                            content_dict[current_key]['sections'].append(list_item_text)

        # Assuming pretty_print is a method you use for debugging or displaying the structure
        # pretty_print(content_dict)
        return content_dict

    async def process_markdown(self, text):
        loop = asyncio.get_running_loop()
        try:
            result_dict = await loop.run_in_executor(None, self.parse_markdown, text)
            if not result_dict:
                print("ERROR: parse_markdown returned an empty dictionary.")
                return {
                    "error": True,
                    "message": "Markdown parsing resulted in an empty dictionary."
                }
            return {
                'processed_value': result_dict
            }

        except Exception as e:
            print(f"ERROR during markdown parsing: {str(e)}")
            return {
                "error": True,
                "message": f"Markdown parsing error: {str(e)}"
            }

    async def process_markdown_nested(self, text):
        loop = asyncio.get_running_loop()
        try:
            result_dict = await loop.run_in_executor(None, self.parse_markdown_nested, text)
            if not result_dict:
                print("ERROR: parse_markdown returned an empty dictionary.")
                return {
                    "error": True,
                    "message": "Markdown parsing resulted in an empty dictionary."
                }
            return {
                'processed_value': result_dict
            }

        except Exception as e:
            print(f"ERROR during markdown parsing: {str(e)}")
            return {
                "error": True,
                "message": f"Markdown parsing error: {str(e)}"
            }
