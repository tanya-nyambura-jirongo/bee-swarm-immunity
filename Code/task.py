# task.py - Task generation and decomposition

from typing import List

class Task:
    """Represents a task with harmfulness score."""
    
    def __init__(self, task_id: int, task_type: str, harmfulness: float, 
                 is_subtask: bool = False):
        self.id = task_id
        self.type = task_type
        self.harmfulness = harmfulness
        self.is_subtask = is_subtask
        self.status = 'pending'
        self.result = None


class TaskQueue:
    """Queue of tasks for agents."""
    
    def __init__(self):
        self.tasks = {}
        self.task_counter = 0
    
    def add_task(self, task_type: str, harmfulness: float) -> Task:
        """Add a new task to the queue."""
        task = Task(self.task_counter, task_type, harmfulness)
        self.tasks[self.task_counter] = task
        self.task_counter += 1
        return task
    
    def get_tasks_for(self, agent_id: int) -> List[Task]:
        """Get tasks assigned to an agent."""
        assigned_tasks = []
        for task_id, task in self.tasks.items():
            if task_id % 10 == agent_id % 10:
                assigned_tasks.append(task)
        return assigned_tasks
