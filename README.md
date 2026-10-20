# Task Tracker API (devsecops-p5-0110225139)

## 1. Nama Aplikasi & Fungsi
**Task Tracker API** adalah REST API sederhana untuk mengelola daftar tugas
(tambah, lihat, filter berdasarkan status, ubah status, hapus). Data disimpan di SQLite.

## 2. Bahasa / Framework
- Python 3.12
- Flask 3 (web framework), SQLite (database), pytest + pytest-cov (testing)
- Bandit (SAST)

## 3. Cara Menjalankan
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py                    # server di http://127.0.0.1:5000
```
Contoh pemakaian:
```bash
curl -X POST http://127.0.0.1:5000/tasks -H "Content-Type: application/json" -d '{"title":"Belajar DevSecOps"}'
curl http://127.0.0.1:5000/tasks
curl -X PATCH http://127.0.0.1:5000/tasks/1 -H "Content-Type: application/json" -d '{"status":"done"}'
curl -X DELETE http://127.0.0.1:5000/tasks/1
```
Menjalankan test:
```bash
python -m pytest --cov=app
```

## 4. Overview Pipeline CI/CD
Workflow: `.github/workflows/devsecops.yml`, terpicu pada **push** dan **pull_request** ke branch `main`.

| Job | Fungsi |
|-----|--------|
| `build` | Install dependency, jalankan unit test, **Quality Gate**: coverage minimal 70% |
| `sast-scan` (`needs: build`) | Jalankan **Bandit** (SAST), unggah laporan JSON sebagai artifact, **Quality Gate**: gagal jika ada temuan severity & confidence MEDIUM/HIGH |

Kedua job berjalan di `ubuntu-latest`.

## Struktur
```
app/        config.py, models.py, validators.py, routes.py, __init__.py
tests/      test_validators.py, test_routes.py
run.py      entry point
```
