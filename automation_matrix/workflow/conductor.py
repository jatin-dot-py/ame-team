from common import vcprint, cool_print, pretty_print
from automation_matrix import ErrorHandler
import asyncio

AsyncAiCaller, get_recipe_package, RecipeProcessor = None, None, None

verbose = False


# Just some placeholders to get a feel for the structure of the classes

class Conductor:
    def __init__(self, single):
        self.error_handler = ErrorHandler()
        self.single = single
        self.recipe_ais = {}
        self.agents = {}
        self.workflow = None
        self.task_manager = self.single.task_manager
        self.value_broker = self.single.value_broker
        self.conductor_event = asyncio.Event()
        print("[Conductor] Conductor Initialized")

    async def load_recipes(self, recipe_data):
        vcprint(verbose=verbose, data=recipe_data, title="load_recipes Recipe Data", color="green")

        for recipe in recipe_data:
            recipe_id = recipe['id']
            variable_objects = []

            for variable in recipe['variables']:
                vcprint(verbose=verbose, data=variable, title="load_recipes Variable", color="blue")
                variable_object = {
                    'name': variable['broker'],
                    'value': variable['value'],
                    'ready': variable['ready']
                }
                vcprint(verbose=verbose, data=variable_object, title="load_recipes Variable Object", color="red")
                variable_objects.append(variable_object)

            recipe_manager = self.RecipeAi(self, recipe_id=recipe_id, model_override=None,
                                           variable_objects=variable_objects)
            self.recipe_ais[recipe_id] = recipe_manager
            await recipe_manager.subscribe_all_variables()

    class RecipeAi():
        def __init__(self, conductor, recipe_id, model_override=None, variable_objects=None):
            print(
                f'[DEBUG] RecipeAi __init__ called with recipe_id={recipe_id}, model_override={model_override}, variable_objects={variable_objects}')
            self.conductor = conductor
            self.task_manager = self.conductor.task_manager
            self.value_broker = self.conductor.value_broker
            self.agents = {}
            self.recipe_id = recipe_id
            self.variable_objects = []
            self.model_override = model_override
            self.status = "initialized"

            if variable_objects:
                for variable_object in variable_objects:
                    self.variable_objects.append(variable_object)
            vcprint(verbose=verbose, data=variable_objects, title="Variable Objects", color="green")

            super().__init__(self.recipe_id, self.model_override, variable_values=None)

            vcprint(verbose=verbose,
                    data=f"[RecipeAi init] Recipe Processor Initialized with Recipe ID: {self.recipe_id}", color="blue")
            self.task_manager.add_task_sync(self.check_all_variables_ready())

        async def load_variable_objects(self, variable_objects):
            self.variable_objects = variable_objects  # Name, value, ready
            await self.check_all_variables_ready()

        async def subscribe_all_variables(self):
            for var_object in self.variable_objects:
                vcprint(verbose=verbose, data=var_object, title="subscribe_all_variables Variable Object",
                        color="green")
                if not var_object['ready']:
                    self.value_broker.subscribe(var_object['name'], self.set_variable_value, is_recipe_var=True)
                    vcprint(verbose=verbose, data=f"[RecipeAi] Subscribed to {var_object['name']}", color="blue")

        async def set_variable_value(self, var_name_value_object):
            vcprint(verbose=verbose, data=var_name_value_object, title="set_variable_value Received update from broker",
                    color="green")
            for var_name, value in var_name_value_object.items():
                for var_object in self.variable_objects:
                    if var_object['name'] == var_name:
                        var_object['value'] = value
                        var_object['ready'] = True
            await self.check_all_variables_ready()

        async def check_all_variables_ready(self):
            all_ready = True
            var_names_values = {}
            vcprint(verbose=verbose, data=self.variable_objects, title="check_all_variables_ready Variable Objects",
                    color="blue")
            for var_object in self.variable_objects:
                vcprint(verbose=verbose, data=var_object, title="check_all_variables_ready Variable Object",
                        color="green")
                var_name = var_object['name']
                var_names_values[var_name] = var_object['value']
                vcprint(verbose=verbose, data=var_object, title="check_all_variables_ready Variable Object",
                        color="green")
                if not var_object['ready']:
                    vcprint(verbose=verbose, data=f"[RecipeAi] {var_name} is not ready", color="blue")
                    all_ready = False
            if all_ready:
                self.set_variables(var_names_values)
                if not self.status == "running":
                    await self.get_package_and_call()

        async def get_package_and_call(self):
            self.status = "running"
            vcprint(verbose=verbose, data=f"[RecipeAi] Calling RecipeAi for Recipe ID: {self.recipe_id}", color="blue")

            missing_variables = await self.variable_manager.get_missing_variables()
            if missing_variables:
                vcprint(verbose=verbose, data=f"[RecipeAi] Missing Variables: {missing_variables}", color="red")
                return

            api_call_package = await self.get_full_call_package()
            vcprint(verbose=verbose, data=api_call_package, title="RecipeAi Full Call Package", color="green")
            response = await self.conductor.handle_recipe_call(api_call_package)
            return response

    class RecipeCallAI():
        def __init__(self, Conductor, task_manager, value_broker, call_package):
            super().__init__()
            self.conductor = Conductor
            self.task_manager = task_manager
            self.value_broker = value_broker
            self.call_package = call_package
            self.overrides = {}
            self.agents = {}
            vcprint(verbose=verbose, data=self.call_package, title="RecipeCallAI Call Package", color="green")
            self.set()

        async def make_call(self):
            response = await self.call()
            return response

        async def make_call_with_changes(self, call_package=None,
                                         overrides=None):  # this currently has no uses because the call can be made right after init.
            if call_package is not None:
                self.call_package = call_package
            if overrides is not None:
                self.overrides = overrides
            vcprint(verbose=verbose, data=self.call_package, title="RecipeCallAI Call Package", color="red")
            response = await self.set_and_call(call_package=self.call_package, overrides=self.overrides)
            return response

    async def handle_recipe_call(self, api_call_package):
        recipe_call_ai = self.RecipeCallAI(self, self.task_manager, self.value_broker, api_call_package)
        response = await recipe_call_ai.make_call()
        return response


