import logging
from common import pretty_print, cool_print
import traceback


# All errors must be handled through this class and have specific handlers
# A class needs to be set up for each manager that needs to handle errors, just like these examples

class ErrorHandler:
    def __init__(self, RecipeProcessor=None, recipe_id=None, manager=None):
        self.orchestrator = None
        self.recipe_processor = RecipeProcessor
        self.recipe_id = recipe_id
        self.manager = manager
        self.error_message = "unknown error"
        self.reported_errors = set()
        self.error_package = {
            "recipe_id": recipe_id,
            "manager": manager,
            "method": "unknown",
            "error_message": self.error_message,
            "traceback": traceback.format_exc()
        }

    def set_recipe_processor(self, RecipeProcessor):
        self.recipe_processor = RecipeProcessor

    def set_orchestrator(self, Orchestrator):
        self.orchestrator = Orchestrator

    class RecipeManagerError:
        def __init__(self, RecipeManager, ErrorHandler):
            self.error_handler = ErrorHandler
            self.manager = RecipeManager

        def error(
                self,
                method,
                error_message,
                error_type="critical",
                recipe_id=None):
            self.error_handler.handle(
                self,
                method=method,
                error_message=error_message,
                error_type=error_type,
                recipe_id=recipe_id,
                manager=self.manager)

    class ModelError:
        def __init__(self, ModelManager, ErrorHandler):
            self.error_handler = ErrorHandler
            self.manager = ModelManager

        def error(self, method, error_message, error_type="critical", recipe_id=None):
            self.error_handler.handle(self, method=method, error_message=error_message, error_type=error_type,
                                      recipe_id=recipe_id, manager=self.manager)

    class VariableError:
        def __init__(self, VariableManager, ErrorHandler):
            self.error_handler = ErrorHandler
            self.manager = VariableManager

        def error(self, method, error_message, error_type="critical", recipe_id=None):
            self.error_handler.handle(self, method=method, error_message=error_message, error_type=error_type,
                                      recipe_id=recipe_id, manager=self.manager)

    class TokenError:
        def __init__(self, TokenManager, ErrorHandler):
            self.error_handler = ErrorHandler
            self.manager = TokenManager

        def error(self, method, error_message, error_type="critical", recipe_id=None):
            self.error_handler.handle(self, method=method, error_message=error_message, error_type=error_type,
                                      recipe_id=recipe_id, manager=self.manager)

    class AiApiError:
        def __init__(self, AiApiManager, ErrorHandler):
            self.error_handler = ErrorHandler
            self.manager = AiApiManager

        def error(self, method, error_message, error_type="critical", recipe_id=None):
            self.error_handler.handle(self, method=method, error_message=error_message, error_type=error_type,
                                      recipe_id=recipe_id, manager=self.manager)

    def handle(self, method, error_message, error_type="critical", recipe_id=None, manager=None):
        self.error_package["method"] = method
        self.error_package["error_type"] = error_type
        self.error_package["error_message"] = error_message
        self.error_package["recipe_id"] = recipe_id or self.error_package["recipe_id"]
        self.error_package["manager"] = manager or self.error_package["manager"]
        self.print_and_log()
        self.process_error(error_type)

    def print_and_log(self):
        self.print()
        self.log()

    def print(self, color="red"):
        cool_print(text=self.error_package, color=color, style="bold")

    def log(self):
        logging.error(self.error_package)

    def process_error(self, error_type):
        if error_type == "critical":
            self.terminate_process()
        elif error_type == "rate_limit":
            cool_print(text="Rate limit error. Recovery not implemented...", color="yellow", style="bold")
        elif error_type == "model_error":
            cool_print(text="Model error. Recovery not implemented...", color="yellow", style="bold")
        elif error_type == "missing_variables":
            cool_print(text="Missing variables error. Recovery not implemented...", color="yellow", style="bold")
        elif error_type == "configuration_error":
            cool_print(text="Configuration error. Recovery not implemented...", color="yellow", style="bold")
        elif error_type == "token_limit":
            cool_print(text="Token limit error. Recovery not implemented...", color="yellow", style="bold")
        elif error_type == "unknown":
            cool_print(text="Unknown error. Recovery not implemented...", color="yellow", style="bold")
        else:
            self.attempt_recovery()

    def report_missing_variable(self, method, variable_names):
        self.error_package["method"] = method
        self.error_package["error_message"] = f"Missing required variables."
        self.error_package["missing_variables"] = variable_names
        logging.error(self.error_package)
        pretty_print(self.error_package)
        self.terminate_process()

    def terminate_process(self):
        import sys
        print("Terminating process due to error...")
        sys.exit(1)

    def attempt_recovery(self):
        self.check_for_missing_variables()
        self.check_for_token_limit()
        self.check_for_model_error()
        self.check_package_configurations()
        self.process_error_message()
        pretty_print(self.error_package)

    def process_error_message(self):
        return self.error_package

    def check_for_missing_variables(self):
        missing_variables = self.recipe_processor.variable_manager.check_for_missing_variables()
        if missing_variables:
            self.error_package["missing_variables"] = missing_variables

    def check_for_token_limit(self):
        available_tokens = self.recipe_processor.token_manager.get_available_input_tokens()
        if available_tokens < 0:  # This is not accurate
            self.error_package["available_tokens"] = available_tokens

    def check_for_model_error(self):
        listed_models = self.recipe_processor.model_manager.all_models
        attempted_model = self.recipe_processor.model_manager.selected_model
        if attempted_model not in listed_models:
            self.error_package["model_error"] = f"Model '{attempted_model}' not found in available models."

    def check_package_configurations(self):
        api_call_package = {}
        try:
            api_call_package = self.recipe_processor.api_manager.api_call_package
        except AttributeError:
            self.error_package["configuration_errors"] = ["api_manager is missing 'api_call_package' attribute"]

        configuration_errors = []
        required_top_level_keys = ['endpoint', 'config', 'post_params']
        for key in required_top_level_keys:
            if key not in api_call_package:
                configuration_errors.append(f"Missing required key '{key}' in api_call_package.")

        if 'config' in api_call_package:
            required_config_keys = ['model', 'messages']
            for key in required_config_keys:
                if key not in api_call_package['config']:
                    configuration_errors.append(f"Missing required key '{key}' in api_call_package['config'].")
        else:
            configuration_errors.append("Missing required 'config' key in api_call_package.")

        if configuration_errors:
            self.error_package["configuration_errors"] = configuration_errors
