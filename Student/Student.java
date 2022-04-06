package Student;

import java.util.ArrayList;

public class Student extends Person {
    
    private String studentID;

    private ArrayList<Subject> subjects = new ArrayList<>();

    public Student(String name, int age, String studentID) {

        super(name, age);

        this.studentID = studentID;
    }

    public String getStudentID() {
        return this.studentID;
    }

    public ArrayList<Subject> getSubjects() {
        return this.subjects;
    }
}
