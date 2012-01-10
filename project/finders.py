from django.contrib.staticfiles.finders import AppDirectoriesFinder
from django.contrib.staticfiles.storage import AppStaticStorage

class LegacyAppStaticStorage(AppStaticStorage):
    source_dir = 'media'

class AppMediaFinder(AppDirectoriesFinder):
    storage_class = LegacyAppStaticStorage
