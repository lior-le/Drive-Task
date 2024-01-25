from datetime import datetime
import time
import argparse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

OAUTH_SCOPE = ['https://www.googleapis.com/auth/drive']


def auth():
    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", OAUTH_SCOPE
        )
        creds = flow.run_local_server(port=0)
        return creds
    except FileNotFoundError:
        print("no credentials.json file found")


def get_parents(service, file):
    path = ""
    parent = file.get('parents')
    public_parent = False
    while parent:
        parent_id = parent[0]
        folder = service.files().get(fileId=parent_id, fields='id, name, parents, permissions').execute()
        for permission in folder.get('permissions'):
            # Search for permissive permissions
            if permission['type'] == 'anyone':
                public_parent = True
        folder_name = folder.get('name')
        path = f'{folder_name}/{path}'
        parent = folder.get('parents')
    return path, public_parent


def permissive_files(service, new_only=False, new_timestamp=None):
    try:
        fields = "nextPageToken, files(permissions, id , name, parents)"
        query = "'me' in owners"
        if new_only:
            query = f"'me' in owners and createdTime > '{new_timestamp}'"
        page_token = None
        items = []
        # Go over all the return pages to gat all the relevant results
        while True:
            results = service.files().list(q=query, fields=fields, pageToken=page_token).execute()
            items += results.get("files", [])
            page_token = results.get('nextPageToken')
            if not page_token:
                break
        if not items:
            return
        for item in items:
            path, public_parent = get_parents(service, item)
            print(f"found {item.get('name')} at {path}:")
            for permission in item.get('permissions'):
                # Search for permissive permissions
                if permission['type'] == 'anyone':
                    fid = item.get('id')
                    pid = permission['id']
                    if public_parent:
                        try:
                            service.permissions().delete(fileId=fid, permissionId=pid).execute()
                            print("+ public permissions found and removed")
                        except HttpError as error:
                            print(f"- failed to remove public permissions. error: {error}")
                    else:
                        print(f"+ public permissions found, and were not removed")
                    break
                else:
                    print(f"+ no public permissions found")

    except HttpError as error:
        print(f"An error occurred: {error}")


def main():
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--wait", help="wait time in minutes")
    parser.add_argument("--existing", help="if True, permission will be checked for existing files in drive"
                        , choices=["True", "False"], default="False")
    args = parser.parse_args()
    # get user's credentials
    credentials = auth()
    if not credentials:
        return
    service = build("drive", "v3", credentials=credentials)
    if args.existing == "True":
        print("Going over existing files:")
        permissive_files(service)
    current_time = datetime.utcnow()
    print("**monitoring new files**")
    while True:
        next_time = datetime.utcnow()
        permissive_files(service, new_only=True, new_timestamp=current_time.strftime("%Y-%m-%dT%H:%M:%S"))
        current_time = next_time
        if args.wait and str(args.wait).isnumeric():
            time.sleep(int(args.wait)*60)
        else:
            time.sleep(60)



if __name__ == "__main__":
    main()
