#!/usr/bin/python3

import sys, getopt
import csv
import os.path
import re
from datetime import date

def main(mfile):
	file_input = mfile
	file_output = file_input[:-4]+"_output.csv"

	if os.path.isfile(file_output):
		os.remove(file_output)

	payee_dictionary={}
	payee_dictionary_csv="payee_dictionary_csv.csv"

	extrato_output=open(file_output, "w+")

	fromCSV(payee_dictionary, payee_dictionary_csv)

	extrato_output.write("Date,Payee,Category,Memo,Outflow,Inflow\n")

	with open(file_input, encoding="ISO-8859-1") as fp:
		for line in fp:
			data_array = re.split("[;\t]+", line.rstrip())

			transaction_date = data_array[0]

			if transaction_date.count("/") == 1:
				transaction_date = transaction_date.strip() + "/" + str(date.today().year)

			value = float(data_array[2].replace(",",".").strip())
			if value > 0 and line.count(";") > 0:
				inflow = str(value)
				outflow = ""
			else:
				inflow = ""
				outflow = str(value).replace("-","")

			memo = data_array[1].strip()
			payee = memo

			if "RSHOP-" in memo:
				rshop_memo = memo.split("-")
				payee = rshop_memo[1].strip()
				transaction_date = rshop_memo[len(rshop_memo)-1] + transaction_date[5:]

			if payee in payee_dictionary:
				if not payee_dictionary[payee]:
					input_payee = input('Enter payee name for [' + memo + " - $ " + str(value) + ']:')
					payee_dictionary[payee] = input_payee
					payee = input_payee
				else:
					payee = payee_dictionary[payee]
			else:
				input_payee = input('Enter payee name for [' + memo + " - $ " + str(value) + ']:')
				payee_dictionary[payee] = input_payee
				payee = input_payee

			category = ''

			extrato_output.write(transaction_date + "," + payee + "," + category + "," + memo + "," + outflow + "," + inflow + "\n")

	extrato_output.close()
	toCSV(payee_dictionary, payee_dictionary_csv)

	print("File generated:", file_output)

	os.remove(mfile)

	print("File", mfile, "removed")



def run(argv):
	if len(argv) != 2:
		print("usage: ynab_prepare.py <file>")
		sys.exit(2)
	return argv[1]

def toCSV(dic, name):
	file=open(name, "w")
	w = csv.writer(file)
	for key, val in dic.items():
		w.writerow([key, val])
	file.close()

def fromCSV(dic, name):
	if not os.path.isfile(name):
		file=open(name, "w")
		file.close()

	file=open(name, "r")
	for key, val in csv.reader(file):
		dic[key] = val
	file.close()

if __name__ == "__main__":
	mfile=run(sys.argv)
	main(mfile)