class Agent:
    """ A specific AI Model, equipped with a specific recipe and a predefined set of tools."""
    __slots__ = ['conductor', 'name', 'conductor', 'workflow', 'task_manager', 'value_broker']

    def __init__(self, name, recipe, conductor):
        self.name = name
        self.recipe = recipe
        self.conductor = conductor
        self.workflow = conductor.workflow
        self.task_manager = None
        self.value_broker = None


class SuperAgent:
    """ A fine-tuned agent that is highly specialized for a specific task."""

    def __init__(self, name, model, recipe, conductor):
        self.name = name
        self.model = model
        self.recipe = recipe
        self.conductor = conductor
        self.workflow = conductor.workflow
        self.task_manager = None
        self.value_broker = None


class Tool:
    """ A set of functions or API calls with preformatted structure that can be used by an agent to perform a specific task."""

    def __init__(self, name, function, conductor):
        self.name = name
        self.function = function
        self.conductor = conductor
        self.workflow = conductor.workflow
        self.task_manager = None
        self.value_broker = None


class Task:
    """ A specific task that can be completed with any combination of recipes, agents, and tools."""

    def __init__(self, name, conductor):
        self.name = name
        self.conductor = conductor
        self.workflow = conductor.workflow
        self.task_manager = None
        self.value_broker = None


class Data:
    """ A data storage system that can be used to store and retrieve data by agents and throughout the system."""

    def __init__(self, name, conductor):
        self.name = name
        self.conductor = conductor
        self.workflow = conductor.workflow
        self.task_manager = None
        self.value_broker = None
        self.data_map = {}  # This will need to be set up to load from somewhere
        self.data = self.get_data()

    def get_data(
            self):  # Not sure if this works, but it would be a great way to get things like JOB_CODE_LIST and other things like that
        for name in self.data_map:
            self.data[name] = self.data_map[name]
        return self.data


class Memory:
    """ A memory storage system that can be used to store and retrieve data by agents and throughout the system."""

    def __init__(self, name, conductor):
        self.name = name
        self.conductor = conductor


class Short(Memory):
    """ A version of memory that is used for short-term storage during the execution of a Task, but not directly accessible in other workflow steps."""

    def __init__(self, name, conductor):
        super().__init__(name, conductor)


class Long(Memory):
    """ A version of memory that is used for long-term storage and is easily accessible during the entire process of a workflow."""

    def __init__(self, name, conductor):
        super().__init__(name, conductor)


class Permanent(Memory):
    """ A version of memory that is used for permanent storage and can be accessed at anytime."""

    def __init__(self, name, conductor):
        super().__init__(name, conductor)
