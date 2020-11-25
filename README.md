AliExpress API wrapper for Python
=======================================================
A simple Python wrapper for the [AliExpress Open Platform API](https://developers.aliexpress.com). This module allows to get product information and affiliate links from AliExpress using the official API in an easier way.

[![PyPI](https://img.shields.io/pypi/v/python-aliexpress-api?color=%231182C2&label=PyPI)](https://pypi.org/project/python-aliexpress-api/)
[![Python](https://img.shields.io/badge/Python-3.x-%23FFD140)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-%23e83633)](https://github.com/sergioteula/python-aliexpress-api/blob/master/LICENSE)
[![Support](https://img.shields.io/badge/Support-Good-brightgreen)](https://github.com/sergioteula/python-aliexpress-api/issues)


Features
--------

* Object oriented interface for simple usage.
* Get information about a product through its ID or URL.
* Support for language and currency configuration.
* Ask for new features through the [issues](https://github.com/sergioteula/python-aliexpress-api/issues) section.
* Join our [Telegram group](https://t.me/PythonAliExpressAPI) for support or development.

Installation
-------------

You can install or upgrade the module with:

    pip install python-aliexpress-api --upgrade


Usage guide
-----------
**Get product information:**

    from aliexpress.api import Aliexpress
    aliexpress = Aliexpress(KEY, SECRET, 'ES', 'EUR', TRACKING_ID)
    product = aliexpress.product_info('1000006468625')
    print(product.product_title)

**Get affiliate link:**

    from aliexpress.api import Aliexpress
    aliexpress = Aliexpress(KEY, SECRET, 'EN', 'USD', TRACKING_ID)
    url = aliexpress.affiliate_link('https://aliexpress.com/item/1000006468625.html')

Changelog
-------------

    Version 1.0.3
        -First release.

License
-------------
Copyright © 2020 Sergio Abad. See [license](https://github.com/sergioteula/python-aliexpress-api/blob/master/LICENSE) for details.
