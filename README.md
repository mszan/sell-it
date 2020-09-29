# SELL IT!

Selll it! is an online marketplace web application built with Django 3.1 that handles offers announcements displaying and allows their management.
![](https://i.imgur.com/lYjxzSj.png)

## Live demo
Live web demo is available at [sell-it.mszanowski.pl](https://sell-it.mszanowski.pl).
### Description
- Hosted on [GAE](https://cloud.google.com/appengine).
- Media and static handled by [Cloud Storage](https://cloud.google.com/storage/docs/introduction).
- SQL uses Cloud SQL Proxy as described [here](https://cloud.google.com/python/django/appengine#installingthecloudsqlproxy).

## Structure
### Django apps
- **Offers** - displaying, adding, modifying and deleting offers
- **Users** - user registration, login
- **Messages** - conversations between users
### API - DRF
Available at [sell-it.mszanowski.pl/api](https://sell-it.mszanowski.pl/api) as a browsable API.
- For now it  handles only `GET`, `HEAD` and `OPTIONS` methods with basic access authentication.
- API has not been seperated to another app yet.

## Requirements

### Python packages
| **PACKAGE NAME**    | VERSION |
| ------------------- | ------- |
| django              | 3.1     |
| django-compressor   | 2.4     |
| django-crispy-forms | 1.9.2   |
| django-libsass      | 0.8     |
| django-mptt         | 0.11.0  |
| django-registration | 3.1     |
| django-storages     | 1.10.1  |
| djangorestframework | 3.11.1  |
| psycopg2-binary     | 2.8.5   |

Full `pip freeze` can be found in [requirements.txt](requirements.txt).

### External libraries

| LIBRARY NAME                                 | VERSION |
| -------------------------------------------- | ------- |
| [bootstrap](https://getbootstrap.com/)       | 4.0.0   |
| [fancybox](http://fancyapps.com/fancybox/3/) | 3.5.7   |
| [fontawesome](https://fontawesome.com/)      | 5.14.0  |
| [jquery](https://jquery.com/)                | 3.2.1   |