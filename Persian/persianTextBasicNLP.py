from __future__ import unicode_literals
from hazm import *

normalizer = Normalizer()
normalizer.normalize('اصلاح نويسه ها و استفاده از نیم‌فاصله پردازش را آسان مي كند')

print(sent_tokenize('ما هم برای وصل کردن آمدیم! ولی برای پردازش، جدا بهتر نیست؟'))
print(word_tokenize('ولی برای پردازش، جدا بهتر نیست؟'))

stemmer = Stemmer()
print(stemmer.stem('کتاب‌ها'))
lemmatizer = Lemmatizer()
print(lemmatizer.lemmatize('می‌روم'))


# ---------------- POS Tagging Ex --------
tagger = POSTagger(model='Res/resources/postagger.model')
print(tagger.tag(word_tokenize('ما بسیار کتاب می‌خوانیم')))

# --------------- Chunker Ex ----------
chunker = Chunker(model='Res/resources/chunker.model')

input_text = """عرض سلام و احترام

۵۶ متر لوکس موقعیت اداری
موقعیت میدان کاج
لابی و نگهبانی ۲۴ ساعته
تابلو خور
ساختمان ۱۰۰ درصد اداری
دولاین آسانسور
پارکینگ
سالن اجتماعات
یک اتاق
کف پارکت
آبدارخانه
سند تک برگ

◾◼موارد مشابه را از ما بخواهید◼◾

لطفا فقط تماس بگیرید
از ساعت 8 صبح تا 12 شب

کارشناس اداری
 رحیمی  09127659558

****گروه مشاورین املاک بزرگ مثلث****
آدرس دفتر : بلوار دادمان تقاطع حسن سیف
تلفن دفتر : ۸۸۵۹۱۵۰۰ داخلی ۳۵۶"""

words = word_tokenize(input_text)
print(words)
simplified_str = ' '.join(words)
print(simplified_str)

print('\n\n\n')

tagged = tagger.tag(words)
print(tagged)
print(tree2brackets(chunker.parse(tagged)))


# parser = DependencyParser(tagger=tagger, lemmatizer=lemmatizer)
# parser.parse(word_tokenize('زنگ‌ها برای که به صدا درمی‌آید؟'))
