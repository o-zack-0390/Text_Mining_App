import os
import csv
import itertools
from django.core.exceptions import ObjectDoesNotExist
from mining_apps.models     import LivedoorNewscorpus

'''
以下の形式でlivedoorニュースコーパスを指定のファイルに記録するプログラム
ラベル番号,ファイル名,文章
'''
def main(input_type1, input_type2, input_type3, input_type4, input_type5, input_type6, select_file):

  path      = os.path.abspath('livedoor_news_corpus.txt') # write [正解ラベル, ファイル名, 文章]
  label_flag = 'N'

  if input_type4 != 'N' or input_type5 != 'N':
     label_flag = 'Y'

# 共通の処理を実行
  common_process(path, input_type1, input_type3, label_flag, input_type6, select_file)

# 正解ラベルを欠損値にする処理
  loss_process(input_type4, input_type5, path)

# 出力形式がcsvファイルの場合
  if   input_type2 == "csv":
    csv_process(path)

# 出力形式がtsvファイルの場合
  elif input_type2 == "tsv":
    tsv_process(path)

# 出力形式がtxtファイルの場合
  else:
    pass


''' テキスト形式で出力する処理 '''
def common_process(path, format_flag, name_flag, label_flag, sentence_flag, select_file):

  all_data      = None
  write_f       = open(path, 'w', encoding="utf-8", newline='')
  id_list       = []
  name_list     = []
  sentence_list = []

  if select_file != None:
    all_data = []
    content  = select_file.read().decode('utf-8')
    reader   = csv.reader(content.splitlines())
    for row in reader:
            try:
                data = LivedoorNewscorpus.objects.get(pk=str(row).strip("['']"))
                all_data.append(data)
            except ObjectDoesNotExist:
                pass
  else:
    all_data = LivedoorNewscorpus.objects.all()

  if label_flag == 'Y':
     for data in all_data:
        id_list.append(data.label)

  if name_flag == 'Y':
     for data in all_data:
        name_list.append(',' + data.name)

  if sentence_flag == 'Y':
     if format_flag == "分かち書き+整形":
        for data in all_data:
           sentence_list.append(',' + format_process(data.sentence))
     else:
        for data in all_data:
           sentence_list.append(',' + data.sentence)

  for label, name, sentence in itertools.zip_longest(id_list, name_list, sentence_list, fillvalue=''):
     new_line = label + name + sentence + "\n"
     if new_line[0] ==  ',':
        new_line = new_line[1:]
     write_f.write(new_line)
  write_f.close()

  id_list.clear()
  name_list.clear()
  sentence_list.clear()


'''文章を整形する関数'''
def format_process(text):
    text = ''.join(['0' if char.isdigit() else char for char in text])         # 文章中の数字を0に置き換える
    text = ''.join(char for char in text if char.isalnum() or char.isspace())  # 文章中の記号を削除する
    text = text.replace(',', ' ')                                              # csvの列が乱れるので削除する
    text = text.replace("\t", ' ')                                             # tsvの列が乱れるので削除する
    text = text.lower()                                                        # 英単語は全て小文字にする
    return text


'''ラベルを欠損値にする処理'''
def loss_process(flag1, flag2, f_path):

  prev_label   = -99999
  this_label   = None
  file_count   = 0
  loss_rate    = None
  groups       = []
  updated_rows = []
  
# 「欠損値なしが有効」 or 「欠損値ありが無効」 の場合は欠損値なしで出力
  if flag1 == 'Y' or flag2 == 'N':
    return
  
  else:
    loss_rate = int(flag2) / 100
  
# テキスト形式で出力する場合
  with open(f_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)

    for row in reader:
        this_label = row[0]

        if this_label != prev_label:
            groups.append(file_count)

        updated_rows.append(row)
        file_count += 1
        prev_label  = this_label

  groups.append(file_count)
  group_size = len(groups)

  for i in range(1, group_size):
      end_index   = groups[i]
      start_index = int(end_index - ( (end_index - groups[i-1]) * loss_rate ))

      for j in range(start_index, end_index):
          updated_rows[j][0] = ''
  
  f = open(f_path, 'w', encoding='utf-8')
  for row in updated_rows:
      f.write(','.join(row)+"\n")
  f.close()
  

''' csvファイルで出力する処理 '''
def csv_process(path):

  csv_list = []
  read_f   = open(path, 'r', encoding="utf-8")
  line     = read_f.readline()

  while line:
     line = line.replace("\n", '')
     line = line.split(',')
     csv_list.append(line)
     line = read_f.readline()
  read_f.close()

  with open(path.replace("txt", "csv"), 'w', encoding="utf-8", newline='') as f:
    writer = csv.writer(f)
    writer.writerows(csv_list)

  csv_list.clear()


''' tsvファイルで出力する処理 '''
def tsv_process(path):
   
  tsv_list = []
  read_f   = open(path, 'r', encoding="utf-8")
  line     = read_f.readline()

  while line:
     line = line.replace("\n", '')
     line = line.split(',')
     tsv_list.append(line)
     line = read_f.readline()
  read_f.close()

  with open(path.replace("txt", "tsv"), 'w', encoding="utf-8", newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerows(tsv_list)

  tsv_list.clear()


def delete_file():
  
# ファイルを開くことでデータが上書きされる
  f1 = open(os.path.abspath('livedoor_news_corpus.txt'), 'w', encoding="utf-8", newline='')
  f2 = open(os.path.abspath('livedoor_news_corpus.csv'), 'w', encoding="utf-8", newline='')
  f3 = open(os.path.abspath('livedoor_news_corpus.tsv'), 'w', encoding="utf-8", newline='')

# 何もしないでファイルを閉じることで白紙の状態に戻すことができる
  f1.close()
  f2.close()
  f3.close()