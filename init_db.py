#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3

# ============================================
#  مسار قاعدة البيانات
# ============================================
BASE_DIR = "/storage/emulated/0/storybook"
DB_PATH = os.path.join(BASE_DIR, "database", "stories.db")

# تأكد أن المجلد موجود
if not os.path.exists(BASE_DIR):
    print(f"❌ المجلد غير موجود: {BASE_DIR}")
    exit(1)

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def create_database():
    """إنشاء قاعدة البيانات والجداول"""
    print("=" * 50)
    print("🛠️  جاري إنشاء قاعدة البيانات...")
    print("=" * 50)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # ----------- جدول القصص -----------
    c.execute("""
        CREATE TABLE IF NOT EXISTS stories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT,
            description TEXT,
            cover TEXT,
            created_at TEXT
        )
    """)
    print("✅ جدول stories تم إنشاؤه")

    # ----------- جدول الفصول -----------
    c.execute("""
        CREATE TABLE IF NOT EXISTS chapters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            story_id INTEGER,
            chapter_num INTEGER,
            title TEXT,
            content TEXT,
            FOREIGN KEY (story_id) REFERENCES stories(id)
        )
    """)
    print("✅ جدول chapters تم إنشاؤه")

    # ----------- إضافة 3 قصص تجريبية -----------
    c.execute("SELECT COUNT(*) FROM stories")
    count = c.fetchone()[0]

    if count == 0:
        print("\n📚 إضافة القصص التجريبية...")
        add_sample_stories(c)
        print("✅ تمت إضافة 3 قصص")
    else:
        print(f"\n⚠️  يوجد {count} قصة مسبقاً - لن نضيف المزيد")

    conn.commit()
    conn.close()

    print("\n" + "=" * 50)
    print("✅ قاعدة البيانات جاهزة!")
    print(f"📁 المسار: {DB_PATH}")
    print("=" * 50)


