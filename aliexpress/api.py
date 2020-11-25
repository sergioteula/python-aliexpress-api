"""AliExpress API wrapper for Python

A simple Python wrapper for the AliExpress Open Platform API. This module allows
to get product information and affiliate links from AliExpress using the official
API in an easier way.
"""

import aliexpress.top.api
import json
from types import SimpleNamespace


class AliexpressException(Exception):
    """Custom exception class for AliExpress API."""
    def __init__(self, status=None, reason=None):
        self.status = status
        self.reason = reason

    def __str__(self):
        if self.reason:
            return '%s: %s' % (self.status, self.reason)
        else:
            return '%s' % (self.status)


def get_product_id(text):
    """Returns product ID for a given link."""
    product_id = text.split('?')[0]
    product_id = product_id.replace('.', '/').split('/')
    if len(product_id) == 1:
        product_id = product_id[0]
    else:
        product_id = product_id[-2]
    try:
        return int(product_id)
    except ValueError:
        return None


class Aliexpress:
    """Creates an instance containing your API credentials.

    Args:
        key (str): Your API key.
        secret (str): Your API secret.
        language (str): Language code. Defaults to EN.
        currency (str): Currency code. Defaults to USD.
        tracking_id (str): The tracking id for link generator. Defaults to None.
    """
    def __init__(self, key: str, secret: str, language='EN', currency='USD', tracking_id=None):
        self.key = key
        self.secret = secret
        self.tracking_id = tracking_id
        self.language = language
        self.currency = currency
        aliexpress.top.setDefaultAppInfo(self.key, self.secret)

    def product_info(self, product_id: str):
        """Find product information for a specific product on AliExpress.

        Args:
            product_id (str): One item ID or product URL.
        """
        product_id = get_product_id(str(product_id))
        if product_id:
            product = aliexpress.top.api.rest.AliexpressAffiliateProductdetailGetRequest()
            product.app_signature = None
            product.fields = None
            product.product_ids = product_id
            product.target_currency = self.currency
            product.target_language = self.language
            product.tracking_id = self.tracking_id
            try:
                response = product.getResponse()
                response = json.dumps(response)
                response = json.loads(response, object_hook=lambda d: SimpleNamespace(**d))
                response = response.aliexpress_affiliate_productdetail_get_response.resp_result
                if response.resp_code == 200:
                    response = response.result
                    if response.current_record_count > 0:
                        response = response.products.product[0]
                        return response
                    else:
                        raise AliexpressException('Product not available')
                else:
                    raise AliexpressException('Server not reached')
            except Exception as e:
                raise AliexpressException(e)
        else:
            raise AliexpressException('Product ID not found')

    def affiliate_link(self, link: str):
        """Creates affiliate link for a specific product.

        Args:
            link (str): The URL that needs to be converted.
        """
        if self.tracking_id:
            affiliate = aliexpress.top.api.rest.AliexpressAffiliateLinkGenerateRequest()
            affiliate.source_values = link
            affiliate.promotion_link_type = "0"
            affiliate.tracking_id = self.tracking_id
            try:
                response = affiliate.getResponse()
                response = json.dumps(response)
                response = json.loads(response, object_hook=lambda d: SimpleNamespace(**d))
                response = response.aliexpress_affiliate_link_generate_response.resp_result
                if response.resp_code == 200:
                    response = response.result
                    if response.total_result_count > 0:
                        response = response.promotion_links.promotion_link[0].promotion_link
                        return response
                    else:
                        raise AliexpressException('Affiliate link not available')
                else:
                    raise AliexpressException('Server not reached')
            except Exception as e:
                raise AliexpressException(e)
        else:
            raise AliexpressException('Tracking ID not specified')
