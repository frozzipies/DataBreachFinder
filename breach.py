import requests
from googlesearch import search
from bs4 import BeautifulSoup
import re
import os
import urllib.parse

def google_search_jakarta_dork(target_domain):
    query = f"site:{target_domain} (filetype:xls OR filetype:xlsx OR filetype:pdf) NIK OR NIP OR \"nomor telepon\" OR gaji OR username OR password"
    results = search(query, num=100, pause=2)  # Mengambil sebanyak mungkin hasil pencarian

    return results

def download_files(search_results, directory):
    keywords = ['NIK', 'nomor telepon', 'gaji']
    regex_pattern = r'\b(?:' + '|'.join(keywords) + r')\b'

    for url in search_results:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Cari semua link yang mengarah ke file Excel (xls atau xlsx) atau PDF
            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href']
                anchor_text = link.get_text()

                # Filter hanya file Excel (.xls atau .xlsx) atau PDF
                if href.endswith('.xls') or href.endswith('.xlsx') or href.endswith('.pdf'):
                    # Filter berdasarkan teks anchor atau URL yang mengandung kata kunci
                    if re.search(regex_pattern, href, re.IGNORECASE) or re.search(regex_pattern, anchor_text, re.IGNORECASE):
                        # Dapatkan URL lengkap file
                        file_url = urllib.parse.urljoin(url, href)

                        # Unduh file
                        file_name = href.split("/")[-1]
                        file_path = os.path.join(directory, file_name)

                        with open(file_path, 'wb') as f:
                            f.write(requests.get(file_url).content)

                        print(f"File '{file_name}' berhasil diunduh ke '{directory}'")

        except Exception as e:
            print(f"Error processing URL: {url}")
            print(str(e))

# Prompt the user for their target domain
target_domain = input("Masukkan Target Kamu:")

# Contoh penggunaan:
search_results = google_search_jakarta_dork(target_domain)
print("Hasil pencarian ditemukan:")
for url in search_results:
    print(url)

# Unduh file-file Excel dan PDF dari hasil pencarian
download_files(search_results, "downloaded_files")

