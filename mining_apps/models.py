from django.db import models

# Create your models here.
class LivedoorNewscorpus(models.Model):
    label    = models.CharField(max_length=50)
    name     = models.CharField(max_length=50, primary_key=True)
    sentence = models.TextField()
'''
    livedoorニュースコーパスのデータを保存するデータベース
    label    : ニュース記事のカテゴリー
    name     : ニュース記事の名前
    sentence : 記事の本文

    db_index = True について
    Djangoでデータベースのインデックスを作成するために使用されるフラグ。
    データベースインデックスは、検索や並べ替えなどの要求を高速化するために使用する。
'''