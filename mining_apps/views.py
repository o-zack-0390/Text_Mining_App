import os
from django.views                   import View
from django.shortcuts               import render, redirect
from django.contrib.auth            import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http                    import HttpResponse, Http404
from importlib                      import reload
from mining_apps.modules            import txt_mining, db_save, db_delete


class MainView(View):

    def __init__(self):
        super().__init__()
        self.input_type1 = ''
        self.input_type2 = ''
        self.input_type3 = ''
        self.input_type4 = ''
        self.input_type5 = ''
        self.input_type6 = ''
        self.upload_file = None
        self.file_exists = False


#   リクエストの送信元によって異なるテンプレートをレンダリング
    def get(self, request):

        if request.user.is_authenticated:
            return render(request, "main.html", {'file_exists': self.file_exists})
        
        else:
            return render(request, "login.html")


    def post(self, request):
        global format_type

        self.input_type1 = request.POST.get('input_type1', '分かち書きのみ')
        self.input_type2 = request.POST.get('input_type2', 'txt')
        self.input_type3 = request.POST.get('input_type3', 'N')
        self.input_type4 = request.POST.get('input_type4', 'N')
        self.input_type5 = request.POST.get('input_type5', 'N')
        self.input_type6 = request.POST.get('input_type6', 'N')
        format_type      = self.input_type2

        if 'file' in request.FILES:
            self.upload_file = request.FILES['file']

#       txt_mining.py を実行
        txt_mining.main(self.input_type1,\
                        self.input_type2,\
                        self.input_type3,\
                        self.input_type4,\
                        self.input_type5,\
                        self.input_type6,\
                        self.upload_file)
        reload(txt_mining)

#       ファイルが存在する場合は、file_existsフラグをTrueに設定する
        file_path = os.path.abspath('livedoor_news_corpus.txt').replace("txt", self.input_type2)
        
        if os.path.exists(file_path):
            self.file_exists = True

        else:
            self.file_exists = False
        
        return render(request, "main.html", {'file_exists': self.file_exists})


    def login_view(request):

#       フォームからユーザー名とパスワードを取得する
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

#           ユーザー情報を検証する
            user = authenticate(request, username=username, password=password)

#           認証に失敗した場合、エラーメッセージを表示する
            if user is None:
                error_message = 'ユーザー名またはパスワードが間違っています。'
                return render(request, 'login.html', {'error_message': error_message})
                
#           認証に成功した場合、セッションを開始する
            else:
                login(request, user)
                return redirect('main')
        
#       GETリクエストの場合、ログインページを表示する
        else:
            return render(request, 'login.html', {})


    def logout_view(request):
        txt_mining.delete_file() # 容量を圧迫するためファイルを削除
        logout(request)          # ログアウト
        return redirect('login') # ログインページに遷移させる


    @login_required
    def download_file(request):
        global format_type

        file_path = os.path.abspath('livedoor_news_corpus.txt').replace("txt", format_type)

        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        else:
            error_msg = f"{file_path} does not exist"
            return HttpResponseServerError(error_msg)


    @login_required
    def insert(request):

        if request.method == 'POST':

            if 'file' not in request.FILES:
                message = "ファイルが選択されていません。"
                context = {'message': message}
                return render(request, 'insert.html', context)

            file             = request.FILES['file']
            valid_extensions = ['.txt', '.csv']
            file_extension   = os.path.splitext(file.name)[1]

            if not file_extension.lower() in valid_extensions:
                message = "無効なファイル形式です。txt,csv形式のファイルをアップロードしてください。"
                context = {'message': message}
                return render(request, 'insert.html', context)

            db_save.main(file)
            message = "データを登録しました。"
            context = {'message': message}
            return render(request, 'insert.html', context)
        
        else:
            return render(request, 'insert.html')


    @login_required
    def delete(request):

        if request.method == 'POST':

            model_type = request.POST.get('model', '')
            db_delete.main(model_type)
            
            if   model_type == 'LivedoorNewscorpus':
                message = "LivedoorNewscorpusのデータを削除しました。"

            elif model_type == 'fetch_20newsgroups':
                message = "fetch_20newsgroupsのデータを削除しました。"

            else:
                message = "モデルが指定されていません。"
            
            context = {'message': message}
            return render(request, 'delete.html', context)
        
        else:
            return render(request, 'delete.html')
        
format_type = None