import csv

dataset1=[]
dataset2=[]

with open ('final.csv', 'r') as f:
    reader= csv.reader(f)
    for row in reader :
        dataset1.append(row)
    
with open ('data2sorted.csv', 'r') as f:
    reader= csv.reader(f)
    for row in reader :
        dataset2.append(row)
    
headers1 = dataset1[0]
planetdata1= dataset1[1:]

headers2 = dataset2[0]
planetdata2= dataset2[1:]

headers=headers1+headers2

planetdata=[]
for index, datarow in enumerate(planetdata1):
    planetdata.append(planetdata1[index]+planetdata2[index])

with open ('merged_data.csv', 'a+') as f:
    writter= csv.writer(f)
    writter.writerow(headers)
    writter.writerows(planetdata)



