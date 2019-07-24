import csv

with open('report1542574860732.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    data = [[] for _ in range(7)]
    for row in csv_reader:
        data[0].append(row["Código Representante"])
        data[1].append(row["Cliente"])
        data[2].append(row["Data de Entrega"])
        data[3].append(row["Pedido"])
        data[4].append(row["Produto"])
        data[5].append(row["Status"])
        data[6].append(True)
    

def str_pedido(data_pedido):
        st = ''
        for i in range(len(data)):
                if data[2][i] == data_pedido:
                        st += ("\nCliente " + data[1][i] + '\n'+"Pedido " + data[3][i] +
                               '\n'+"Produto " + data[4][i] + '\n'+"Status " + data[5][i] + '\n')
        return st
    
print(str_pedido(input()))



