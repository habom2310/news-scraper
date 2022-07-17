import src.backend.lib.utils as utils

class WebConfig:
    def __init__(self, webname):
        self._webname = webname
        self._web = utils.load_config_file(r"src\backend\input\data.yaml")[webname]

    def get_config(self, key, default=""):
        if key not in self._web.keys():
            self.set_config(key, default)
            return default
        else:
            value = self._web[key]
            try:
                return int(value)
            except:
                return value

    def set_config(self, key, value):
        self._web[key] = value

    def get_webname(self):
        return self._webname

    def get_main_url(self):
        return self.get_config("main_url")

    def get_main_category_tag(self):
        return self.get_config("main_category_tag")
    def get_main_category_class(self):
        return self.get_config("main_category_class")

    def get_main_subcategory_tag(self):
        return self.get_config("main_subcatergory_tag")
    def get_main_subcatergory_class(self):
        return self.get_config("main_subcatergory_class")

    def get_cat_post_tag(self):
        return self.get_config("cat_post_tag")
    def get_cat_post_class(self):
        return self.get_config("cat_post_class")
    
    def get_subcat_post_tag(self):
        return self.get_config("subcat_post_tag")
    def get_subcat_post_class(self):
        return self.get_config("subcat_post_class")

    def get_article_title_tag(self):
        return self.get_config("article_title_tag")
    def get_article_title_class(self):
        return self.get_config("article_title_class")

    def get_article_metadata_tag(self):
        return self.get_config("article_metadata_tag")
    def get_article_metadata_class(self):
        return self.get_config("article_metadata_class")

    def get_article_metadata_author_tag(self):
        return self.get_config("article_metadata_author_tag")
    def get_article_metadata_author_class(self):
        return self.get_config("article_metadata_author_class")

    def get_article_metadata_datetime_tag(self):
        return self.get_config("article_metadata_datetime_tag")
    def get_article_metadata_datetime_class(self):
        return self.get_config("article_metadata_datetime_class")

    def get_article_text_tag(self):
        return self.get_config("article_text_tag")
    def get_article_text_class(self):
        return self.get_config("article_text_class")