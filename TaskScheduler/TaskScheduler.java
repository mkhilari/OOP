import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;

class Task {

    public String name;
    public int time;

    public boolean cancelled = false;

    public Task(String name, int time) {

        this.name = name;
        this.time = time;
    }

    public String toString() {

        return "(" + this.name + ", " + this.time + ")";
    }

    public static void main(String[] args) {

        List<Task> newTasks = new ArrayList<>(Arrays.asList(
            new Task("Run", 2), new Task("Jump", 1), 
            new Task("Drive", 3), new Task("Write", 7)));

        TaskScheduler aScheduler = new TaskScheduler();

        aScheduler.add(newTasks);
        
        aScheduler.execute();
        aScheduler.execute();
        aScheduler.cancel("Drive");
        aScheduler.executeAll();

        System.out.println(aScheduler.executedTasks);
    }
}

public class TaskScheduler {

    // Get tasks by time ascending 
    private PriorityQueue<Task> taskHeap = new PriorityQueue<>(
        (a, b) -> (a.time - b.time));
    private Map<String, Task> tasks = new HashMap<>();

    public List<Task> executedTasks = new ArrayList<>();

    public TaskScheduler() {

    }

    public void add(Task newTask) {

        this.taskHeap.add(newTask);
        this.tasks.put(newTask.name, newTask);
    }

    public void add(List<Task> newTasks) {

        for (Task newTask : newTasks) {

            this.add(newTask);
        }
    }

    public void cancel(String taskName) {

        // Cancels the task with the given task name 
        // if found 

        if (!this.tasks.containsKey(taskName)) {

            return;
        }

        this.tasks.get(taskName).cancelled = true;
    }

    public void execute() {

        // Returns the next non cancelled task 

        // Move past cancelled tasks 
        while (!this.taskHeap.isEmpty() && this.taskHeap.peek().cancelled) {

            this.taskHeap.poll();
        }

        if (this.taskHeap.isEmpty()) {

            return;
        }

        Task nextTask = this.taskHeap.poll();

        this.executedTasks.add(nextTask);
    }

    public void executeAll() {

        while (!this.taskHeap.isEmpty()) {

            this.execute();
        }
    }
}