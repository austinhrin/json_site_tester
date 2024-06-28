# JSON Site Tester
Edit the `json\tests.json` file to meet your needs. When running the JSON Site Tester if you do not include a json file name like this `python main.py json\test.json` then it will look in the `json` folder and run all tests. By default JSON Site Tester tests both Chrome and Firefox. If you would like to test one or the other search for this line `selenium_browser = ''` and specify either `chrome` or `firefox`.

## Setup
- Install Python 3.10+
- `pip install virtualenv`
- `python -m virtualenv .venv`
- `.\.venv\Scripts\activate`
- `python -m pip install -r .\requirements.txt`
- Edit tests.json for your test scenario
- `python main.py test.json`

Currently supports the following features:
- input
- button
- wait
- execjs
- newtab
- closetab
- openurl

You can also specify success checks with `success_checks`:
- Check html element text. You can have 1 or more of the following in the same check:
    - in
    - notin
    - eq
    - noteq
- Check a cookie value. You can have 1 or more of the following in the same check:
    - in
    - notin
    - eq
    - noteq

# Known issues
- if you get an error starting with `Could not get version for google-chrome with the command:` open chrome so it can detect the version
- if getting errors opening powershell try adding `%SYSTEMROOT%\System32\WindowsPowerShell\v1.0\` to your system path
