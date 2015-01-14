# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'recipes_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'recipes', ['Category'])

        # Adding model 'Ingredient'
        db.create_table(u'recipes_ingredient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quantity', self.gf('django.db.models.fields.FloatField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('measurement_unit', self.gf('django.db.models.fields.CharField')(default='unit', max_length=100)),
        ))
        db.send_create_signal(u'recipes', ['Ingredient'])

        # Adding model 'Direction'
        db.create_table(u'recipes_direction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sort_number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('video', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('time', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'recipes', ['Direction'])

        # Adding model 'Comment'
        db.create_table(u'recipes_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['users.User'])),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('timestamp', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'recipes', ['Comment'])

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

        # Adding M2M table for field categories on 'Recipe'
        m2m_table_name = db.shorten_name(u'recipes_recipe_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('recipe', models.ForeignKey(orm[u'recipes.recipe'], null=False)),
            ('category', models.ForeignKey(orm[u'recipes.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['recipe_id', 'category_id'])

        # Adding M2M table for field ingredients on 'Recipe'
        m2m_table_name = db.shorten_name(u'recipes_recipe_ingredients')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('recipe', models.ForeignKey(orm[u'recipes.recipe'], null=False)),
            ('ingredient', models.ForeignKey(orm[u'recipes.ingredient'], null=False))
        ))
        db.create_unique(m2m_table_name, ['recipe_id', 'ingredient_id'])

        # Adding M2M table for field directions on 'Recipe'
        m2m_table_name = db.shorten_name(u'recipes_recipe_directions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('recipe', models.ForeignKey(orm[u'recipes.recipe'], null=False)),
            ('direction', models.ForeignKey(orm[u'recipes.direction'], null=False))
        ))
        db.create_unique(m2m_table_name, ['recipe_id', 'direction_id'])

        # Adding M2M table for field comments on 'Recipe'
        m2m_table_name = db.shorten_name(u'recipes_recipe_comments')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('recipe', models.ForeignKey(orm[u'recipes.recipe'], null=False)),
            ('comment', models.ForeignKey(orm[u'recipes.comment'], null=False))
        ))
        db.create_unique(m2m_table_name, ['recipe_id', 'comment_id'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'recipes_category')

        # Deleting model 'Ingredient'
        db.delete_table(u'recipes_ingredient')

        # Deleting model 'Direction'
        db.delete_table(u'recipes_direction')

        # Deleting model 'Comment'
        db.delete_table(u'recipes_comment')

        # Deleting model 'Recipe'
        db.delete_table(u'recipes_recipe')

        # Removing M2M table for field categories on 'Recipe'
        db.delete_table(db.shorten_name(u'recipes_recipe_categories'))

        # Removing M2M table for field ingredients on 'Recipe'
        db.delete_table(db.shorten_name(u'recipes_recipe_ingredients'))

        # Removing M2M table for field directions on 'Recipe'
        db.delete_table(db.shorten_name(u'recipes_recipe_directions'))

        # Removing M2M table for field comments on 'Recipe'
        db.delete_table(db.shorten_name(u'recipes_recipe_comments'))


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
        u'recipes.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'recipes.comment': {
            'Meta': {'object_name': 'Comment'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['users.User']"})
        },
        u'recipes.direction': {
            'Meta': {'object_name': 'Direction'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'sort_number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'time': ('django.db.models.fields.FloatField', [], {}),
            'video': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'recipes.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measurement_unit': ('django.db.models.fields.CharField', [], {'default': "'unit'", 'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'quantity': ('django.db.models.fields.FloatField', [], {})
        },
        u'recipes.recipe': {
            'Meta': {'object_name': 'Recipe'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['recipes.Category']", 'symmetrical': 'False'}),
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['recipes.Comment']", 'symmetrical': 'False'}),
            'cooking_time': ('django.db.models.fields.FloatField', [], {}),
            'created_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'directions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['recipes.Direction']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'ingredients': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['recipes.Ingredient']", 'symmetrical': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'ES'", 'max_length': '10'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recipes'", 'to': u"orm['users.User']"}),
            'servings': ('django.db.models.fields.IntegerField', [], {}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'total_rating': ('django.db.models.fields.IntegerField', [], {}),
            'updated_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'users_rating': ('django.db.models.fields.IntegerField', [], {})
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