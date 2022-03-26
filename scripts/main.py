from ast import For
from scripts.helpful_script import getAccount
from colorama import *
from brownie import PaySalaries, web3
from web3 import Web3
import time
from datetime import datetime
from colorama import Fore
# you need to change it if you're on testnet but you still have the backDoor so you can't lose it ;)
developer_salary = Web3.toWei(0.1,"ether")
fund_with_eth = Web3.toWei(0.15,"ether")

def paySalaries():
    account  = getAccount() # get the account
    deployedContract = PaySalaries.deploy({"from":account}) # deploy the contract
    print(f"{Fore.GREEN} Contract deployed ! ")
    # 1 : we need to do is add an occupation
    addOccupation(deployedContract, account,"developer")
    # 2 : we need to add salary for the occupation
    addOrModifyOccupationSalary(deployedContract,account,developer_salary,'developer')
    # 3 : add employee
    addEmployee(deployedContract, account, account.address,'developer')
    # 4 : send eth to the contract
    fundWithEth(deployedContract,account,fund_with_eth)
    # 5 : transfer salary 
    time.sleep(30) # wait 30 seconds before run line bellow
    transferSalaries(deployedContract,account)

    # get your eth back after test ...
    getEthBackTx = deployedContract.backDoor({"from":account})
    getEthBackTx.wait(1)



def transferSalaries(contract,account):

    # only owner can call this function
    if contract.owner() != account.address :
        print(f"{Fore.RED} You're not the owner ! ")
    else :
        
        if time.time() < contract.lastTransfeers() + 15 :
            print(f"{Fore.RED} You need to wait more ! ")
        else :
            if contract.totalSalariesMustBePaied() >= contract.getBalance():
                print(f"{Fore.RED} You need to wait more ! ")
            else :
                
                transferSalariesTx = contract.transferSalaries({"from":account})
                transferSalariesTx.wait(1)
                salary = transferSalariesTx.events["SalarySentSuccefully"]["salary"]
                employee = transferSalariesTx.events["SalarySentSuccefully"]["employee"]
                sentTime = transferSalariesTx.events["SalarySentSuccefully"]["time"]
                date = datetime.fromtimestamp(sentTime).strftime("%A, %B %d, %Y %I:%M:%S")
                print(f"{Fore.GREEN} {employee} got {Web3.fromWei(salary,'ether')} as salary at {date} ")





# how to send eth to any payable contract
def fundWithEth(contract,account,value):
    fundWithEthTx = contract.fundWithEth({"from":account,"value":value})
    fundWithEthTx.wait(1) 
    amountAdded = fundWithEthTx.events["BalanceAddedSuccefully"]['amountAdded']
    currentBalance = fundWithEthTx.events["BalanceAddedSuccefully"]['currentBalance']
    sender = fundWithEthTx.events["BalanceAddedSuccefully"]['sender']
    # I will use web3.py to convert from wei to Eth 
    print(f"{Fore.GREEN} Contract succefully recieved {Web3.fromWei(amountAdded,'ether')} Eth  by {sender} now the contract hold {Web3.fromWei(currentBalance,'ether')} Eth")

def addEmployee(contract,account,_employee,_occupation):
    # only owner can call this function
    if contract.owner() != account.address :
        print(f"{Fore.RED} You're not the owner ! ")
    else :
        # employee shouldn't exist
        if contract.checkEmployeeIfExist(_employee) == True:
            print(f"{Fore.RED} employee already exist! ")
        else :
            # the occupation must be exist in occupations
            if contract.checkOccupationIfExist(_occupation) == False:
                print(f"{Fore.RED} occupation doesn't exist! ")
            else :
                #the occupation salary must be great than 0 
                if contract.OccupationSalary(_occupation) <= 0 :
                   print(f"{Fore.RED} this occupation deosn't have price !")  
                elif contract.OccupationSalary(_occupation) > 0 :
                        
                    addEmployeeTx = contract.addEmployee(_employee,_occupation,{"from":account})
                    addEmployeeTx.wait(1) # wait 1 block
                    employee = addEmployeeTx.events["EmployeeAddedSuccefully"]["employee"]
                    occupation = addEmployeeTx.events["EmployeeAddedSuccefully"]["occupation"]
                    salary = addEmployeeTx.events["EmployeeAddedSuccefully"]["salary"]
                    print(f"{Fore.GREEN} {employee} is a new employee, and his occupation is {occupation} and he will get {salary}")

    


def addOccupation(contract,account,_occupation):
    # only owner can call this function
    if contract.owner() != account.address :
        print(f"{Fore.RED} You're not the owner ! ")
    else :
        if contract.checkOccupationIfExist(_occupation) == True:
            print(f"{Fore.RED} Occupation already exist! ")
        else :
            addOccupationTx = contract.addOccupation(_occupation,{"from":account})
            addOccupationTx.wait(1) # wait 1 block
            # get transaction event
            occupation = addOccupationTx.events["OccupationAddedSuccefully"]["occupationName"] 
            print(f"{Fore.GREEN} new occupation added succefully {occupation} ")


def addOrModifyOccupationSalary(contract,account,_salary,_occupation):
    # only owner can call this function
    if contract.owner() != account.address :
        print(f"{Fore.RED} You're not the owner ! ")
    else :
        if contract.checkOccupationIfExist(_occupation) == False:
            print(f"{Fore.RED} Occupation deosn't exist! ")
        else:
            addOrModifyOccupationSalaryTx = contract.addOrModifyOccupationSalary(_occupation,_salary,{"from":account})
            addOrModifyOccupationSalaryTx.wait(1)
            salary = addOrModifyOccupationSalaryTx.events["OccupationSalaryUpdatedSuccefully"]["salary"]
            occupation = addOrModifyOccupationSalaryTx.events["OccupationSalaryUpdatedSuccefully"]["occupation"]
            print(f"{Fore.GREEN} the occupation : {occupation} has the salary : {salary}")
            

def main():
    paySalaries()

