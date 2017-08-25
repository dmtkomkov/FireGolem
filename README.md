# FireGolem

## Overview

## Installation

### Create database

Database have to be created with utf8 support
```
CREATE DATABASE FireGolem CHARACTER SET utf8;
```

### Generate self-signed certificate

sosulka.com domain is temporarily used. One certificate might be found in certs/sosulka.com.cer.
If its expired new one must be generated with command
```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout mysitename.key -out mysitename.crt -config <(cat certs/cert_ssl.conf)
```