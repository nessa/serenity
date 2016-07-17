from django.contrib import admin
from recipes.models import User
from recipes.models import Recipe
from recipes.models import RecipeCategory
from recipes.models import RecipeIngredient
from recipes.models import RecipeDirection
from recipes.models import RecipeComment
from recipes.models import RecipeRating
from recipes.models import Ingredient
from recipes.models import TranslatedIngredient
from recipes.models import IngredientCategory

class AuthorAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'

# Models registered
admin.site.register(User)
admin.site.register(Recipe)
admin.site.register(RecipeCategory)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeDirection)
admin.site.register(RecipeComment)
admin.site.register(RecipeRating)
admin.site.register(Ingredient)
admin.site.register(TranslatedIngredient)
admin.site.register(IngredientCategory)
