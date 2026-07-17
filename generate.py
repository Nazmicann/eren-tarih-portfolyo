import os
import re
import shutil
import markdown

# Çıktı klasörlerini garantiye alalım
os.makedirs('output', exist_ok=True)

# --- RESİMLERİ OTOMATİK KOPYALAMA MOTORU ---
if os.path.exists('images'):
    if os.path.exists('output/images'):
        shutil.rmtree('output/images')
    shutil.copytree('images', 'output/images')
else:
    os.makedirs('output/images', exist_ok=True)

# Şablonları oku
with open('templates/index.html', 'r', encoding='utf-8') as f:
    index_template = f.read()

with open('templates/admin/index.html', 'r', encoding='utf-8') as f:
    admin_template = f.read()

articles_html = ""
content_dir = 'content'

# --- LOG DEDEKTİFİ BAŞLIYOR ---
print(f"🔍 Kontrol ediliyor: '{content_dir}' klasörü var mı?")

if os.path.exists(content_dir):
    files = os.listdir(content_dir)
    print(f"📂 '{content_dir}' klasörü bulundu! İçindeki tüm dosyalar: {files}")
    
    # Dosyaları listele ve tarihe göre sırala
    for filename in sorted(files, reverse=True):
        if filename.endswith('.md'):
            print(f"📖 İşleniyor: {filename}")
            filepath = os.path.join(content_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                raw_content = f.read()
            
            title = filename.replace('.md', '').replace('-', ' ').upper()
            date = "2026-07-17"  # Varsayılan tarih
            body_markdown = raw_content
            
            normalized_content = raw_content.replace('\r\n', '\n').strip()
            
            if normalized_content.startswith('---'):
                parts = normalized_content.split('---', 2)
                if len(parts) >= 3:
                    metadata = parts[1]
                    body_markdown = parts[2]
                    
                    title_match = re.search(r'^title:\s*(.*)$', metadata, re.MULTILINE)
                    if title_match:
                        title = title_match.group(1).strip().strip('"').strip("'")
                    
                    date_match = re.search(r'^date:\s*(.*)$', metadata, re.MULTILINE)
                    if date_match:
                        date = date_match.group(1).strip().strip('"').strip("'")
                        if len(date) >= 10:
                            date = date[:10]
            
            body_html = markdown.markdown(body_markdown.strip())
            
            articles_html += f"""
            <div class="border border-amber-900/30 bg-slate-900/40 backdrop-blur-sm p-6 rounded-xl shadow-xl hover:border-amber-500/40 transition duration-300 mb-6">
                <h2 class="text-2xl font-bold text-amber-500 font-cinzel mb-2 tracking-wide uppercase">{title}</h2>
                <div class="text-sm text-slate-400 font-lora italic mb-4">
                    Tarih: {date}
                </div>
                <div class="text-slate-300 font-lora leading-relaxed prose prose-invert max-w-none">
                    {body_html}
                </div>
            </div>
            """
else:
    print(f"❌ HATA: '{content_dir}' adında bir klasör sunucuda YOK!")

# Şablonda placeholder kontrolü
if '{{articles}}' in index_template:
    print("✅ Şablondaki '{{articles}}' etiketi başarıyla doğrulandı.")
else:
    print("⚠️ UYARI: 'templates/index.html' içinde '{{articles}}' kelimesi bulunamadı! Değiştirme yapılamıyor.")

# Değişiklikleri enjekte et
output_index = index_template.replace('{{articles}}', articles_html)
with open('output/index.html', 'w', encoding='utf-8') as f:
    f.write(output_index)

# Admin paneli klasör yapısını koru
os.makedirs('output/admin', exist_ok=True)
with open('output/admin/index.html', 'w', encoding='utf-8') as f:
    f.write(admin_template)

if os.path.exists('templates/admin/config.yml'):
    with open('templates/admin/config.yml', 'r', encoding='utf-8') as f:
        config_data = f.read()
    with open('output/admin/config.yml', 'w', encoding='utf-8') as f:
        f.write(config_data)

print("🚀 Altyapı tamamen yenilendi, işlem bitti!")