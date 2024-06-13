from tabulate import tabulate

tab_data = { 
    'Course No.' : ['GEC101','GEC104','MAT051','STT101','STT125','STT125.1','PED001','NST001'],
    'Course Title' : ['Understanding Self','Mathematics in the Modern World','Calculus I','Descriptive and Inferential Statistics','Statistical Computing I (Lec)','Statistical Computing I (Lab)','Exercise Prescription and Management','CWTS 1/ROTC 1'],
    'Units' : [3,3,5,4,2,1,2,3]
}
data_Pros = pd.DataFrame(tab_data, header= "keys", tablefmt = 'grid')