def add_sample_stories(c):
    """إضافة 3 قصص تجريبية"""

    # ============ قصة 1 ============
    c.execute("""
        INSERT INTO stories (title, author, category, description, cover, created_at)
        VALUES (?, ?, ?, ?, ?, datetime('now'))
    """, (
        "رحلة في الصحراء",
        "martda",
        "مغامرة",
        "مغامرة شيقة عبر رمال الصحراء الكبرى، يبحث فيها بطلنا عن كنز مفقود منذ قرون.",
        "https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=500&q=80"
    ))
    sid1 = c.lastrowid

    chapters1 = [
        (sid1, 1, "البداية",
"""كانت الشمس تتوسط السماء حين وصل سامي إلى حافة القرية.

رمل ذهبي يمتد إلى ما لا نهاية، والصمت يلف المكان كأن الزمن توقف.

في يده خريطة قديمة ورثها عن جده، عليها علامة حمراء تشير إلى مكان في قلب الصحراء.

قال له جده ذات يوم:
'يا سامي، هناك كنز لا يعرفه أحد. لكن الطريق ليس سهلاً.'

أخذ سامي نفساً عميقاً، ثم خطا أول خطوة."""),
        (sid1, 2, "الغريب",
"""بعد ساعتين، ظهر على الأفق رجل يجلس على صخرة.

'السلام عليكم'، قال سامي.

رفع الغريب رأسه.

'إلى أين؟' سأل.

'أبحث عن الكنز'، أجاب سامي بصدق.

ابتسم الغريب ابتسامة غامضة، ثم أشار إلى الجنوب.

'كل من يبحث عن الكنز يعرف أن الطريق يمر بثلاث عواصف.'

ثم اختفى.

وبقيت قطعة قماش صغيرة على الصخرة، عليها رقم: 7."""),
    ]
    for ch in chapters1:
        c.execute(
            "INSERT INTO chapters (story_id, chapter_num, title, content) VALUES (?, ?, ?, ?)",
            ch
        )

    # ============ قصة 2 ============
    c.execute("""
        INSERT INTO stories (title, author, category, description, cover, created_at)
        VALUES (?, ?, ?, ?, ?, datetime('now'))
    """, (
        "الحلم",
        "قلم حر",
        "خيال علمي",
        "في زمنٍ لا أحد يحلم فيه، يحاول شاب أن يستعيد القدرة على الحلم قبل أن تفنى البشرية.",
        "https://images.unsplash.com/photo-1532012197267-da84d127e765?w=500&q=80"
    ))
    sid2 = c.lastrowid

    chapters2 = [
        (sid2, 1, "المدينة الرمادية",
"""في مدينة اسمها 'نظام'، لا يوجد وقت للأحلام.

يستيقظ الناس في الساعة السادسة تماماً، يعملون تسع ساعات، يعودون إلى منازلهم.

لا أحد يسأل: لماذا؟ لا أحد يسأل: ماذا لو؟

كل شيء مخطط. كل شيء معروف. كل شيء... ميت.

لكن آدم كان مختلفاً.

كل ليلة، قبل أن ينام، كان يغمض عينيه ويرى أشياء لا يراها الآخرون.

'يا أمي، حلمت البارحة أنني أطير.'

لكن والدته قالت ببرود:
'الأحلام ممنوعة يا آدم.'"""),
        (sid2, 2, "قانون الأحلام",
"""ذهب آدم إلى المكتبة.

الرجل العجوز الذي يديرها، اسمه سليم، كان آخر من يعرف عن الزمن القديم.

'لماذا نحن لا نحلم؟'

نظر سليم إلى الباب، ثم خفض صوته:

'قبل أربعين سنة، كانت الأحلام موجودة. لكن الحكومة أدركت أن الأحلام تجعل الناس يفكرون.'

'ماذا فعلوا؟'

'بنوا جهازاً يرسل موجات في الهواء كل ليلة، تمنع العقل من الأحلام.'

أخرج سليم كتاباً قديماً من رفٍ خفي.

'خذ هذا الكتاب. لكن اقرأه في النهار فقط.'"""),
    ]
    for ch in chapters2:
        c.execute(
            "INSERT INTO chapters (story_id, chapter_num, title, content) VALUES (?, ?, ?, ?)",
            ch
        )

    # ============ قصة 3 ============
    c.execute("""
        INSERT INTO stories (title, author, category, description, cover, created_at)
        VALUES (?, ?, ?, ?, ?, datetime('now'))
    """, (
        "القمر المكسور",
        "أمل",
        "خيال",
        "قصة عن فتاة صغيرة تحاول إصلاح القمر بعد أن تشقق، لتعيد النور إلى مدينتها الحزينة.",
        "https://images.unsplash.com/photo-1532693322450-2cb5c511067d?w=500&q=80"
    ))
    sid3 = c.lastrowid

    chapters3 = [
        (sid3, 1, "الليلة التي اختفى فيها الضوء",
"""في مدينة صغيرة، يسكن الناس بحزن دائم.

لماذا؟ لأن القمر تشقق.

ذات ليلة، رأى الجميع شقاً طويلاً يعبر وجه القمر. ثم شقاً آخر. ثم ثالثاً.

في الصباح، لم يعد القمر ساطعاً. أصبح باهتاً، رمادياً، ميتاً.

لكن نورة، الفتاة ذات العشر سنوات، رفضت أن تستسلم.

'أنا سأصلح القمر'، قالت.

ضحك الجميع. حتى أمها.

'كيف؟'
'لا أعرف بعد. لكنني سأعرف.'"""),
        (sid3, 2, "الرحلة إلى الجبل",
"""خرجت نورة من بيتها ليلاً، وحملت معها حقيبة فيها: خيط، إبرة، وشمعة.

في طريقها، التقت بقطة عرجاء.

'إلى أين يا صغيرة؟'
'إلى القمر.'
'القمر بعيد. لن تصلي.'
'سأصل. أو سأموت وأنا أحاول.'

أعجبت القطة بالعزيمة، فمشت معها.

وصلت نورة إلى جبل.

في الأعلى، وجدت شيئاً لم تتوقعه: كهفاً من نور.

وعلى مدخل الكهف، رجل عجوز يجلس مبتسماً.

'أخيراً، وصلتِ'، قال."""),
    ]
    for ch in chapters3:
        c.execute(
            "INSERT INTO chapters (story_id, chapter_num, title, content) VALUES (?, ?, ?, ?)",
            ch
        )


# ============================================
#  تشغيل السكريبت
# ============================================
if __name__ == "__main__":
    create_database()