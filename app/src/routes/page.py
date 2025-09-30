from flask import render_template
from app.routes import page_bp
from app.src.repositories.pengambilan_gambar import get_all_gambar_repository

@page_bp.route("/galeri")
def galeri_page():
    foto_rows = get_all_gambar_repository()
    return render_template("galeri.html", foto_rows=foto_rows)
