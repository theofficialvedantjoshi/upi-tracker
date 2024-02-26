from __future__ import print_function
import os.path
import re
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from tqdm import tqdm
import tabulate

def isemail(email):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    else:
        return False
def fetch(num):
    bank = input("Enter bank alerts email: ")
    if not isemail(bank):
        print("Invalid email")
        return
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    df = pd.DataFrame(columns=['Amount','Date'])
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        amounts = []
        dates = []
        transaction_ids = []
        service = build('gmail', 'v1', credentials=creds)
        l_list = service.users().messages().list(userId='me',q=("from:{}".format(bank))).execute()
        ids=[]  
        for i in l_list.get('messages'):
            ids.append(i.get('id'))
        n = num
        #getting message ids and email bodies and adding that to our lists.
        for i in tqdm(range(0, n), desc="Fetching Records"):
            request = service.users().messages().get(userId='me',id=ids[i],)
            request.execute()
            transaction = str(request.execute().get('snippet'))
            #print("Computing transaction ",i+1," of ",n,'...\n')
            try:
                amounts.append(float(re.findall(r'Rs.[0-9]*[.]?[0-9]+',transaction)[0].strip('Rs.')))
                dates.append(re.findall(r"\d{2}[-]\d{2}[-]\d{2}",transaction)[0])
                #word that starts with VPA
                transaction_ids.append(''.join(transaction.split('VPA')[1]).split(' ')[1])
            except:
                continue
        path = "records.xlsx"
        #creating dataframe.
        df['Amount'] = amounts
        df['Date'] = dates
        df['ids'] = transaction_ids
        df.set_index('Date', inplace=True)
        #writing to excel file.
        with pd.ExcelWriter(path) as writer:
            df.to_excel(writer, sheet_name="BANK RECORDS", index=True)
        #print("Records computed.")

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')
def daywise():
    df = pd.read_excel('records.xlsx', sheet_name='BANK RECORDS')
    df.drop('ids',axis=1,inplace=True)
    daywise = df.groupby('Date').sum()
    daywise.to_excel('daywise.xlsx')
def stats():
    df = pd.read_excel('records.xlsx', sheet_name='BANK RECORDS')
    inf = df.describe()
    inf.to_excel('info.xlsx')
    print(tabulate.tabulate(inf, headers='keys', tablefmt='psql'))
    print("\n")


def tag():
    df = pd.read_excel('records.xlsx', sheet_name='BANK RECORDS')
    l= []
    print("Unique ids found were: ",', '.join(df['ids'].unique()))
    for i in df['ids'].unique():
        l.append(df['Amount'][df['ids']==i].to_list())
    print("Add tags or type 'na' for no tag: \n")
    tags = []
    for i in range(len(l)):
        print("List of Amounts spent",l[i],end=': \n')
        tags.append(input())
        if tags[i] == 'na':
            tags[i] = df['ids'].unique()[i] 
    tf = pd.DataFrame(columns=['ids','tags'])
    tf['ids'] = df['ids'].unique()
    tf['tags'] = tags
    tf.to_excel('tags.xlsx')
def tag_amounts():
    try:
        df = pd.read_excel('records.xlsx', sheet_name='BANK RECORDS')
        tf = pd.read_excel('tags.xlsx')
        amounts = []
        for i in tf['ids']:
            amounts.append(df['Amount'][df['ids']==i].sum())
        tf['Amounts'] = amounts
        tf.to_excel('tag_amounts.xlsx',index=False)
    except:
        print("Tags not found.")
        return
def menu():
    print("UPI Transaction Analyzer\n")
    print("1. Fetch Records\n")
    print("2. Fetch daywise records\n")
    print("3. View statistics\n")
    print("4. Tag transactions\n")
    print("5. View Amounts by tags\n")
    print("6. Exit\n")
    choice = input("Enter your choice: ")
    if choice == '1':
        num = int(input("Enter the number of records to fetch: \n"))
        fetch(num)
        menu()
    elif choice == '2':
        daywise()
        menu()
    elif choice == '3':
        stats()
        menu()
    elif choice == '4':
        tag()
        menu()
    elif choice == '5':
        tag_amounts()
        menu()
    elif choice == '6':
        print("Exiting...")
        exit()
    else:
        print("Invalid choice")
        menu()
menu()