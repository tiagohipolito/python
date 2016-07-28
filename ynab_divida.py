#!/usr/bin/python3

import sys
import csv
import datetime, calendar
from decimal import *

if len(sys.argv) == 7:
    payee=sys.argv[1]
    categoria=sys.argv[2]
    descricao=sys.argv[3]
    total_parcelas=int(sys.argv[4])
    data_parcela=datetime.datetime.strptime(sys.argv[5], '%d/%m/%Y').date()
    valor=Decimal(sys.argv[6])
else:
    payee=input("Payee: ")
    categoria=input("Categoria: ")
    descricao=input("Descrição: ")
    total_parcelas=int(input("Total Parcelas: "))
    data_parcela=datetime.datetime.strptime(input("Data (dd/mm/yyyy): "), '%d/%m/%Y').date()
    valor=Decimal(input("Valor parcela: "))

def add_months(sourcedate,months):
    month = sourcedate.month - 1 + months
    year = int(sourcedate.year + month / 12 )
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return datetime.date(year,month,day)



output_file="/home/talves/Downloads/nova_divida_output.csv"
output=open(output_file, "w+")
output.write("Date,Payee,Category,Memo,Outflow,Inflow\n")

i = 0
while i < total_parcelas:
    i+=1
    if i==1:
        nova_data = data_parcela
    else:
        nova_data = add_months(nova_data, 1)

    output.write(nova_data.strftime('%d/%m/%Y') + "," + payee + "," + categoria + "," + descricao + " - Parcela " + str(i) + " de " + str(total_parcelas) + "," + str(valor) + ",\n")

output.close()
print(output_file)
