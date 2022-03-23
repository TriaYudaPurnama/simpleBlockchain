#!/usr/bin/env python3
import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
from application import *

from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from bigchaindb_driver.exceptions import BigchaindbException
from time import sleep
from sys import exit

import xlrd
import re
import sha3
import rethinkdb as r
import base58
import time
from cryptoconditions import Ed25519Sha256

import requests
from flask import Flask, jsonify, request


class Blockchain:


    def __init__(self):
        self.conn = r.connect(host='localhost',port = 28015, db = 'bigchain_4')
        self.bdb_root_url = 'http://localhost:9984'
        self.bdb = BigchainDB(self.bdb_root_url)
        self.costarray = [[0 for x in range(1766)] for y in range(2)]
        self.account = generate_keypair()
        self.signed_amount_tx = None

    def add_identity_assets(self):
        """
        Add a new node to the list of nodes

        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """
        ExcelAccountFileName= '/home/tria/aplikasiTA/test_bigchaindb/account.xls'
        workbookAccount = xlrd.open_workbook(ExcelAccountFileName)
        worksheetAccount = workbookAccount.sheet_by_name("Sheet1") # We need to read the data 
        #from the Excel sheet named "Sheet1"
        num_rows = worksheetAccount.nrows #Number of Rows
        num_cols = worksheetAccount.ncols #Number of Columns

        row_it = 1

        while row_it <2 :
             start = time.time()
             name = worksheetAccount.cell_value(0+row_it, 0)
             nik = worksheetAccount.cell_value(0+row_it, 1)
             address = worksheetAccount.cell_value(0+row_it, 2)
             
             tx = self.bdb.transactions.prepare(
                 operation='CREATE',
                 signers=self.account.public_key,
                 asset={'data':{'nik': str(nik),'name': name,'address': address,'pub_key': self.account.public_key,'priv_key': self.account.private_key}})
                    
             signed_tx = self.bdb.transactions.fulfill(tx , private_keys=self.account.private_key)
             txid = signed_tx['id']
             self.bdb.transactions.send(signed_tx)
             while self.bdb.transactions.status(txid).get('status') != 'valid':
                if self.bdb.transactions.status(txid).get('status') == 'valid':
                    end = time.time()
                    print("Execution time :",end-start)
                    break


             row_it += 1





    def add_car_assets(self):
        """
        Determine if a given blockchain is valid

        :param chain: A blockchain
        :return: True if valid, False if not
        """

        ExcelTransFileName= '/home/tria/aplikasiTA/test_bigchaindb/dataset.xls'
        workbookTransaction = xlrd.open_workbook(ExcelTransFileName)
        worksheetTransaction  = workbookTransaction.sheet_by_name("Sheet1") # We need to read the data 
        #from the Excel sheet named "Sheet1"


        data = r.table('assets').has_fields({'data' : {'pub_key': True}}).filter({'data': {'name': 'Bob'}}).pluck({'data' : 'pub_key'}).limit(1).run(self.conn)
        datainstring = str(data)
        pub_key = datainstring[97:141]
        #pub_key,noise = re.split("['-]", datasplit)
                        
        datapk = r.table('assets').has_fields({'data' : {'priv_key': True}}).filter({'data': {'name': 'Bob'}}).pluck({'data' : 'priv_key'}).limit(1).run(self.conn)
        datapkinstring = str(datapk)
        priv_key = datapkinstring[98:142]
        #priv_key,noisepk = re.split("['-]", datapksplit)


        rowTran_it = 1

        while rowTran_it <801 :
          start = time.time()
          reg_number = worksheetTransaction.cell_value(0+rowTran_it, 0)
          bpkb_number = worksheetTransaction.cell_value(0+rowTran_it, 1)
          category = worksheetTransaction.cell_value(0+rowTran_it, 2)
          merk = worksheetTransaction.cell_value(0+rowTran_it, 3)
          model = worksheetTransaction.cell_value(0+rowTran_it, 4)
          year = worksheetTransaction.cell_value(0+rowTran_it, 5)
          machine_number = worksheetTransaction.cell_value(0+rowTran_it, 6)
          body_number = worksheetTransaction.cell_value(0+rowTran_it, 7)
          type_of_fuel = worksheetTransaction.cell_value(0+rowTran_it, 8)
          color = worksheetTransaction.cell_value(0+rowTran_it, 9)

            

          tx = self.bdb.transactions.prepare(
              operation='CREATE',
              signers=str(pub_key),
              asset={'data':{'reg_number': str(reg_number),'bpkb_number': str(bpkb_number),'category': str(category),
              'merk': str(merk),'model': str(model),'year': str(year),'machine_number': str(machine_number), 'body_number': str(body_number),
              'type_of_fuel': str(type_of_fuel),'color': str(color)}})
                
          signed_tx = self.bdb.transactions.fulfill(tx , private_keys=str(priv_key))
          self.bdb.transactions.send(signed_tx)
          txid = signed_tx['id']
          end = time.time()
          print("Execution time", end - start)
          rowTran_it += 1


    def add_initial_money(self):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.

        :return: True if our chain was replaced, False if not
        """

        ExcelBalFileName= '/home/tria/aplikasiTA/test_bigchaindb/balance.xls'
        workbookBalance = xlrd.open_workbook(ExcelBalFileName)
        worksheetBalance  = workbookBalance.sheet_by_name("Sheet1") # We need to read the data from the Excel sheet named "Sheet1"


        rowBal_it = 1


        while rowBal_it <2 :
            name = worksheetBalance.cell_value(0+rowBal_it, 0)
            print(name)
            amount = worksheetBalance.cell_value(0+rowBal_it, 1)
            print(amount)

            data = r.table('assets').has_fields({'data' : {'pub_key': True}}).filter({'data': {'name': name}}).pluck({'data' : 'pub_key'}).limit(1).run(self.conn)
            datainstring = str(data)
            pub_key = datainstring[97:141]
            #pub_key,noise = re.split("['-]", datasplit)
                        
            datapk = r.table('assets').has_fields({'data' : {'priv_key': True}}).filter({'data': {'name': name}}).pluck({'data' : 'priv_key'}).limit(1).run(self.conn)
            datapkinstring = str(datapk)
            priv_key = datapkinstring[98:142]
            #priv_key,noisepk = re.split("['-]", datapksplit)
            
            tx = self.bdb.transactions.prepare(
                operation='CREATE',
                signers=str(pub_key),
                asset={'data':{'name': str(name),'amount': str(amount),'desc': 'cryptocurrentcy'}})
                
            self.signed_amount_tx = self.bdb.transactions.fulfill(tx , private_keys=str(priv_key))
            self.bdb.transactions.send(self.signed_amount_tx)
            rowBal_it += 1

    def find_asset_cost(self,reg_number):

        rowCost_it = 1
        found = False
        cost = 0

        while rowCost_it <1766  and found == False:
            if self.costarray[0][rowCost_it] == reg_number :
                found = True
                cost = self.costarray[1][rowCost_it]

            else:
                rowCost_it += 1

        return cost     

    def insert_asset_cost(self):        

        ExcelCostFileName= '/home/tria/aplikasiTA/test_bigchaindb/costlist.xls'
        workbookCost = xlrd.open_workbook(ExcelCostFileName)
        worksheetCost  = workbookCost.sheet_by_name("Sheet1") # We need to read the data from the Excel sheet named "Sheet1"
        num_rows = worksheetCost.nrows #Number of Rows
        num_cols = worksheetCost.ncols #Number of Columns
        print(num_rows,num_cols)

        rowCost_it = 1
        arrayRow_it = 0


        while rowCost_it <1766 :
            self.costarray[0][arrayRow_it] = worksheetCost.cell_value(0+rowCost_it, 0)
            self.costarray[1][arrayRow_it] = worksheetCost.cell_value(0+rowCost_it, 1)
            rowCost_it += 1
            arrayRow_it += 1

    def request_transaction(self):
        ExcelCostFileName= '/home/tria/aplikasiTA/test_bigchaindb/request_transaction.xls'
        workbookCost = xlrd.open_workbook(ExcelCostFileName)
        worksheetCost  = workbookCost.sheet_by_name("Sheet1") # We need to read the data from the Excel sheet named "Sheet1"
        num_rows = worksheetCost.nrows #Number of Rows

        rowBal_it = 1


        while rowBal_it <2 :
            start = time.time()
            address = worksheetCost.cell_value(0+rowBal_it, 0)
            reg_number = worksheetCost.cell_value(0+rowBal_it, 1)
            name = worksheetCost.cell_value(0+rowBal_it, 2)
            seller = worksheetCost.cell_value(0+rowBal_it, 3)

            print(address)
            print(reg_number)
            print(name)

            payload = {'reg_number' : str(reg_number) }

            response = requests.get(str(address),params=payload)
            cost = response.text
            cost = cost[12:14]
            cost = int(float(cost))

            print(cost)


            data = r.table('assets').has_fields({'data' : {'amount': True}}).filter({'data': {'name': name}}).pluck({'data' : 'amount'}).limit(1).run(self.conn)
            datainstring = str(data)
            amount = datainstring[96:99]
            amount = int(float(amount))
            print(amount)

            if amount >= cost:

                dataid = r.table('assets').has_fields({'data' : {'amount': True}}).filter({'data': {'name': name}}).pluck({'id'}).limit(1).run(self.conn)
                idinstring = str(dataid)
                idtx = idinstring[83:147]
                print(dataid)
                print(idtx)
                
            
                creationtx = self.bdb.transactions.retrieve(idtx)

                asset_id = creationtx['id']
                transfer_asset = {
                    'id': asset_id,
                }
                output_index = 0

                output = creationtx['outputs'][output_index]

                data = r.table('assets').has_fields({'data' : {'pub_key': True}}).filter({'data': {'name': seller}}).pluck({'data' : 'pub_key'}).limit(1).run(self.conn)
                datainstring = str(data)
                pub_key = datainstring[97:141]

                transfer_input = {
                    'fulfillment':  output['condition']['details'],
                    'fulfills': {
                        'output_index': output_index,
                        'transaction_id': creationtx['id'],
                    },
                    'owners_before': output['public_keys']

                }


                transfer_tx = self.bdb.transactions.prepare(
                    operation = 'TRANSFER',
                    asset=transfer_asset,
                    inputs=transfer_input,
                    recipients = str(pub_key)
                )

                datapk = r.table('assets').has_fields({'data' : {'priv_key': True}}).filter({'data': {'name': 'Bob'}}).pluck({'data' : 'priv_key'}).limit(1).run(self.conn)
                datapkinstring = str(datapk)
                priv_key = datapkinstring[98:142]

                signed_transfer_tx = self.bdb.transactions.fulfill(transfer_tx , private_keys=priv_key)

                sent_transfer_tx = self.bdb.transactions.send(signed_transfer_tx)


                print("Is ALice the owner?",
                    sent_transfer_tx['outputs'][0]['public_keys'][0] == pub_key)

                datapk = r.table('assets').has_fields({'data' : {'pub_key': True}}).filter({'data': {'name': 'Bob'}}).pluck({'data' : 'pub_key'}).limit(1).run(self.conn)
                datapkinstring = str(datapk)
                pub_key2 = datapkinstring[97:141]

                print("Was Bob the previous owner?",
                    signed_transfer_tx['inputs'][0]['owners_before'][0] == pub_key2)

                print("Money Transferred")

                #payload = {'reg_number' : str(reg_number), 'name': 'Bob' }
                #response = requests.get('http://192.168.43.73:5000/transfercar',params=payload)

                self.transfer_car(reg_number,'Bob')


            else :
                print("transfer error")

            end = time.time()
            print("Execution Time", end-start)
            rowBal_it += 1



    def transfer_car(self, reg_number, buyer_name):

        data = r.table('assets').has_fields({'data' : {'bpkb_number': True}}).filter({'data': {'reg_number': reg_number}}).pluck({'id'}).limit(1).run(self.conn)            
        strdata = str(data)            
        idtx = strdata[83:147]

        creationtx = self.bdb.transactions.retrieve(str(idtx))

        asset_id = creationtx['id']
        transfer_asset = {
            'id': asset_id,
        }

        output_index = 0

        output = creationtx['outputs'][output_index]

        data = r.table('assets').has_fields({'data' : {'pub_key': True}}).filter({'data': {'name': buyer_name}}).pluck({'data' : 'pub_key'}).limit(1).run(self.conn)
        datainstring = str(data)
        pub_key = datainstring[97:141]

        transfer_input = {
            'fulfillment':  output['condition']['details'],
            'fulfills': {
                'output_index': output_index,
                'transaction_id': creationtx['id'],
            },
            'owners_before': output['public_keys'],

        }

        prepared_transfer_tx  = self.bdb.transactions.prepare(
            operation = 'TRANSFER',
            asset=transfer_asset,
            inputs=transfer_input,
            recipients = str(pub_key)
        )


        datapk1 = r.table('assets').has_fields({'data' : {'priv_key': True}}).filter({'data': {'name': 'Sally'}}).pluck({'data' : 'priv_key'}).limit(1).run(self.conn)
        datapkinstring2 = str(datapk1)
        priv_key2 = datapkinstring2[98:141]
        
        fullfilled_transfer_tx = self.bdb.transactions.fulfill(prepared_transfer_tx, private_keys=str(priv_key2))

        sent_transfer_tx = self.bdb.transactions.send(fullfilled_transfer_tx)

        print("Is Bob the new owner?",
            sent_transfer_tx['outputs'][0]['public_keys'][0] == pub_key)

        datapk = r.table('assets').has_fields({'data' : {'pub_key': True}}).filter({'data': {'name': 'Sally'}}).pluck({'data' : 'pub_key'}).limit(1).run(self.conn)
        datapkinstring = str(datapk)
        pub_key2 = datapkinstring[97:141]

        print("Was Sally the previous owner?",
            fullfilled_transfer_tx['inputs'][0]['owners_before'][0] == pub_key2)

        print("Car Transferred")
