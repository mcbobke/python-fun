#!/usr/bin/env python3
import pathlib
import requests
import sys
import tabulate

base_url = 'https://api.youneedabudget.com/v1'

def get_apikey() -> str:
    '''
    Gets the API key for YNAB, either from an expected file location or from standard input.
    '''
    expected_path = pathlib.Path(pathlib.Path.home(), 'ynabkey')
    if expected_path.exists():
        with open(expected_path) as ynabkeyfile:
            api_key = ynabkeyfile.readline()
    else:
        api_key = input('Enter your API key: ')
    return api_key

def get_budgets(headers: dict) -> list:
    '''
    Gets all budgets under a YNAB account.
    '''
    budgets_url = "{0}/budgets".format(base_url)
    try:
        response = requests.get(budgets_url, headers=headers)
        response.raise_for_status()
        return response.json()['data']['budgets']
    except requests.HTTPError as err:
        print("An error occurred while requesting your budgets: [{0}]".format(err))
        sys.exit()

def get_accounts(headers: dict, budgets: list) -> list:
    '''
    Gets all accounts under each budget.
    '''
    accounts = []
    for budget in budgets:
        accounts_url = "{0}/budgets/{1}/accounts".format(base_url, budget['id'])
        try:
            response = requests.get(accounts_url, headers=headers)
            response.raise_for_status()
            accounts.append(response.json()['data']['accounts'])
        except requests.HTTPError as err:
            print("An error occurred while requesting your accounts: [{0}]".format(err))
            sys.exit()
    
    return accounts

if __name__ == '__main__':
    api_key = get_apikey()
    print()
    headers = {
        'Authorization' : "Bearer {0}".format(api_key)
    }

    allbudgets = get_budgets(headers)
    allaccounts = get_accounts(headers, allbudgets)

    count = 0
    while count < len(allbudgets):
        accountdata = []
        for account in allaccounts[count]:
            balance = account['balance'] / 1000
            accountdata.append((account['name'], balance))
        print(allbudgets[count]['name'])
        print(tabulate.tabulate(accountdata, headers=['Account Name', 'Balance'], tablefmt='pretty'))
        print()
        count += 1