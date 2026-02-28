# 📝 Todo List App

Aplikasi Todo List sederhana menggunakan **FastAPI** + **Jinja2** + **PostgreSQL**.

## Fitur
- ✅ Tambah, edit, hapus todo
- ✔ Toggle status selesai/belum
- 📊 Statistik total, pending, selesai
- 🗑 Hapus semua tugas yang sudah selesai
- 📱 Responsive design

## Struktur Proyek
```
todo-app/
├── main.py               # FastAPI app + routes + models
├── templates/
│   ├── index.html        # Halaman utama
│   └── edit.html         # Halaman edit todo
├── static/
│   └── css/style.css     # Stylesheet
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## Cara Menjalankan

### Menggunakan Docker Compose (Direkomendasikan)
```bash
docker-compose up --build
```
Buka http://localhost:8000

### Manual (tanpa Docker)

1. Pastikan PostgreSQL berjalan, buat database `tododb`

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variable:
```bash
export DATABASE_URL="postgresql://postgres:password@localhost:5432/tododb"
```

4. Jalankan server:
```bash
uvicorn main:app --reload
```

Buka http://localhost:8000

## API Endpoints
| Method | URL | Deskripsi |
|--------|-----|-----------|
| GET | / | Halaman utama |
| POST | /add | Tambah todo baru |
| POST | /toggle/{id} | Toggle status selesai |
| GET | /edit/{id} | Halaman edit |
| POST | /edit/{id} | Simpan perubahan |
| POST | /delete/{id} | Hapus todo |
| POST | /delete-completed | Hapus semua yang selesai |
# todo-list-app
# todo-list-app
# todo-list-app
