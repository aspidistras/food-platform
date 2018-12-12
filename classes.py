import requests
import json

from constants import *


class Product:
    """defines every attributes needed regarding a product"""

    def __init__(self):
        """sets default values for the attributes"""

        self.name = ""
        self.id = 0
        self.category_id = 0
        self.saved = 0
        self.score = 0
        self.url = ""


class Category:
    """defines every attributes needed regarding a category"""

    def __init__(self):
        """sets default values for the attributes"""

        self.name = ""
        self.id = 0
        self.products_nb = 0


class Database:
    """defines an object symmetrical to the MySQL database"""

    def __init__(self):
        """initializes lists containing all products and categories"""

        self.categories = []
        self.products = []

    def get_categories(self):
        """gathers categories data via the API and instantiates a Category object with its attributes
        for every category, then adds it to the list"""

        for c_id, page in enumerate(categories_names_url):  # browses the list of selected categories

            url = categories_welcome_page.format(page)
            request = requests.get(url)
            result = json.loads(request.text)  # turns json result into a dictionary
            category = Category()
            category.id = c_id
            category.name = categories_names_code[c_id]
            category.products_nb = result["count"]
            self.categories.append(category)

    def get_products(self):
        """gathers products data via the API and instantiates a Product object with its attributes
        for every product, then adds it to the list"""

        for idx, category in enumerate(categories_names_url, 1):  # browses the list of selected categories

            for page in range(1, limit_pages_nb):  # browses the pages within the defined limit

                url = products_page.format(category, page)
                request = requests.get(url)
                result = json.loads(request.text)
                products = result["products"]

                for p_id, item in enumerate(products):  # browses the dictionary of products

                    if "generic_name_fr" in item and item["generic_name_fr"] != "" and "nutrition_grades" in item:
                        # makes sure we don't get a product that doesn't have a name or a nutrition grade

                        product = Product()
                        product.name = item["generic_name_fr"]
                        product.id = p_id
                        product.category_id = idx
                        product.url = item["url"]
                        score = item["nutrition_grades"]
                        product.score = scores.index(score) + 1  # translates the letter score into a numeric one
                        self.products.append(product)
