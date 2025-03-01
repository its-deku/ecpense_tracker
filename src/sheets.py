from googleapiclient.discovery import build

row = 7


class SheetsApi:

    @staticmethod
    def add_entry(creds, sheet_id, transactions):
        global row
        service = build("sheets", "v4", credentials=creds)
        end_row = row + len(transactions) - 1
        range_names = f"E{row}:G{end_row}"

        body = {"values": transactions}
        result = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=sheet_id,
                range=range_names,
                valueInputOption="RAW",
                body=body
            )
            .execute()
        )
