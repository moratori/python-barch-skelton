![coverage](coverage.svg)

# Python Batch System Skelton

## 1. 概要

古式ゆかしいサーバーサイドのバッチアプリケーションをPythonで実装するとき用の
オレオレフレームワークです。

次のような機能を提供するのが目的です。

* コンフィグの読み込み
* ロガーのセットアップ
* DBセッションの管理
* キャッシュデータの管理
* 多重起動防止
* 処理のタイムアウト設定

データパイプラインやバッチ処理順序の定義•可視化の提供は目的としておらず、適切なジョブスケジューラ
（例えば、Rundeck、Hinemos、JobScheduler）を用いることで実現することを想定します。

## 2. 前提

Pipenvが利用できることを前提とします。ない場合はpipなどでインストールします。

```
$ pip3 install --user pipenv
```

## 3. 使い方

### 3.1. 初期構築

最新版を取得します

```
$ wget https://github.com/moratori/python-batch-skelton/archive/refs/tags/v1.0.0.zip
$ unzip v1.0.0.zip
```

プロジェクト名を変更し、依存関係をインスールします。

```
$ mv python-batch-skelton-1.0.0 sample
$ cd sample && pipenv install
```

### 3.2. 実行スクリプトの作成

src直下に実行権限を付けたスクリプト(main_から始まる)を作成します。
内容は次の通りです。

```
#!/usr/bin/env python3

"""
docstring
"""

from typing import Any
import common.framework.application.batchbaseapplication as appframe

global LOGGER


class Application(appframe.BatchBaseApplication):

    def __init__(self) -> None:
        super().__init__(__name__, __file__)

    def run_application(self) -> None:
        print("hello, world")


if __name__ == "__main__":
    app = Application()
    LOGGER = app.create_toplevel_logger()
    app.start()
```

最低以下のメソッドを実装する必要があります。
* run_application

`run_application`メソッドにメインの処理を実装します。
`start`メソッドを呼ぶことで、処理を実行することができます。

### 3.3. 起動

`bin`配下にある、`runapp.sh`の引数に実行スクリプトのファイル名を渡すことで起動します。

```
$ ./bin/runapp.sh main_application
hello, world
```

### 3.3. コンフィグの読み込み

`conf`配下にある、次の2つのコンフィグファイル(TOML形式)を自動で読み込みます。

* common.ini
* 実行スクリプトと同名のコンフィグファイル(例えば、main_application.ini)

読み込んだコンフィグの内容は次の形で参照します。

```
self.conf.common.logging.loglevel
self.conf.self.application.timeout_duration
```

### 3.4 ロギング

実行スクリプトのロガーのセットアップについては、BatchBaseApplication
を継承したクラスの`create_toplevel_logger`を呼ぶことで行います。

```
global LOGGER

...

if __name__ == "__main__":
    app = Application()
    LOGGER = app.create_toplevel_logger()
```

実行スクリプトから別途importする各種モジュール(BatchBaseApplicationを継承しない)については、以下の通り`logging.getLogger`を呼ぶことで通常通りロガーをセットアップします。

```
from logging import getLogger

LOGGER = getLogger(__name__)
```

ログは、`logs`配下に実行スクリプトファイル名と同じ名前で生成されます。

```
$ tail -n10 ./logs/main_application.log
2021-04-03 20:11:48,209 [INFO] common.framework.application.batchbaseapplication start start application
2021-04-03 20:11:48,214 [INFO] common.framework.application.batchbaseapplication start start main routine
2021-04-03 20:11:48,214 [INFO] common.framework.application.batchbaseapplication start end main routine
2021-04-03 20:11:48,214 [INFO] common.framework.application.batchbaseapplication start end application successfully
```

### 3.5 DBセッションの管理

MySQLサーバーへ接続する場合、`MySQLApplication`を継承した実行スクリプトを作成します。

なお、DBへの接続先情報は、`conf`ディレクトリ配下の`common.ini`に記載しておく必要があります。

```
from common.framework.dbsession import local_session

...

    def get_something_record(self) -> List[Something]:
        with local_session(self.thread_local_session_maker) as session:
            ret = session.query(Something).all()
        return ret

    def run_application(self, **args: Any) -> None:
        print("hello, world")
        for each in self.get_something_record():
            print("id: %s" % each.some_id)
            print("val: %s" % each.some_value)

...
```

`thread_local_session_maker`は、スレッド毎に一意なDBセッションを生成する仕組みです。これを`local_session`に渡すことで、セッションを得ます。


コンテキストマネージャ`local_session`内で、データの更新を行ってもデフォルトではロールバックします。`with`句を抜ける時にデータをコミットする場合は、`commit_on_exit`を`True`にします。

```
with local_session(self.thread_local_session_maker,
                   commit_on_exit=True) as session:
    pass
```

### 3.8. 処理のタイムアウト設定

`run_application`メソッドにはタイムアウトを設けることができます。
`common.ini`または実行スクリプト用のコンフィグに以下の設定を記載します。
双方の設定ファイルに記載がある場合は、実行スクリプト用のコンフィグに記載のある設定を優先します。

```
[application]
timeout_duration=300
```
