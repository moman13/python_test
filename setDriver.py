import os
import zipfile
from selenium import webdriver
import requests
import random

def get_chromedriver(use_proxy=False, user_agent=None,numberOfLoop=0):

    response = requests.get("https://proxy.webshare.io/api/proxy/list/",
                            headers={"Authorization": "Token 9f4c211268e13496ee85676c04870479d4a8e676"})
    result = response.json()
    data = result['results']
    select_ip = random.choice(data)
    port = select_ip['ports']['socks5']
    ip = select_ip['proxy_address']
    username = select_ip['username']
    password = select_ip['password']

    PROXY_HOST = ip  # rotating proxy
    PROXY_PORT = port
    PROXY_USER = username
    PROXY_PASS = password
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
              },
              bypassList: ["localhost"]
            }
          };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
    path = r'C:\chromedriver.exe'

    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    driver = webdriver.Chrome(path,
        chrome_options=chrome_options)
    return driver