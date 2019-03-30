from functools import reduce
import csv
import pandas as pd
import pprint

class Classifier():
    data = None
    atribut = None
    priori = {}
    cp = {}
    hipotesis = None


    def __init__(self,filename=None, atribut=None ):
        self.data = pd.read_csv(filename, sep=',', header =(0))
        self.atribut = atribut

    def calculate_priori(self):
        nilai_kelas = list(set(self.data[self.atribut]))
        data_kelas =  list(self.data[self.atribut])
        for i in nilai_kelas:
            self.priori[i]  = data_kelas.count(i)/float(len(data_kelas))
        print ("Priori Values: ", self.priori)

    def get_cp(self, attr, attr_type, class_value):
        data_attr = list(self.data[attr])
        data_kelas = list(self.data[self.atribut])
        total =1
        for i in range(0, len(data_attr)):
            if data_kelas[i] == class_value and data_attr[i] == attr_type:
                total+=1
        return total/float(data_kelas.count(class_value))


    def calculate_conditional_probabilities(self, hipotesis):
        for i in self.priori:
            self.cp[i] = {}
            for j in hipotesis:
                self.cp[i].update({ hipotesis[j]: self.get_cp(j, hipotesis[j], i)})

    def classify(self):
        hasil = [1,1]
        iterator = 0
        for i in self.cp:
            hasil[iterator] = reduce(lambda x, y: x*y, self.cp[i].values())*self.priori[i]
            iterator += 1

        if (hasil[0] > hasil[1]):
            return '>50K'
        else:
            return '<=50K'

if __name__ == "__main__":
    c = Classifier(filename="TrainsetTugas1ML.csv", atribut="income" )
    c.calculate_priori()
    
    filename = 'TestsetTugas1ML.csv'
    data = pd.read_csv(filename, sep=',', header=(0))
    predict = []
    for index, row in data.iterrows():
        c.hipotesis = {'age': row["age"], 'workclass': row["workclass"], 
        'education': row["education"], 'marital-status': row["marital-status"], 
        'occupation': row["occupation"], 'relationship': row["relationship"], 
        "hours-per-week": row["hours-per-week"]}

        c.calculate_conditional_probabilities(c.hipotesis)
        predict.append(c.classify())
    print(predict)



with open('TebakanTugas1ML.csv', 'w', newline="") as filecsv:
    w=csv.writer(filecsv)
    for j in predict:
        w.writerow([j])