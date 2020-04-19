#!/usr/bin/env python3
import requests
import sys

base_url = 'https://api.youneedabudget.com/v1'

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
        return None

def get_accounts(headers: dict, budgets: list) -> list:
    '''
    Gets all accounts under each budget.
    '''
    for budget in budgets:
        accounts_url = "{0}/budgets/{1}/accounts".format(base_url, budget['id'])
    
    return None

if __name__ == '__main__':
    api_key = input('Enter your API key: ')
    headers = {
        'Authorization' : "Bearer {0}".format(api_key)
    }

    budgets = get_budgets(headers)
    if budgets is None:
        sys.exit()

    accounts = get_accounts(headers, budgets)