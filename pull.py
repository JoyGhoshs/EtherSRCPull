import requests
from bs4 import BeautifulSoup
import os
from colorama import Fore, Back, Style
import random
import argparse
import time

def EtherSourcePull(address):
    endpoint = "https://etherscan.io/address/"+address+"#code"
    agents = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)",
        "Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3",
        "Firefox/39.0 Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0",
        "Brave/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)",
        "Chrome/58.0.3029.110 Safari/537.36 OPR/45.0.2552.635",
        "Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.18",
    ]
    agent = random.choice(agents)
    headers = {
        "User-Agent": agent,
    }
    try:
        session = requests.Session()
        r = session.get(endpoint, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        body_source = BeautifulSoup(r.text, "html.parser")
        codes = body_source.find_all("div", id="dividcode")
        source_codes = codes[0].find_all("pre", class_="js-sourcecopyarea editor")
        print(f"{Fore.RED}EtherSourcePull: {Fore.RESET} Pulling {len(source_codes)} source codes from {address}")
        source_code = []
        for source in source_codes:
            source_code.append(source.text)
        filenames = codes[0].find_all("span", class_="text-muted")
        files = []
        for filename in filenames:
            name = filename.text
            if "File" in name:
                sp, name = name.split(":")
                name = name.strip()
                files.append(name)
        print(f"{Fore.RED}EtherSourcePull: {Fore.RESET} Cloning {len(files)} files from {address}")
        path = "./"+address+"/"
        if not os.path.exists(path):
            os.makedirs(path)
        for i in range(len(files)):
            try:
                file = open(path+files[i], "w")
                file.write(source_code[i])
                file.close()
            except:
                pass
        print(f"{Fore.RED}EtherSourcePull: {Fore.RESET} Finished Cloning {len(files)} files from {address}")
    except Exception as e:
        print(f"{Fore.RED} EtherSourcePull: {Fore.RESET} Error {e} occured while pulling {address}")
        pass


def main():
    print(f"""
   ______  __           ____                      ___       ____
  / __/ /_/ /  ___ ____/ __/__  __ _____________ / _ \__ __/ / /
 / _// __/ _ \/ -_) __/\ \/ _ \/ // / __/ __/ -_) ___/ // / / / 
/___/\__/_//_/\__/_/ /___/\___/\_,_/_/  \__/\__/_/   \_,_/_/_/  
                                                {Fore.RED}armx64{Fore.RESET}
          """)
    started = time.time()
    parser = argparse.ArgumentParser(description="EtherSourcePull")
    parser.add_argument("-a", "--address", help="Address to pull source code from")
    args = parser.parse_args()
    if args.address:
        EtherSourcePull(args.address)
        ended = time.time()
        took = ended - started
        print(f"{Fore.RED}EtherSourcePull: It took {took} seconds to pull source code from {args.address}")
    else:
        print(f"{Fore.RED}EtherSourcePull: {Fore.RESET} Please specify an address to pull source code from")
        exit(0)


if __name__ == "__main__":
    main()
        










    