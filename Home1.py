from tabulate import tabulate

table_data = [['Semester', 'Course No.', 'Course Title', 'Units'],
             ['1', 'GEC101', 'Understanding Self', 3],
             ['1', 'GEC104', 'Mathematics in the Modern World', 3],
             ['1', 'MAT051', 'Calculus I', 5],
             ['1', 'STT101', 'Descriptive and Inferential Statistics', 4],
             ['1', 'STT125', 'Statistical Computing I (Lec)', 2],
             ['1', 'STT125.1', 'Statistical Computing I (Lab)', 1],
             ['1', 'PED001', 'Exercise Prescription and Management', 2]]

print(tabulate(table_data, headers="firstrow"))
