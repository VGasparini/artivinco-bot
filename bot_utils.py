from datetime import datetime, timedelta
import csv

def read_token():
        return open("token", "r").read()

def correct_date(date):
        d = datetime.strptime(date,'%d/%m/%Y %H:%M')
        d-= timedelta(seconds=3600)
        return d.strftime("%d/%m/%Y %H:%M") 

def now_date():
        return datetime.now().strftime("%d/%m/%Y %H:%M")

def convert_to_string(instance):
        s = ''
        s += ('\nCliente: ' + instance['cliente'] +
                '\nReferência: ' + instance['ref'] +
                '\nPedido: ' + instance['pedido'] +
                '\nNº NF: ' + instance['nf'] +
                '\nQuantidade Faturada: ' + instance['qtd'] +
                '\nData faturamento: ' + instance['nfdate'] + '\n')
        return s


def verify_attr(attr, seek, data):
        to_return = ''
        for instance in data:
                if len(seek) > 5:
                        if seek in instance[attr]:
                                to_return += convert_to_string(instance)
        if to_return:
                return to_return
        return 'Informação inválida'

