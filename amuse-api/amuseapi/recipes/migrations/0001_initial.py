# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Recipe'
        db.create_table(u'recipes_recipe', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='recipes', to=orm['users.User'])),
            ('language', self.gf('django.db.models.fields.CharField')(default='ES', max_length=10)),
            ('created_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('cooking_time', self.gf('django.db.models.fields.FloatField')()),
            ('image', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('total_rating', self.gf('django.db.models.fields.IntegerField')()),
            ('users_rating', self.gf('django.db.models.fields.IntegerField')()),
            ('servings', self.gf('django.db.models.fields.IntegerField')()),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'recipes', ['Recipe'])

        # Adding model 'RecipeCategory'
        db.create_table(u'recipes_recipecategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(related_name='categories', to=orm['recipes.Recipe'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'recipes', ['RecipeCategory'])

        # Adding model 'RecipeIngredient'
        db.create_table(u'recipes_recipeingredient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ingredients', to=orm['recipes.Recipe'])),
            ('sort_number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('quantity', self.gf('django.db.models.fields.FloatField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('measurement_unit', self.gf('django.db.models.fields.CharField')(default='unit', max_length=100)),
        ))
        db.send_create_signal(u'recipes', ['RecipeIngredient'])

        # Adding model 'RecipeDirection'
        db.create_table(u'recipes_recipedirection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(related_name='directions', to=orm['recipes.Recipe'])),
            ('sort_number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('video', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('time', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'recipes', ['RecipeDirection'])

        # Adding model 'RecipeComment'
        db.create_table(u'recipes_recipecomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['recipes.Recipe'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['users.User'])),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('timestamp', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'recipes', ['RecipeComment'])


    def backwards(self, orm):
        # Deleting model 'Recipe'
        db.delete_table(u'recipes_recipe')

        # Deleting model 'RecipeCategory'
        db.delete_table(u'recipes_recipecategory')

        # Deleting model 'RecipeIngredient'
        db.delete_table(u'recipes_recipeingredient')

        # Deleting model 'RecipeDirection'
        db.delete_table(u'recipes_recipedirection')

        # Deleting model 'RecipeComment'
        db.delete_table(u'recipes_recipecomment')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'recipes.recipe': {
            'Meta': {'object_name': 'Recipe'},
            'cooking_time': ('django.db.models.fields.FloatField', [], {}),
            'created_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'ES'", 'max_length': '10'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recipes'", 'to': u"orm['users.User']"}),
            'servings': ('django.db.models.fields.IntegerField', [], {}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'total_rating': ('django.db.models.fields.IntegerField', [], {}),
            'updated_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'users_rating': ('django.db.models.fields.IntegerField', [], {})
        },
        u'recipes.recipecategory': {
            'Meta': {'object_name': 'RecipeCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'categories'", 'to': u"orm['recipes.Recipe']"})
        },
        u'recipes.recipecomment': {
            'Meta': {'object_name': 'RecipeComment'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['recipes.Recipe']"}),
            'timestamp': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['users.User']"})
        },
        u'recipes.recipedirection': {
            'Meta': {'object_name': 'RecipeDirection'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'directions'", 'to': u"orm['recipes.Recipe']"}),
            'sort_number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'time': ('django.db.models.fields.FloatField', [], {}),
            'video': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'recipes.recipeingredient': {
            'Meta': {'object_name': 'RecipeIngredient'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measurement_unit': ('django.db.models.fields.CharField', [], {'default': "'unit'", 'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'quantity': ('django.db.models.fields.FloatField', [], {}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ingredients'", 'to': u"orm['recipes.Recipe']"}),
            'sort_number': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'users.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"})
        }
    }

    complete_apps = ['recipes']