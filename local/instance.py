import utils

class Instance:
    def __init__(self, data):
        self.data = dict()
        self.fields = [
            "Cliente",
            "Data",
            "Referência",
            "Pedido",
            "Qtde",
            "Status",
            "Faturamento",
            "Qtde Expedição",
        ]
        self.rep = utils.REP_TO_ID[data["Representante"]] if data["Representante"] in utils.REP_TO_ID else data["Representante"]
        for field in self.fields:
            self.data[field] = ""
        for field in data:
            try:
                if field == "StatusAtual":
                    self.data["Qtde Expedição"] = int(float(data["StatusAtual"]))
                elif field == "Qtde":
                    self.data[field] = int(float(data["Qtde"]))
                elif field in self.fields:
                    self.data[field] = data[field]
                elif field == None:
                    self.data["Faturamento"] = self.parse_nf(data[field][0]) if data[field][0] != "" else ""
                    self.data["Status"] = data[field][1].replace('\n\t  ','').replace('    ','')
            except:
                continue

    def __str__(self):
        ret = ""
        to_show = ['Cliente', 'Data', 'Referência','Pedido', 'Qtde', 'Status','Faturamento', 'Qtde Expedição']
        for field in to_show:
            if self.data[field] != '':
                if field == "Faturamento":
                    ret += "\n---Faturamento---\n{}-----------------\n".format(self.data[field])
                elif field == "Qtde":
                    ret += "Qtde Pedido: {}\n".format(self.data[field])
                else:
                    ret += "{}: {}\n".format(field,self.data[field])
        return ret

    def __hash__(self):
        h = ""
        for field in self.data.keys():
            h += self.data[field]
        return h

    def __eq__(self, value):
        return self.data == value.data

    def parse_nf(self, data):
        ret = ""
        data = data.replace("- EPP ", "").replace("- ME ","").replace(", ,",",").replace(", "," - ").split(" - ")
        for i in range(0, len(data), 5):
            ret += "\n".join([data[i], data[i + 2], data[i + 4],"\n" ])
        return ret
    
    def auth(self, info):
        if info == self.rep or info == 1066700692:
            return True
        return False