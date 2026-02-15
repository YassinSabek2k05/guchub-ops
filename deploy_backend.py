#!/usr/bin/env python3
import subprocess
import paramiko
import os

def upload_and_verify(ip, username, local_file, remote_path,password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    key_path = os.path.expanduser("~/.ssh/id_ed25519")

    try:
        print(f"Connecting to {ip}...")
        my_key = paramiko.Ed25519Key.from_private_key_file(key_path)
        client.connect(ip, username=username, pkey=my_key,password=password)

        print(f"Uploading {local_file} to {remote_path}...")
        sftp = client.open_sftp()
        sftp.put(local_file, remote_path)
        sftp.close()
        print("Upload successful!")

        stdin, stdout, stderr = client.exec_command(f"ls -l {remote_path}")
        print(f"Server Verification:\n{stdout.read().decode()}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        client.close()

def build(path):
    cmd = f"cd {path} && mvn clean package"
    with subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1  # Line buffered
    ) as process:
        for line in process.stdout:
            print(line, end='', flush=True)

    if process.returncode != 0:
        print(f"\nBuild Failed with exit code {process.returncode}")
        return False
    return True
def restart_backend_service(host,user,pw):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=user, password=pw)

        # Use -S to read password from stdin
        command = "sudo -S systemctl restart guchub-springboot"
        stdin, stdout, stderr = client.exec_command(command)

        # Write password to stdin and flush
        stdin.write(pw + '\n')
        stdin.flush()

        # Read the streams ONCE and store them
        out_msg = stdout.read().decode()
        err_msg = stderr.read().decode()

        # sudo -S usually prints the password prompt to stderr, we can ignore that specific line
        if err_msg and "[sudo] password for" not in err_msg:
            print(f"Error restarting service:\n{err_msg}")
        else:
            print("Service restarted successfully (or no output returned).")
            if out_msg: print(out_msg)

    except Exception as e:
        print(f"Connection failed: {e}")
    finally:
        client.close()

def main():
    password= input("Enter password:")
    springboot_path = os.getenv("SPRINGBOOT_PATH")
    final_name = os.getenv("FINAL_NAME")
    remote_path = os.getenv("REMOTE_PATH") + final_name
    host = os.getenv("HOST")
    user = os.getenv("USER")
    print(springboot_path,final_name,remote_path)
    print("Building...")
    if build(springboot_path):
        print("Build Successful!")
        print("uploading")
        try:
            if upload_and_verify(host, user, springboot_path+"/target/"+final_name, remote_path,password):
                restart_backend_service(host,user,password)
                print("Upload Successful!")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()