import csv

from instance import Instance
from datetime import datetime

REP_TO_ID = {
    "S01-014" : 912511604,
    "S32-004" : 835688488,
}

ID_TO_NAME = {
    912511604 : "Roberto",
    1066700692: "Paulo",
    650172463 : "Vinicius",
    835688488 : "Dilvo",
}

"""
S32-006 -> Laercio
S40-002 -> Sandra
"""

def read_token():
    return open("token", "r").read()

def download(filename, data):
    file = open(filename + ".html", "w")
    file.write(data)
    file.close()

def export_to_csv(filename, table):
    output_rows = []
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        output_row = []
        for column in columns:
            output_row.append(column.text)
        output_rows.append(output_row)
    with open(filename + '.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(output_rows)


def load_from_csv(filename):
    with open(filename + ".csv", "r") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            inst = Instance(row)
            data.append(inst)
    return data


def update_from_csv(filename, data):
    to_notify = []
    with open(filename + ".csv", "r") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            inst = Instance(row)
            idx = -1
            for i in range(len(data)):
                if data[i].data["Pedido"] == inst.data["Pedido"]:
                    idx = i
                    break
            if idx != -1:
                if (data[idx].data["Status"] != inst.data["Status"] and inst.data["Status"] in ["Entrega Parcial","Atendido"]) or (data[idx].data["Faturamento"] != inst.data["Faturamento"]) :
                    to_notify.append(inst)
                data[idx].data = inst.data
            else:
                data.append(inst)
    return data, to_notify

def query(data, q_id, q_type, q_n = 0):
    to_return = []
    if q_type == "pedido":
        for inst in data:
            if q_n == inst.data["Pedido"]:
                if inst.auth(q_id):
                    return [inst]
    elif q_type == "expedicao":
        for inst in data:
            if inst.data["Status"] == "Expedição":
                if inst.auth(q_id):
                    to_return.append(inst)
        return to_return
    elif q_type == "programado":
        for inst in data:
            if inst.data["Status"] == "Programado":
                if inst.auth(q_id):
                    to_return.append(inst)
        return to_return
    return -1
        