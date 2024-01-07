# カスタムコマンドの実装

from django.core.management.base import BaseCommand
from ecapp.models import PromoCodeModel
import random
import string


class Command(BaseCommand):
    help = 'Generate a new promotion code'

    def handle(self, *args, **kwargs):
        # プロモーションコードの作成
        for _ in range(10):
            # 大文字、小文字、数値から7つ取り出す
            code = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=7))
            # 100-1000の間で1つ取り出す
            discount = random.randint(100, 1000)

            PromoCodeModel.objects.create(code=code, discount=discount)

        print('Successfully generated promotion code')
