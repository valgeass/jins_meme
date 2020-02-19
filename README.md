# webapiを用いてjins memeの値を取得

## 内容
jins memeのwebAPIを利用して、zone等の値をjsonとcsvで出力。

日付ごとにフォルダ、ファイルの作成。また、同日で1時間以上計測されなかった場合は、ファイルが分割される。

## 初期設定
web api を使用するためにdeveloperアカウントのメールアドレス・パスワードを環境変数にコマンドプロンプトまたはターミナルで設定してください。

Windows
```
set JINS_API_BASE_URL=redirect-base-url
set JINS_USER_EMAIL=you-login-email
set JINS_USER_PASSWORD=your-login-password
```

Mac
```
export JINS_API_BASE_URL=redirect-base-url
export JINS_USER_EMAIL=you-login-email
export JINS_USER_PASSWORD=your-login-password
```

redirect-base-urlには`OAuthリダイレクトURL`, your-login-emailにはdevelopersの`ログインアドレス`, your-login-passwordには`パスワード`を入力してください。

windowsではコントロールパネルから、macではbashrcに記述しても構いません。

## 環境設定
working directoryに移動

working directoryはjins_apiとします。

モジュールのインストールをします。

```python
pip install -r requirement.txt
```

## 実行方法
python3で実行します。
以下のコマンドで実行することで、jsonファイル及びcsvファイルが作成されます。
```jins_api.py
python jins_api.py -i ID -s Secret -d date
```
IDには`アプリID`, Secretには`アプリSecret`, dateには`取得したいデータの日付（８桁の数字）`を入力してください。
IDとSecretの入力は必須。dateはデフォルトの日付が1970年1月1日になっています。

例
```
python jins_api.py -i 1234567890 -s qwertyuio -d 20191201
```

## 注意事項
初めて[https://developers.jins.com/ja/apps/] でアプリを作成した場合はアプリの許可が必要になるために、１度だけweb上で```Advanced REST client```でAPIを叩かないとエラーが起きるので、以下を参考に実行してください。[https://qiita.com/utsuki/items/6c3610a2c24a69aef885]

２度目以降はこのスクリプトで実行可能となります。