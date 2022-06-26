
from queue_array import Queue
#from queue_linked import Queue

class Task:

    tasks_created = 0

    def __init__(self,workload,arrival_time):
        self.id = Task.tasks_created
        Task.tasks_created += 1
        self.total_workload = workload
        self.remaining_workload = workload
        self.arrival_time = arrival_time

    def get_arrival_time(self):
        return self.arrival_time

    def is_done(self):
        return self.remaining_workload == 0

    def do_work(self):
        self.remaining_workload -= 1

    def __str__(self):
        return f"Task {self.id}: {self.remaining_workload}/{self.total_workload}"

def simulate(task_list,time_quantum):

    ready_queue = Queue()
    active_task = None

    tick = 0

    while active_task is not None or \
          len(ready_queue) > 0 or \
          len(task_list) > 0:

        # add tasks from task_list that are arriving this tick
        i = 0
        while i < len(task_list):
            if task_list[i].get_arrival_time() == tick:
                arriving_task = task_list.pop(i)
                print(f"Tick {tick}: {arriving_task} arrives")
                ready_queue.enqueue(arriving_task)
            else:
                i += 1

        # are we loading new task?
        if active_task is None and not ready_queue.is_empty():
            active_task = ready_queue.dequeue()
            print(f"Tick {tick}: {active_task} enters CPU")
            remaining_quantum = time_quantum

        if active_task is not None:
            active_task.do_work()
            remaining_quantum -= 1
            if active_task.is_done():
                print(f"Tick {tick}: {active_task} completes")
                active_task = None
            elif remaining_quantum == 0:
                print(f"Tick {tick}: {active_task} completes its quantum")
                ready_queue.enqueue(active_task)
                active_task = None

        tick += 1
          

if __name__ == "__main__":

    tasks = []
    tasks.append(Task(100,0))
    tasks.append(Task(15,15))
    tasks.append(Task(100,16))
    simulate(tasks,10)
