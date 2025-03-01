from googleapiclient.discovery import build


class DriveApi:

    @staticmethod
    def create_folder(creds):
        service = build("drive", "v3", credentials=creds)
        folder_metadata = {
            "name": "Expense Tracker",
            "mimeType": "application/vnd.google-apps.folder",
        }

        # check if the folder with same name exists create only if it does not exist
        all_files = service.files().list().execute()['files']
        for detail in all_files:
            mime_type = detail['mimeType']
            name = detail['name']
            if mime_type == "application/vnd.google-apps.folder" and name == "Expense Tracker":
                return detail['id']

        file = service.files().create(body=folder_metadata, fields="id").execute()
        return file.get("id")

    @staticmethod
    def create_sheet(creds):
        service = build("drive", "v3", credentials=creds)
        folder_id = DriveApi.create_folder(creds)
        file_metadata = {
            "name": "xpenses",
            "mimeType": "application/vnd.google-apps.spreadsheet",
            "parents": [folder_id]
        }

        # check if the file exists in the current folder, create only if it doesn't
        response = (
            service.files()
            .list(
                q="mimeType='application/vnd.google-apps.spreadsheet'",
                spaces="drive",
                fields="nextPageToken, files(id, name, parents)"
            )
            .execute()
        )

        for entry in response['files']:
            if entry['parents'][0] == folder_id and entry['name'] == file_metadata['name']:
                return entry['id']

        # file does not exist create one
        file = (
            service.files()
            .create(body=file_metadata, fields="id")
            .execute()
        )

        return file.get("id")
