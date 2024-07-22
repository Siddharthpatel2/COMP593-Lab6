import os
import requests
import hashlib
import subprocess

def main():
    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()

    # Download VLC installer from the VLC website
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer
    if installer_data and installer_ok(installer_data, expected_sha256):
        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)

        # Run the VLC installer silently
        run_installer(installer_path)

        # Deleting the VLC installer from disk
        delete_installer(installer_path)

def get_expected_sha256():
    """retrieves the expected SHA-256 value from the text file that is downloaded from the videolan.org website and contains the required SHA-256 value for the VLC installer file.
    Returns:
        str: Expected SHA-256 hash value of VLC installer
    """
    #TO DO:Step 1
    # Send GET request to download the file
    file_url = 'https://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe.sha256'
    resp_msg = requests.get(file_url)
    
    # Check whether the download was successful
    if resp_msg.status_code == requests.codes.ok:
        # Extract text file content from response message
        file_content = resp_msg.text
        
        # Save the text file to disk
        with open(r'C:\temp\sha_code.txt', 'w') as file:
            file.write(file_content)
        
        # Extract SHA-256 value from the content
        sha = file_content.split(' ')
        shacode = sha[0]
        return shacode
    else:
        print(f"Failed to retrieve SHA-256 value: {resp_msg.status_code} ({resp_msg.reason})")
        return None

def download_installer():
    """Downloads, but does not save, the .exe VLC installer file for 64-bit Windows.

    Returns:
        bytes: VLC installer file binary data
    """
    #TO DO:Step 2
    # Send GET message to download the file
    file_url = 'https://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe'
    resp_msg = requests.get(file_url)
    
    # Check whether the download was successful
    if resp_msg.status_code == requests.codes.ok:
        # Extract binary file content from response message
        file_content = resp_msg.content
        return file_content
    else:
        print(f"Failed to download VLC installer: {resp_msg.status_code} ({resp_msg.reason})")
        return None

def installer_ok(installer_data, expected_sha256):
    """Verifies the integrity of the downloaded VLC installer file by calculating its SHA-256 hash value 
    and comparing it against the expected SHA-256 hash value. 

    Args:
        installer_data (bytes): VLC installer file binary data
        expected_sha256 (str): Expected SHA-256 of the VLC installer

    Returns:
        bool: True if SHA-256 of VLC installer matches expected SHA-256. False if not.
    """    
    # Calculate SHA-256 hash value of installer data
    installer_hash = hashlib.sha256(installer_data).hexdigest()
    #TO DO:Step 3
    # Compare with expected SHA-256 value
    if installer_hash == expected_sha256:
        return True
    else:
        return False

def save_installer(installer_data):
    """Saves the VLC installer to a local directory.

    Args:
        installer_data (bytes): VLC installer file binary data

    Returns:
        str: Full path of the saved VLC installer file
    """
    #TO DO:Step 4
    # Save the binary file to disk
    download_path = r'C:\users\vlc.exe'
    with open(download_path, 'wb') as file:
        file.write(installer_data)    
    return download_path

def run_installer(installer_path):
    """Silently runs the VLC installer.

    Args:
        installer_path (str): Full path of the VLC installer file
    """    
    # Run the installer silently
    #TO DO:Step 5
    subprocess.run([installer_path, '/L=1033', '/S'], shell=True)

def delete_installer(installer_path):
    #TO DO:Step 6
    """Deletes the VLC installer file.

    Args:
        installer_path (str): Full path of the VLC installer file
    """
    # Delete the installer from disk
    os.remove(installer_path)

if __name__ == '__main__':
    main()