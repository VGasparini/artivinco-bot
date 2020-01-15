from datetime import datetime, timedelta
import csv

def read_token():
        return open("token", "r").read()

def correct_date(date):
        d = datetime.strptime(date,'%d/%m/%Y %H:%M')
        d-= timedelta(hour=1)
        return d.strftime("%d/%m/%Y %H:%M") 

def now_date():
        return datetime.now().strftime("%d/%m/%Y %H:%M")

def convert_to_string(instance):
        s = ''
        s += ('\nCliente: ' + instance['cliente'] +
                '\nReferência: ' + instance['referência'] +
                '\nPedido: ' + instance['pedido'] +
                (instance['nf'].replace(', ,','\n') if instance['nf'] else instance['status']))
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

