import matplotlib.pyplot as plt

def load_students(filepath):
    students = {}
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            student_id = ''.join(filter(str.isdigit, line[:3]))
            name = line[3:]
            students[name] = student_id
    return students

def load_assignments(filepath):
    assignments = {}
    with open(filepath, "r") as f:
        lines = f.read().splitlines()
        for i in range(0, len(lines), 3):
            name = lines[i].strip()
            aid = lines[i+1].strip()
            points = int(lines[i+2].strip())
            assignments[name] = {"id": aid, "points": points}
    return assignments

def load_submissions(folder_path):
    import os
    submissions = {}
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        with open(filepath, "r") as f:
            for line in f:
                sid, aid, percent = line.strip().split("|")
                key = (sid, aid)
                submissions[key] = float(percent)
    return submissions


def student_grade(students, assignments, submissions):
    name = input("What is the student's name: ")
    if name not in students:
        print("Student not found")
        return
    sid = students[name]
    total_score = 0
    for aname, adata in assignments.items():
        aid = adata["id"]
        points = adata["points"]
        score = submissions.get((sid, aid), 0)
        total_score += score / 100 * points
    grade = round(total_score / 1000 * 100)
    print(f"{grade}%")

def assignment_stats(assignments, submissions):
    name = input("What is the assignment name: ")
    if name not in assignments:
        print("Assignment not found")
        return
    aid = assignments[name]["id"]
    scores = [v for (sid, aid_), v in submissions.items() if aid_ == aid]
    if not scores:
        print("Assignment not found")
        return
    print(f"Min: {int(min(scores))}%")
    print(f"Avg: {int(sum(scores)/len(scores))}%")
    print(f"Max: {int(max(scores))}%")



def assignment_graph(assignments, submissions):
    name = input("What is the assignment name: ")
    if name not in assignments:
        print("Assignment not found")
        return

    aid = str(assignments[name]["id"])
    scores = [v for (sid, aid_), v in submissions.items() if str(aid_) == aid]

    if not scores:
        print("No scores found for this assignment.")
        return

    # plt.hist(scores, bins=10)  # 또는 bins=[50, 55, 60, ..., 95, 100]
    plt.hist(scores, bins=[50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100])
    plt.title(f"Histogram for {name}")
    plt.xlabel("Percentage")
    plt.ylabel("Number of Students")
    plt.grid(True)
    plt.show()



def main():
    students = load_students("./data/students.txt")
    assignments = load_assignments("./data/assignments.txt")
    submissions = load_submissions("./data/submissions")

    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    choice = input("Enter your selection: ")

    if choice == "1":
        student_grade(students, assignments, submissions)
    elif choice == "2":
        assignment_stats(assignments, submissions)
    elif choice == "3":
        assignment_graph(assignments, submissions)


if __name__ == "__main__":
    main()