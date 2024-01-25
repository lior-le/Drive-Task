<img width="936" alt="image" src="https://github.com/lior-le/Drive-Task/assets/157607302/52da56a0-50e7-42bc-b23b-d20151278d91">This Script monitor any new file created in the User's drive, and if it's in a publicly accessible folder, the script will change its permissions to private

Permissions:
	* This app requires "https://www.googleapis.com/auth/drive" permissions scope in order to modify the files permissions.
	* To authenticate, create your own json credentials and download to {repo}/credentials.json


Usage: drive_public.py [-h] [--existing] [--wait]
	* To check and modify puplic permissions for existing files in the drive, use --existing True (default is False)
	* Default wait time between scans is 1 minute, modify by using --wait.

Output example:

	![alt text](https://github.com/lior-le/Drive-Task/blob/main/examples/example.png)



Notes:
	* This script will find new files with fully public permissions, but there could be other files with very permissive policies
	* There are no oAuth scopes that allows the app to change permissions without getting access to the files content
	* I couldn't find a way to retrieve the default sharing settings of files in the google account. from what I've gathered, it might be possible in Google Workspace environments.
