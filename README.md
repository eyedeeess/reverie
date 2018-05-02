[![Build Status](https://travis-ci.org/oneirism/reverie.svg?branch=master)](https://travis-ci.org/oneirism/reverie)
[![Coverage Status](https://coveralls.io/repos/github/oneirism/reverie/badge.svg)](https://coveralls.io/github/oneirism/reverie)
[![Known Vulnerabilities](https://snyk.io/test/github/oneirism/reverie/badge.svg?targetFile=package.json)](https://snyk.io/test/github/oneirism/reverie?targetFile=package.json)

# reverie

## Production Configuration

Create a production settings file named `reverie/settings/prod.py` and configure:

1. `EMAIL_BACKEND` - [Documentation](https://docs.djangoproject.com/en/2.0/topics/email/#topic-email-backends)
1. `TWO_FACTOR_SMS_GATEWAY` - [Documentation](http://django-two-factor-auth.readthedocs.io/en/stable/configuration.html#twilio-gateway)
