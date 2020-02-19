import os

JINS_API_BASE_URL = os.environ['JINS_API_BASE_URL']

LOGIN_INFO = {
  'utf8': '✓',
  'user[email]': os.environ['JINS_USER_EMAIL'],
  'user[password]': os.environ['JINS_USER_PASSWORD'],
  'user[remember_me]': '0'
}
TOKEN = {
  'grant_type': 'authorization_code',
  'redirect_uri': JINS_API_BASE_URL,
}

GET_CODE_HEADERS = {
    "Accept-Encoding": "utf-8",
}

GET_TOKEN_HEADERS = {
  'Content-Type': 'application/x-www-form-urlencoded',
  }

GET_INFO_HEADERS = {
  'accept': 'application/json',
}

JINS_API_COLUMNS = ['date', 'zone', 'focus', 'calm', 'posture', 'bki_sum', 'bki_n']

# PROXY = {
#   'http': os.environ["http_proxy"],
#   'https': os.environ["https_proxy"]
# }
