from model.model import Model

myModel=Model()
myModel.buildGraph(7.4, 7.8)
n,a=myModel.getGraphDetails()
print("Numero di nodi:", n)
print("Numero di archi:", a)