import subprocess

def main():

    fetch_process = subprocess.run(["python", "fetch.py"], capture_output=True, text=True)
    if fetch_process.returncode == 0:
        print("fetch.py executed successfully.")
    else:
        print("Error in fetch.py:")
        print(fetch_process.stderr)
        return  

   
    parse_process = subprocess.run(["python", "parse.py"], capture_output=True, text=True)
    if parse_process.returncode == 0:
        print("parse.py executed successfully.")
    else:
        print("Error in parse.py:")
        print(parse_process.stderr)

if __name__ == "__main__":
    main()
