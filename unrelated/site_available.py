import os
import time

import requests

def check_website(url):
  response = requests.get(url)
  return response.status_code

if __name__ == "__main__":
    return_code = None
    website = "https://google.com"

    while return_code != 200:
        return_code = check_website(website)
        print(f"The return code for {website} is {return_code}")
        time.sleep(5)



