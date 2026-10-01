#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3

DB_PATH = "/storage/emulated/0/storybook/database/stories.db"

print("=" * 60)
print("🔧 إصلاح قاعدة البيانات")
print("=" * 60)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# عرض الأعمدة الحالية
c.execute("PRAGMA table_info(stories)")
cols = [row[1] for row in c.fetchall()]
print(f"\n📋 الأعمدة الحالية في stories:")
for col in cols:
    print(f"   - {col}")

# إضافة عمود reads إذا مو موجود
if "reads" not in cols:
    print("\n➕ إضافة عمود reads...")
    c.execute("ALTER TABLE stories ADD COLUMN reads INTEGER DEFAULT 0")
    print("   ✅ تمت الإضافة")
else:
    print("\n✅ عمود reads موجود مسبقاً")

# إضافة عمود rating إذا مو موجود
if "rating" not in cols:
    print("\n➕ إضافة عمود rating...")
    c.execute("ALTER TABLE stories ADD COLUMN rating REAL DEFAULT 4.8")
    print("   ✅ تمت الإضافة")
else:
    print("✅ عمود rating موجود مسبقاً")

# تحديث القيم الفارغة
c.execute("UPDATE stories SET reads = 0 WHERE reads IS NULL")
c.execute("UPDATE stories SET rating = 4.8 WHERE rating IS NULL")

conn.commit()
conn.close()

print("\n" + "=" * 60)
print("✅ انتهى الإصلاح! الآن شغّل app.py")
print("=" * 60)