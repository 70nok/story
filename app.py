#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, abort

BASE_DIR = "/storage/emulated/0/storybook"
DB_PATH = os.path.join(BASE_DIR, "database", "stories.db")

if not os.path.exists(BASE_DIR):
    print(f"❌ المجلد غير موجود: {BASE_DIR}")
    exit(1)

if not os.path.exists(DB_PATH):
    print(f"❌ قاعدة البيانات غير موجودة: {DB_PATH}")
    print("👉 شغّل init_db.py أولاً")
    exit(1)

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
)
app.secret_key = "storybook-secret-2024"

APP_NAME = "مكتبة القصص"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_all_stories():
    conn = get_db()
    stories = conn.execute("SELECT * FROM stories ORDER BY id DESC").fetchall()
    conn.close()
    return stories


def get_story(sid):
    conn = get_db()
    s = conn.execute("SELECT * FROM stories WHERE id = ?", (sid,)).fetchone()
    conn.close()
    return s


def get_chapters(sid):
    conn = get_db()
    chapters = conn.execute(
        "SELECT id, chapter_num, title FROM chapters WHERE story_id = ? ORDER BY chapter_num",
        (sid,)
    ).fetchall()
    conn.close()
    return chapters


def get_chapter(cid):
    conn = get_db()
    ch = conn.execute("SELECT * FROM chapters WHERE id = ?", (cid,)).fetchone()
    conn.close()
    return ch


def get_categories():
    conn = get_db()
    cats = conn.execute("SELECT DISTINCT category FROM stories WHERE category IS NOT NULL").fetchall()
    conn.close()
    return sorted([c[0] for c in cats])


def increment_reads(sid):
    conn = get_db()
    conn.execute("UPDATE stories SET reads = COALESCE(reads, 0) + 1 WHERE id = ?", (sid,))
    conn.commit()
    conn.close()


@app.context_processor
def inject_globals():
    return {
        "app_name": APP_NAME,
        "year": datetime.now().year,
        "categories": get_categories(),
    }


@app.route("/")
def home():
    stories = get_all_stories()
    return render_template("home.html", stories=stories, title="الرئيسية")


@app.route("/story/<int:sid>")
def story_page(sid):
    s = get_story(sid)
    if not s:
        abort(404)
    chapters = get_chapters(sid)
    return render_template("story.html", story=s, chapters=chapters, title=s["title"])


@app.route("/read/<int:cid>")
def read_page(cid):
    ch = get_chapter(cid)
    if not ch:
        abort(404)

    s = get_story(ch["story_id"])
    chapters = get_chapters(ch["story_id"])

    chapter_ids = [c["id"] for c in chapters]
    try:
        idx = chapter_ids.index(cid)
        prev_id = chapter_ids[idx - 1] if idx > 0 else None
        next_id = chapter_ids[idx + 1] if idx < len(chapter_ids) - 1 else None
    except ValueError:
        prev_id = next_id = None

    increment_reads(ch["story_id"])

    return render_template(
        "read.html",
        story=s,
        chapter=ch,
        chapters=chapters,
        prev_id=prev_id,
        next_id=next_id,
        title=ch["title"],
    )


@app.route("/category/<cat>")
def category_page(cat):
    conn = get_db()
    stories = conn.execute("SELECT * FROM stories WHERE category = ?", (cat,)).fetchall()
    conn.close()
    return render_template("home.html", stories=stories, current_category=cat, title=cat)


if __name__ == "__main__":
    print("=" * 55)
    print(f"📚 {APP_NAME} شغالة!")
    print("👉 افتح المتصفح: http://127.0.0.1:5050")
    print("=" * 55)

    app.run(host="0.0.0.0", port=5050, debug=True, use_reloader=False)