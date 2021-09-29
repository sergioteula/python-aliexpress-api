"""AliExpress API wrapper for Python

A simple Python wrapper for the AliExpress Open Platform API. This module allows
to get product information and affiliate links from AliExpress using the official
API in an easier way.
"""

from .skd import setDefaultAppInfo
from .skd import api as aliapi
from .tools import get_product_id
from .errors import AliexpressException, ProductsNotFoudException, InvalidTrackingIdException
from .helpers import api_request
from .helpers import get_links_string
from . import models

from types import SimpleNamespace
from typing import List, Union
import json


class AliexpressApi:
    """Provides methods to get information from AliExpress using your API credentials.

    Args:
        key (str): Your API key.
        secret (str): Your API secret.
        language (str): Language code. Defaults to EN.
        currency (str): Currency code. Defaults to USD.
        tracking_id (str): The tracking id for link generator. Defaults to None.
    """

    def __init__(self,
        key: str,
        secret: str,
        language: models.Language,
        currency: models.Currency,
        tracking_id: str = None,
        app_signature: str = None,
        **kwargs):
        self._key = key
        self._secret = secret
        self._tracking_id = tracking_id
        self._language = language
        self._currency = currency
        self._app_signature = app_signature
        setDefaultAppInfo(self._key, self._secret)


    def product_info(self, product_id: str):
        """Find product information for a specific product on AliExpress.

        Args:
            product_id (str): One item ID or product URL.
        """
        product_id = get_product_id(str(product_id))
        if product_id:
            product = aliapi.rest.AliexpressAffiliateProductdetailGetRequest()
            product.app_signature = None
            product.fields = None
            product.product_ids = product_id
            product.target_currency = self._currency
            product.target_language = self._language
            product.tracking_id = self._tracking_id
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

    def get_affiliate_links(self,
        links: Union[str, List[str]],
        link_type: models.LinkType = models.LinkType.NORMAL,
        **kwargs) -> List[models.AffiliateLink]:
        """Converts a list of links in affiliate links.

        Args:
            links (``str | list[str]``): One or more links as a list of strings or a string
                separated by commas.
            link_type (``models.LinkType``): Choose between normal link with standard commission
                or hot link with hot product commission. Defaults to NORMAL.
        """
        if not self._tracking_id:
            raise InvalidTrackingIdException('The tracking id is required for affiliate links')

        links = get_links_string(links)

        request = aliapi.rest.AliexpressAffiliateLinkGenerateRequest()
        request.app_signature = self._app_signature
        request.source_values = links
        request.promotion_link_type = link_type
        request.tracking_id = self._tracking_id

        response = api_request(request, 'aliexpress_affiliate_link_generate_response')

        if response.total_result_count > 0:
            return response.promotion_links.promotion_link
        else:
            raise ProductsNotFoudException('Affiliate links not available')


    def get_hotproducts(self,
        category_ids: str = None,
        delivery_days: int = None,
		fields: str = None,
		keywords: str = None,
		max_sale_price: int = None,
		min_sale_price: int = None,
		page_no: int = None,
		page_size: int = None,
		platform_product_type: models.ProductType = None,
		ship_to_country: str = None,
		sort: models.SortBy = None,
        **kwargs):
        """Search for affiliated products with high commission.

        Args:
            category_ids (``str``): One or more category IDs separated by commas.
            delivery_days (``int``): Estimated delivery days.
            fields (``str``): The fields to include in the results list separated by commas.
            keywords (``str``): Search products based on keywords.
            max_sale_price (``int``): Filters products with price below the specified value.
                Prices appear in lowest currency denomination. So $31.41 should be 3141.
            min_sale_price (``int``): Filters products with price above the specified value.
                Prices appear in lowest currency denomination. So $31.41 should be 3141.
            page_no (``int``):
            page_size (``int``): Products on each page. Should be between 1 and 50.
            platform_product_type (``models.ProductType``): Specify platform product type.
            ship_to_country (``str``): Filter products that can be sent to that country.
                Returns the price according to the country's tax rate policy.
            sort (``models.SortBy``): Specifies the sort method.
        """
        request = aliapi.rest.AliexpressAffiliateHotproductQueryRequest()
        request.app_signature = self._app_signature
        request.category_ids = category_ids
        request.delivery_days = str(delivery_days)
        request.fields = fields
        request.keywords = keywords
        request.max_sale_price = max_sale_price
        request.min_sale_price = min_sale_price
        request.page_no = page_no
        request.page_size = page_size
        request.platform_product_type = platform_product_type
        request.ship_to_country = ship_to_country
        request.sort = sort
        request.target_currency = self._currency
        request.target_language = self._language
        request.tracking_id = self._tracking_id

        response = api_request(request, 'aliexpress_affiliate_hotproduct_query_response')

        if response.current_record_count > 0:
            response.products = response.products.product
            return response
        else:
            raise ProductsNotFoudException('No products found with current parameters')
