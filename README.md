# Sell it!

## General info
*Sell it!* is an online marketplace web application built with Django that handles offers announcements displaying and allows their management.
![](https://i.imgur.com/lYjxzSj.png)

## Features
- Website is fully responsive - mobile, tablet, desktop;
- Users can add, modify and delete their offers,
- Users can manage their profile's details and visibility,
- Users can message other users,
- Administrators can manage offers and users through customised Django admin site,

## Structure
### Description
This website is based on Django (both backend and frontend) and is divided into two main parts:
* **public** - place where people can browse, add, modify and delete offers
* **admin** - place where an administrator can manage the content (it is basically a modifed built-in Django's admin site)

### Django apps
- **Offers** - displaying, adding, modifying and deleting offers
- **Users** - user registration, login
- **Messages** - conversations between users

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

[requirements.txt](requirements.txt).

### External libraries

| LIBRARY NAME                                 | VERSION |
| -------------------------------------------- | ------- |
| [bootstrap](https://getbootstrap.com/)       | 4.0.0   |
| [fancybox](http://fancyapps.com/fancybox/3/) | 3.5.7   |
| [fontawesome](https://fontawesome.com/)      | 5.14.0  |
| [jquery](https://jquery.com/)                | 3.2.1   |
