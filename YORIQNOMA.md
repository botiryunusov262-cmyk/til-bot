# Til oʻrgatuvchi Telegram bot — oʻrnatish yoʻriqnomasi

## 1-qadam: Bot yaratish (Telegram orqali)
1. Telegram'da **@BotFather** botini toping va oching
2. `/newbot` buyrugʻini yuboring
3. Bot uchun nom bering (masalan: "Til Oʻrgatuvchi")
4. Bot uchun username bering — oxiri "bot" bilan tugashi kerak (masalan: `tilorgatuvchi_bot`)
5. BotFather sizga **TOKEN** beradi — bu kabi koʻrinadi:
   `123456789:AAExampleTokenHere1234567890`
   Bu tokenni hech kimga bermang, uni saqlab qoʻying.

## 2-qadam: Serverga joylashtirish (Railway orqali — bepul, telefondan ham qilsa boʻladi)

1. https://railway.app saytiga kiring, GitHub hisobingiz orqali roʻyxatdan oʻting
2. Avval bu fayllarni (`bot.py`, `words.json`, `requirements.txt`, `Procfile`) GitHub'da yangi repository (masalan `til-bot`) ichiga yuklang
   - Agar GitHub hisobingiz boʻlmasa, https://github.com saytida bepul oching (faqat email kerak)
   - Telefon brauzeridan repository yaratib, "Upload files" tugmasi orqali fayllarni yuklashingiz mumkin
3. Railway'da **"New Project" → "Deploy from GitHub repo"** tugmasini bosing, yuklagan repository'ni tanlang
4. Railway avtomatik `requirements.txt`ni oʻqib kerakli kutubxonalarni oʻrnatadi
5. **Variables** boʻlimiga oʻting va yangi environment variable qoʻshing:
   - Nomi: `BOT_TOKEN`
   - Qiymati: BotFather bergan token
6. **Deploy** tugmasini bosing — bir necha daqiqada bot ishga tushadi

## 3-qadam: Botni sinab koʻrish
Telegram'da botingizni toping (username orqali) va `/start` yuboring.

## Buyruqlar roʻyxati
- `/start` — botni ishga tushirish
- `/soz` — tasodifiy yangi ingliz soʻzi va misol
- `/viktorina` — 4 variantli test savoli
- `/statistika` — toʻgʻri/notoʻgʻri javoblar va oʻrganilgan soʻzlar soni

## Qanday rivojlantirish mumkin
- `words.json` faylga istalgancha yangi soʻz qoʻshishingiz mumkin (bir xil formatda: en, uz, example)
- Boshqa tillar uchun ham xuddi shu tuzilishda alohida fayl yasab, botga ulash mumkin
- Statistikani doimiy saqlash uchun keyinchalik bazaga (masalan SQLite) oʻtkazish tavsiya etiladi, hozircha xotirada saqlanadi va server qayta ishga tushganda tozalanadi

## Muhim eslatma
Railway'ning bepul rejasi oyiga cheklangan soatlik limitga ega (odatda ~500 soat/oy, kichik botlar uchun yetarli). Agar bot koʻp foydalanuvchiga xizmat qilsa, pullik rejaga oʻtish kerak boʻlishi mumkin.
