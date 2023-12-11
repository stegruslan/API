import json

PATH = 'tasks.json'


def write_tasks(tasks: list[dict[str, str | int]], path=PATH):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)


def read_tasks(path=PATH) -> list[dict[str, str | int]]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def filter_tasks(tasks: list[dict[str, str | int]], priority: int) -> list[dict[str, str | int]]:
    return [
        task
        for task in tasks
        if task.get('priority') == priority
    ]


