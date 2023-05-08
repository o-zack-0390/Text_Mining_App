import csv
import itertools

'''
以下の形式でlivedoorニュースコーパスをtxtファイルに記録するプログラム
ラベル番号,ファイル名,文章
'''
def main(order_path, input_type1, input_type2, input_type3, input_type4, input_type5):

  path1 = order_path                        # read  [文章]
  path2 = './data/id.txt'                   # read  [正解ラベル]
  path3 = './data/name.txt'                 # read  [ファイル名]
  path4 = './data/livedoor_news_corpus.txt' # write [正解ラベル, ファイル名, 文章]

# 共通の処理を実行
  common_process(path1, path2, path3, path4, input_type2, input_type3, input_type5)

# 正解ラベルを欠損値にする処理
  loss_process(input_type4, path4)

# 出力形式がcsvファイルの場合
  if   input_type1 == "csv":
    csv_process(path4)

# 出力形式がtsvファイルの場合
  elif input_type1 == "tsv":
    tsv_process(path4)

# 出力形式がtxtファイルの場合
  else:
    pass


''' テキスト形式で出力する処理 '''
def common_process(path1, path2, path3, path4, name_flag, label_flag, sentence_flag):

  write_f       = open(path4, 'w', encoding="utf-8", newline='')
  f_id          = open(path2, 'r', encoding="utf-8")
  f_name        = open(path3, 'r', encoding="utf-8")
  f_sentence    = open(path1, 'r', encoding="utf-8")

  id_line       = f_id.readline()
  name_line     = f_name.readline()
  sentence_line = f_sentence.readline()

  id_list       = []
  name_list     = []
  sentence_list = []

  if label_flag == 'Y':
     while id_line:
        id_list.append(id_line.replace("\n",''))
        id_line = f_id.readline()

  if name_flag == 'Y':
     while name_line:
        name_list.append(',' + name_line.replace("\n",''))
        name_line = f_name.readline()

  if sentence_flag == 'Y':
     while sentence_line:
        sentence_list.append(',' + sentence_line.replace("\n",''))
        sentence_line = f_sentence.readline()

  for label, name, sentence in itertools.zip_longest(id_list, name_list, sentence_list, fillvalue=''):
     new_line = label + name + sentence + "\n"
     if new_line[0] ==  ',':
        new_line = new_line[1:]
     write_f.write(new_line)
  write_f.close()


'''ラベルを欠損値にする処理'''
def loss_process(flag, f_path):

  prev_label   = -99999
  this_label   = None
  file_count   = 0
  groups       = []
  updated_rows = []

  if flag != 'Y':
      return
  
  loss_rate = int(input("欠損値にする割合を0~100で入力。デフォルトは50:"))
  if loss_rate < 0 or 100 < loss_rate:
      loss_rate = 50
  loss_rate = loss_rate / 100
  
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

  f = open('./data/livedoor_news_corpus.txt', 'w', encoding='utf-8')
  for row in updated_rows:
      f.write(','.join(row)+"\n")
  f.close()


''' csvファイルで出力する処理 '''
def csv_process(path3):

  csv_list = []
  read_f   = open(path3, 'r', encoding="utf-8")
  line     = read_f.readline()

  while line:
     line = line.replace("\n", '')
     line = line.split(',')
     csv_list.append(line)
     line = read_f.readline()
  read_f.close()

  with open(path3.replace("txt", "csv"), 'w', encoding="utf-8", newline='') as f:
    writer = csv.writer(f)
    writer.writerows(csv_list)

  csv_list.clear()


''' tsvファイルで出力する処理 '''
def tsv_process(path3):
   
  tsv_list = []
  read_f   = open(path3, 'r', encoding="utf-8")
  line     = read_f.readline()

  while line:
     line = line.replace("\n", '')
     line = line.split(',')
     tsv_list.append(line)
     line = read_f.readline()
  read_f.close()

  with open(path3.replace("txt", "tsv"), 'w', encoding="utf-8", newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerows(tsv_list)

  tsv_list.clear()


if __name__ == "__main__":
    main()