from art.models import Category

class CategoryTree(object):

    def __init__(self):
        self.cats = Category.objects.all()
        self.categories = []
        for c in cats.filter(sub_category_id=None):
            sub_cats = cats.filter(sub_category_id=c.id)
            category = CategoryNode(c, sub_cats)
            self.categories.append(category)

    def get_subs(self, cat_id):
        return self.cats.filter(sub_category_id=cat_id)


class CategoryNode(object):
    def __init__(self, cat, sub_cats):
        self.name = cat.name
        self.sub_categories = []
        if sub_cats:
            for c in sub_cats:
                self.sub_categories.append(c.name)