import random
import csv

def generate_data(num_samples=1000):
    random.seed(42)
    
    headers = ['CGPA', 'Attendance', 'Aptitude_Score', 'Coding_Score', 'Communication_Score', 'Number_of_Projects', 'Placed', 'Salary']
    data = []
    
    for _ in range(num_samples):
        # Generate features
        cgpa = round(random.gauss(7.5, 1.2), 2)
        cgpa = max(4.0, min(10.0, cgpa))
        
        attendance = round(random.gauss(80, 10), 1)
        attendance = max(40.0, min(100.0, attendance))
        
        aptitude_score = round(random.gauss(65, 15), 1)
        aptitude_score = max(0.0, min(100.0, aptitude_score))
        
        coding_score = round(random.gauss(60, 20), 1)
        coding_score = max(0.0, min(100.0, coding_score))
        
        communication_score = round(random.gauss(70, 15), 1)
        communication_score = max(0.0, min(100.0, communication_score))
        
        num_projects = random.randint(0, 5)
        
        # Calculate a hidden score to determine placement and salary
        score = (
            cgpa * 0.3 +
            (attendance / 10) * 0.1 +
            (aptitude_score / 10) * 0.15 +
            (coding_score / 10) * 0.25 +
            (communication_score / 10) * 0.1 +
            num_projects * 0.1
        )
        score += random.gauss(0, 0.5)
        
        data.append([cgpa, attendance, aptitude_score, coding_score, communication_score, num_projects, score])

    # Find the threshold (top 60% placed)
    scores = [row[-1] for row in data]
    scores.sort()
    threshold = scores[int(len(scores) * 0.4)]
    
    final_data = []
    for row in data:
        score = row.pop()
        placed = 1 if score > threshold else 0
        
        if placed == 1:
            salary = 300000 + (score - threshold) * 100000
            salary += random.gauss(0, 50000)
            salary = round(salary / 10000) * 10000
            if salary < 200000:
                salary = 200000
        else:
            salary = 0
            
        row.extend([placed, salary])
        final_data.append(row)

    with open('data/dataset.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(final_data)

    print("Dataset successfully generated at data/dataset.csv")

if __name__ == "__main__":
    generate_data(1000)
