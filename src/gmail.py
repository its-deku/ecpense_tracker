import datetime
from googleapiclient.discovery import build


class GmailApi:

    @staticmethod
    def extract(mails):
        indices = []

        # for mail in mails:

        transactions = [("", "", "")]  # (date, to, amount)
        date_today = str(datetime.date.today())
        ind = -1
        for i in range(len(mails)):
            try:
                i1 = mails[i].index("VPA")
                i2 = mails[i].index("on")
            except ValueError:
                continue
            ind += 1
            indices.append((i1, i2))
            # preprocess the dates to match date time format of datetime module
            tmp = (mails[i][indices[ind][1] + 1][:6] + str(datetime.date.today().year)).split("-")
            tmp[0], tmp[2] = tmp[2], tmp[0]
            transaction_date = "-".join(tmp)
            # check today's date with the transaction date
            if transaction_date == date_today:
                amount = int(float(mails[i][2][3:]))
                i1, i2 = indices[ind][0], indices[ind][1]
                to = " ".join(mails[i][i1 + 1: i1 + (i2 - i1)])
                transactions.append([transaction_date, to, amount])

        return transactions

    @staticmethod
    def get_transactions(creds):
        # Call the Gmail API
        # / gmail / v1 / users / {userId} / messages / {id}
        service = build("gmail", "v1", credentials=creds)
        # fetch 10 mails so to cover more than enough for daily transactions allowed from UPI
        results = service.users().messages().list(userId="me", maxResults=20, q="from:alerts@hdfcbank.net").execute()

        # extract the message ids to get the content of mail later using those ids
        message_ids = []
        for msg in results['messages']:
            message_ids.append(msg['id'])

        # store the mail contents into a list for further processing
        mails = []
        for msg_id in message_ids:
            entire_msg = service.users().messages().get(userId="me", id=msg_id).execute()
            mails.append(entire_msg['snippet'].split(" "))

        return GmailApi.extract(mails)
