from django.db import models

class SiteUsers(models.Model):
    login = models.CharField(max_length=30, blank=True, null=True)
    pasword = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    role = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'SiteUsers'


class Categories(models.Model):
    categorie = models.CharField(db_column='Categorie', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'categories'


class CategoriesOfProduct(models.Model):
    categorie = models.ForeignKey(Categories, models.DO_NOTHING)
    product = models.ForeignKey('Product', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'categories_of_product'


class Product(models.Model):
    cost_on_sell = models.IntegerField(db_column='Cost_on_sell')  # Field name made lowercase.
    cost_on_buy = models.IntegerField(db_column='Cost_on_buy')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    quantity_on_stock = models.IntegerField(db_column='Quantity_on_stock')  # Field name made lowercase.
    picture = models.ImageField(max_length=255, upload_to='main/img/')

    class Meta:
        managed = False
        db_table = 'product'


class Saeles(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    id_users = models.ForeignKey(SiteUsers, models.DO_NOTHING, db_column='id_users')
    date = models.DateField()
    price = models.IntegerField()
    id_product = models.ForeignKey(Product, models.DO_NOTHING, db_column='id_product')

    class Meta:
        managed = False
        db_table = 'saeles'


class Trashbox(models.Model):
    id_user = models.ForeignKey(SiteUsers, models.DO_NOTHING, db_column='id_user')
    id_product = models.ForeignKey(Product, models.DO_NOTHING, db_column='id_product')

    class Meta:
        managed = False
        db_table = 'trashbox'
