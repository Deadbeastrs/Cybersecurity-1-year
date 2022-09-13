from website.app_start import create_app
from flask import Flask

app = create_app({
    'SECRET_KEY': 'IAA_Secret_Key'
    #'OAUTH2_REFRESH_TOKEN_GENERATOR': True,
})


