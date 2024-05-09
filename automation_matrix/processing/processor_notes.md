# Some of the processors:

processors = [
    {
        'processor': 'get_markdown_asterisk_structure',
        'depends_on': 'content',
    },
    {
        'processor': 'define_key_value_pairs',
        'depends_on': 'add_parts',
    },
    {
        'processor': 'data_groups',
        'depends_on': 'get_markdown_asterisk_structure',
    },
    {
        'processor': 'clean_groups',
        'depends_on': 'data_groups',
    },
    {
        'processor': 'validate_data'
    },
    {
        'processor': 'add_parts',
        'depends_on': 'clean_groups',
    },
    {
        'processor': 'oai_fine_tuning_data',
        'depends_on': 'content',
    },
    {
        'processor': 'oai_fine_tuning_data',
        'depends_on': 'define_key_value_pairs',
    }
]
