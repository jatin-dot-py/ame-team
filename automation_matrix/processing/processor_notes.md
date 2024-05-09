# Notes about the class-based processors and related things:
- Think in terms of INSTANCES to understand what we're trying to do here.
- Start with the END in mind.
- An example of "the end result" might be to get the individual bullet points from a large response.
- What gets the individual bullet points and associates them with a broker (variable) is an ExtractData instance.
- The thing that 'decides' how many bullets to get and where to find them is called an Extractor
- But the extractors can't just go get data. Something has to prepare the data for them. Those are Processors.
- But you can't have just one processor because there are MANY ways you have to go about identifying the data.
- Even just within markdown, you have many different ways to identify data.
- So we have a Classifier(Processor), we also have the Markdown(Processor), and we might need to add more.
- The key is to determine what is a classifier and what is an extractor.
- The classifier gets the data and organizes it in a way where an extractor can easily get it out using an "address"
- Sometimes, we can get the same data using multiple ways and that's great, but once we have one, we're good.
- For example, we could create a "code extractor" that can take an argument for "type" or "language" and get the code.
- But it needs to start with either the classifier or the markdown processor to be able to do it.
- The main thing I've done is to work REALLY HARD to build highly dynamic systems to classify and organize data.
- Now, we need to work on the details and ensure we can get the specific methods and functions done.
- Most importantly, we need to make sure they are reliable, consistent, and easy to use. 



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
