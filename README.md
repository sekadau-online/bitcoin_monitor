# 🚨 Bitcoin Transaction Monitor

**Bitcoin Monitor** adalah alat pemantau transaksi keluar (outgoing transactions) dari wallet Bitcoin secara **real-time**. Setiap pergerakan dana akan langsung dikirim ke email Anda sebagai **peringatan kritis**. Sempurna untuk digunakan oleh pengguna yang ingin memantau keamanan aset mereka atau sekadar ingin tahu pergerakan saldo di wallet tertentu.

---

## ✨ Fitur Utama

* 🔍 **Deteksi Transaksi Keluar**: Pantau setiap pergerakan dana dari wallet Bitcoin yang Anda tentukan.
* 💱 **Konversi Otomatis**: Jumlah ditampilkan dalam format BTC dengan 8 desimal.
* 🔗 **Tautan Explorer**: Cek langsung transaksi di [Blockchain.com](https://www.blockchain.com/explorer).
* ⏱ **Pemantauan Real-time**: Periksa transaksi baru setiap 5 menit (bisa diatur).
* 📬 **Notifikasi Email**: Kirim pemberitahuan otomatis ke email Anda jika ada transaksi.

---

## ⚙️ Instalasi

1. **Clone repo ini:**

```bash
git clone https://github.com/sekadau-online/bitcoin-monitor.git
cd bitcoin-monitor
```

2. **Install dependensi:**

```bash
pip install -r requirements.txt
```

3. **Buat file konfigurasi `.env`:**

```ini
# Bitcoin Configuration
BITCOIN_WALLET=your_bitcoin_wallet_address

# Email Configuration
EMAIL_USER=your@email.com
EMAIL_PASS=your_email_app_password
EMAIL_TO=recipient@email.com

# Optional (default: 300 detik / 5 menit)
CHECK_INTERVAL=300
```

---

## ▶️ Menjalankan Monitor

```bash
python3 bitcoin_monitor.py
```

> Pastikan koneksi internet aktif dan informasi email sudah benar agar bisa mengirim notifikasi.

---

## 📬 Contoh Email Peringatan

```
CRITICAL: Bitcoin movement detected from monitored wallet!

Transaction Hash: 1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u
Blockchain: Bitcoin
From: 1F5i3twCN6rMKu6KZRbNYySgP8TwzKrWgh
Amount: 0.12500000 BTC
Date: 2025-06-30 16:45:22
Confirmations: 3

Verify transaction:
https://www.blockchain.com/explorer/transactions/btc/1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u
```

---

## 🤝 FAQ

**Apakah proyek ini gratis?**
✅ Ya! Proyek ini open-source dan bisa digunakan siapa saja.

**Apakah bisa memantau lebih dari 1 wallet?**
🔜 Belum, tetapi fitur ini direncanakan untuk versi selanjutnya.

**Apakah email saya aman?**
📨 Gunakan password aplikasi (App Password) untuk keamanan maksimal, terutama jika menggunakan Gmail.

---

## ☕ Donasi

Jika Anda merasa terbantu dengan alat ini, pertimbangkan untuk memberikan donasi agar proyek ini terus berkembang:

| Coin         | Wallet Address                               |
| ------------ | -------------------------------------------- |
| **Bitcoin**  | `1F5i3twCN6rMKu6KZRbNYySgP8TwzKrWgh`         |
| **Ethereum** | `0x1F491f5d86b78865cD20379FC47FaA04E4f5ceB3` |
| **Litecoin** | `LZJfK7F2Sm6QahnUjZafpzWSbLqE7mp2NK`         |
| **Verus**    | `RPMu8QpUxvevPuTX2baVeVmt9PvYfWjURN`         |

🙏 Setiap kontribusi, sekecil apa pun, sangat berarti!

---

## 👨‍💼 Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE). Bebas digunakan, dimodifikasi, dan dikembangkan.

---

## 📣 Hubungi

Jika Anda memiliki pertanyaan, ide fitur, atau ingin berkontribusi, silakan buka [Issue](https://github.com/sekadau-online/bitcoin-monitor/issues) atau kirim email ke: **[fauzan.skd@gmail.com](mailto:fauzan.skd@gmail.com)**
