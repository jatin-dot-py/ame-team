class ProcessorHandler:
    def __init__(self):
        self.source_data = None
        self.value = None
        self.return_params = {}
        self.signature = None
        self.broker_name = None
        self.processing_manager = ProcessingManager()

    def signature_process(self, source_data):
        self.source_data = source_data
        self.value = self.source_data['value']
        self.return_params = self.source_data['return_params']
        self.signature = self.source_data['signature']
        self.broker_name = self.source_data(self.source_data['broker'])
        self.extract_data()

    def set_broker_name(self, broker_name):
        self.broker_name = broker_name

    def set_config(self, return_params):
        self.return_params = return_params

    def load_data(self, source_data):
        self.source_data = source_data
        self.signature = self.source_data['signature'] if 'signature' in self.source_data else 'default'
        self.extract_data()

    def extract_data(self):
        method_name = f"process_data_{self.signature}"
        method = getattr(self, method_name, self.process_data_default)
        method()

    def process_data_default(self):
        self.value = self.source_data

    def process_data_AiResponse(self):
        if not self.value:
            self.value = self.source_data['value']
        if not self.return_params:
            self.return_params = self.source_data['return_params']
        if not self.broker_name:
            self.broker_name = self.source_data['variable_name']
        if self.return_params:
            self.processing_manager.add_processor('AiResponse', None, self.return_params)


class ProcessingManager:
    def __init__(self):
        self.processors = []

    def add_processor(self, name, depends_on, args):
        processor = Processor()
        processor.name = name
        processor.depends_on = depends_on
        processor.args = args
        self.processors.append(processor)


class Processor:
    def __init__(self):
        self.name = None
        self.depends_on = None
        self.args = {}
        self.extractors = []

    def add_extractor(self, key, index, output_data_type, broker_name):
        extractor = Extractor()
        extractor.add_extractor(key, index, output_data_type, broker_name)
        self.extractors.append(extractor)


class Extractor:
    def __init__(self):
        self.key = None
        self.index = None
        self.output_data_type = None
        self.broker_name = None

    def add_extractor(self, key, index, output_data_type, broker_name):
        self.key = key
        self.index = index
        self.output_data_type = output_data_type
        self.broker_name = broker_name


class ExtractData(ProcessorHandler):
    def __init__(self):
        self.extraction_methods = []
        self.key_extractor = {}
        self.index_extractor = {}
        super().__init__()

    def add_extraction_method(self, key, method):
        self.extraction_methods.append(method)
        self.key_extractor[key] = method

    def process_data(self, source_data):
        self.get_processed_values(source_data)

    def extract_data(self):
        extracted_data = {}
        for key, value in self.source_data.items():
            extracted_data[key] = self.extract_value(value)
        return extracted_data

    def extract_value(self, value):
        if isinstance(value, dict):
            return self.extract_data(value)
        elif isinstance(value, list):
            return [self.extract_value(item) for item in value]
        else:
            return value
