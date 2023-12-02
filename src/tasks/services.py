def get_suitable_employee(base_task_executor):
    """
    Подбирает подходящего сотрудника для выполнения задачи.
    Подходящий сотрудник - сотрудник с наименьшей занятостью
    или сотрудник выполняющий родительскую задачу если ему
    назначено максимум на 2 задачи больше, чем у наименее
    загруженного сотрудника.
    """
    not_busy_employee = []
    nb_tasks = []

    bt_tasks = base_task_executor.tasks.is_active.count()

    result = bt_tasks - nb_tasks
    if result <= 2:
        suitable_employee = base_task_executor
    else:
        suitable_employee = not_busy_employee

    return suitable_employee
