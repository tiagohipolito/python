#!/usr/bin/python3

import sys
import re
from datetime import date
import os.path

input="/home/talves/Dropbox/IFTTT/SMS/sms_received.txt"
error="/home/talves/Dropbox/IFTTT/SMS/sms_error.txt"

output_credit="/home/talves/Dropbox/IFTTT/SMS/credit_output.csv"
output_debit="/home/talves/Dropbox/IFTTT/SMS/debit_output.csv"

def create_file(file, add_header):
	if os.path.isfile(file):
		add_header = False

	this_file=open(file, "a")

	if add_header:
		this_file.write("Date,Payee,Category,Memo,Outflow,Inflow\n")

	return this_file

re_c = re.compile("Compra aprovada no[seu ]*PERSON MULT MC PLAT(.*) - (.*) valor RS (\d*,\d{2}) em (\d{2}\/\d{2}(\/\d{4})*).*")
re_d = re.compile("ITAU PERSONNALITE: Cartao final 0659 COMPRA APROVADA (\d{2}\/\d{2}).* R\$ (\d*,\d{2}) Local: (.*).")

credit_file=None
debit_file=None

counter_credit = 0
counter_debit = 0

with open(input, encoding="ISO-8859-1") as fp:
		for line in fp:
			if re_c.match(line) != None:
				counter_credit+=1
				if counter_credit == 1:
					credit_file = create_file(output_credit, True)

				payee = re_c.match(line).group(2)
				value = re_c.match(line).group(3).replace(",", ".")
				data = re_c.match(line).group(4)

				credit_file.write(data + "," + payee + ",," + payee + "," + value + ",\n")
			elif re_d.match(line) != None:
				counter_debit+=1
				if counter_debit == 1:
					debit_file = create_file(output_debit, True)

				payee = re_d.match(line).group(3)
				value = re_d.match(line).group(2).replace(",", ".")
				data = re_d.match(line).group(1) + "/" + str(date.today().year)

				debit_file.write(data + ",,," + payee + "," + value + ",\n")
			else:
				error_file = create_file(error, False)

				error_file.write(line)

			
os.remove(input)


			
