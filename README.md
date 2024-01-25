
This Script monitor any new file created in the User's drive, and if it's in a publicly accessible folder, the script will change its permissions to private

 
**Permissions:**

 - This app requires "https://www.googleapis.com/auth/drive" permissions
   scope in order to modify the files permissions.
 - To authenticate, create your own OAuth 2.0 Client ID in https://console.cloud.google.com/apis/credentials and download to {repo}/credentials.json
   
 
**Usage**: drive_public.py [-h] [--existing] [--wait]

 - To check and modify public permissions for existing files in the drive, use --existing True (default is False)
 - default wait time between scans is 1 minute, modify by using --wait

**Output Example:**

	![example](https://github.com/lior-le/Drive-Task/blob/main/examples/example.png) 

**Notes:**

- This will find new files with fully public permissions, but there could be other files with very permissive policies that the script will miss.
- There are no oAuth scopes that allows the app to change permissions without getting access to the files content.
- I couldn't find a way to retrieve the default sharing settings of files in the google account. from what I've gathered, it might be possible in Google Workspace environments.
