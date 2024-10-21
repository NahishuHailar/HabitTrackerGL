
def check_input_progrees(habit, request):
    tasks = habit.routine_tasks.all()
    current_progress = [i for i in tasks if i.is_done]
    input_progress = request.data.get("routine_tasks")   
    return len(current_progress)


