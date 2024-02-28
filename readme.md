# UPI Tracker

Python terminal based automation project to scrape upi transactions from Gmail using the Google API and providing analysis in excel.

Features:

    -See bank expense records with date and upi ids.
    -See Daywise brekup of the money spent.
    -See the statistical analysis of the records.
    -Tag upi ids based on past expenditure.
    -See total spending on outlets tagged.
    -Add general catergories to you expenditure.
    -All data returned in xlsx format
    -Uses Gmail API.

### Quick Start

A credentials.json files is required to access the Gmail API.

Visit https://developers.google.com/gmail/api/quickstart/python and follow the steps.

In the Google Cloud console, enable the Gmail API.Configure the OAuth consent screen.Create dredentials.

Download the credentials.json file and place it in the directory of the project.

When the app is run for the first time it will prompt you to sign through your google account.
