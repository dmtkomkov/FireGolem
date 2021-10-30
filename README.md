# FireGolem

## Overview

## Installation

Installation is handled by ansible script in automation repository
In order to use debug version on Windows, use command in powershell $Env:DJANGO="DEV"

### Generate lets encrypt certificate

1. Install epel-release
2. Install python-certbot-apache
3. sudo certbot --apache -d node.example.com

## API EXAMPLES

API guide

### BLOG

*To be done*

### GOAL

#### Worklog

- Create


    POST {'log': 'worklog1', 'labels': ['label1', 'label2']}
    POST {'log': 'worklog1'}

- Update


    PUT {'log': 'worklog1', 'labels': ['label2', 'label1'], 'date': '2019-08-13'}

- Delete


    DELETE

- List


    GET // Ordered by date and id desc.

#### Label

Groups identified by name in label api

- Create


    POST {'name': 'label1', 'group': 'new_group'}
    POST {'name': 'label1', 'group': 'existed_group'}
    POST {'name': 'label1'} // set group None by default

- Update


    PUT {'name': 'label1', 'group': 'new_group'}
    PUT {'name': 'label1', 'group': 'existed_group'}
    PUT {'name': 'label1'} // set group None by default

- Delete


    DELETE: if last label was removed from group - remove the group as well

- List


    GET // Ordered by id.

- Table list


    GET // special url that returns object with all grouped labels including 'NO_GROUP'

#### Group

Every label has a group (None by default).
Groups are created and removed on the fly with label api.
Only update is available in group api

- Update


    PUT {'name': 'group1', 'color': '#aaaaaa'}
