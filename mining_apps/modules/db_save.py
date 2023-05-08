import csv
import sys
from mining_apps.models import LivedoorNewscorpus

def main(csv_file, batch_size=1000):
    instances = []

    with open(csv_file.temporary_file_path(), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)

        for row in reader:

#           データ列が欠損していたらエラー処理
            if len(row) < 3:
                print('Error: the row has less than 3 elements')
                sys.exit()

#           データを作成してインスタンスに追加する
            instance = LivedoorNewscorpus(label=row[0], name=row[1], sentence=row[2])
            instances.append(instance)

#           リストの長さが1000 or ファイルの最終行 になったらデータベースに登録する
            if len(instances) == batch_size:
                LivedoorNewscorpus.objects.bulk_create(instances)
                instances = []

#       残りのデータをデータベースに登録する
        if len(instances) > 0:
            LivedoorNewscorpus.objects.bulk_create(instances)
