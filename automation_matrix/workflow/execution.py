import asyncio
from collections import defaultdict


# Just placeholder classes since they will interact with the actual classes in the main codebase

class TaskManager:
    def __init__(self):
        self.tasks = []

    async def add_task(self, task):
        created_task = asyncio.create_task(task)
        self.tasks.append(created_task)
        return created_task

    async def add_db_task(self, item, value):
        print(f"[Task Manager Placeholder] Adding DB Task: {item} - {value}")
        await asyncio.sleep(1)

    async def wait_for_tasks(self):
        await asyncio.gather(*self.tasks)

    def add_task_sync(self, coro):
        loop = asyncio.get_event_loop()
        if loop.is_running():
            task = loop.create_task(coro)
            self.tasks.append(task)
            return task
        else:
            raise RuntimeError("No running event loop found")


class ValueBroker:
    def __init__(self):
        self.subscriptions = defaultdict(list)
        self.last_clean_values = {}
        self.task_manager = TaskManager()
        self.broker_status = {}
        self.recipe_vars = {}

    def update_broker_status(self, name, status):
        """Update the status of a specific broker."""
        if name in self.broker_status:
            self.broker_status[name]['status'] = status
        else:
            print(f"No broker found with the name {name}.")

    def subscribe(self, broker_name, callback, is_recipe_var=False):
        self.subscriptions[broker_name].append((callback, is_recipe_var))
        if broker_name in self.broker_status:
            self.broker_status[broker_name] = 'subscribed'
        else:
            self.broker_status[broker_name] = 'not_from_workflow_subscribed'

    async def publish(self, broker_name, value):
        if broker_name in self.subscriptions:
            for callback, is_recipe_var in self.subscriptions[broker_name]:
                if is_recipe_var:
                    data = {broker_name: value}
                else:
                    data = value

                await callback(data)

    def unsubscribe(self, broker_name, callback):
        if callback in self.subscriptions[broker_name]:
            self.subscriptions[broker_name].remove(callback)
