import csv


def loadtsvfile(s):
    info=[]
    with open(s) as tsvfile:
        reader = csv.reader(tsvfile,delimiter='\t')
        for row in reader:
            info.append(row)
        info = [[1] + list(map(float, obs)) for obs in info]
        X = [obs[:-1] for obs in info]
        y = [obs[-1] for obs in info]
        return X, y
        
if __name__ == "__main__":
    X,y = loadtsvfile('salammbo/salammbo_a_en.tsv')

    print(y)