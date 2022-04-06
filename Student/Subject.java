package Student;

public class Subject {
    
    private String subjectID;
    private String name;
    private double load;

    public Subject(String subjectID, String name, double load) {

        this.subjectID = subjectID;
        this.name = name;
        this.load = load;
    }

    public String getSubjectID() {
        return this.subjectID;
    }
}
