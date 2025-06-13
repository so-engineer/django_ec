# Django ECサイト 🛍️

このプロジェクトは、DjangoとPostgreSQLを使用して構築されたECサイトアプリケーションです。

## 特徴

Django ECサイトは、シンプルで使いやすいECサイトを提供するWebアプリケーションです。Djangoの強力な機能とPostgreSQLのデータベース機能を活用し、堅牢で保守性の高いアプリケーションを実現しています。

主な機能：
- PostgreSQLによる堅牢なデータ管理
- Dockerによる開発環境の統一

## 技術スタック

- Python
- Django
- PostgreSQL
- Docker & Docker Compose

## セットアップ

1. リポジトリのクローン

```bash
git clone https://github.com/so-engineer/django_ec
```

2. .env.templateをコピーし.envファイルの作成

- SECRET_KEYの生成方法については[こちら](https://noauto-nolife.com/post/django-secret-key-regenerate/)を参照してください。

3. Dockerコンテナの起動
```bash
docker-compose up -d
```

4. 動作確認
ブラウザで[localhost:3001](http://localhost:3001)にアクセスし、Homeが表示されることを確認してください。

## 管理画面から商品登録、更新、削除
スーパーユーザーを作成し、管理画面から商品登録、更新、削除が可能です。
```bash
python manage.py createsuperuser
```

## プロジェクト構造

```
.
├── config/            # Djangoプロジェクト設定
├── ecapp/             # メインアプリケーション
├── media/             # アップロードされたメディアファイル
├── static/            # 静的ファイル
├── Dockerfile         # Dockerイメージ定義
├── docker-compose.yml # Docker Compose設定
├── requirements.txt   # Pythonパッケージ依存関係
├── manage.py          # Djangoプロジェクト管理スクリプト
└── README.md          # プロジェクトドキュメント
```

## デプロイ

本プロジェクトはHerokuへのデプロイに対応しています：
- Procfile: Herokuデプロイ設定
- runtime.txt: Pythonランタイム指定
- whitenoise: 静的ファイル配信
- django-cloudinary-storage: クラウドストレージ連携

## セキュリティ

- 本番環境では適切なセキュリティ設定を行ってください