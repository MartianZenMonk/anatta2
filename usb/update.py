import os
import sys

try:
    import httplib
except:
    import http.client as httplib

def have_internet():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False

def main():
    if have_internet():
        os.system("cd anatta && git pull")
    else:
        print("sorry no internet connection")



if __name__ == '__main__':
        main()