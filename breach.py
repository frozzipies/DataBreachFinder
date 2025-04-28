import requests
from googlesearch import search
from bs4 import BeautifulSoup
import re
import os
import urllib.parse
import time

def google_search_jakarta_dork(domain):
    # Menerima input domain dari pengguna
    query = f"site:{domain} (filetype:xls OR filetype:xlsx OR filetype:pdf) NIK OR \"nomor telepon\" OR gaji OR username OR password"
    results = []
    try:
        # Menggunakan num_results dan sleep_interval (untuk googlesearch-python)
        for result in search(query, num_results=100, lang="id", sleep_interval=5):
            results.append(result)
    except Exception as e:
        print(f"Error saat melakukan pencarian: {str(e)}")
    
    return results

def download_files(search_results, directory):
    keywords = ['NIK', 'nomor telepon', 'gaji']
    regex_pattern = r'\b(?:' + '|'.join(keywords) + r')\b'

    # Membuat folder jika belum ada
    if not os.path.exists(directory):
        os.makedirs(directory)

    for url in search_results:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Cari semua link yang mengarah ke file Excel (xls/xlsx) atau PDF
            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href']
                anchor_text = link.get_text()

                # Filter hanya file Excel atau PDF
                if href.endswith('.xls') or href.endswith('.xlsx') or href.endswith('.pdf'):
                    # Filter berdasarkan kata kunci
                    if re.search(regex_pattern, href, re.IGNORECASE) or re.search(regex_pattern, anchor_text, re.IGNORECASE):
                        # Dapatkan URL lengkap file
                        file_url = urllib.parse.urljoin(url, href)

                        # Nama file
                        file_name = href.split("/")[-1]
                        file_path = os.path.join(directory, file_name)

                        # Unduh file
                        with open(file_path, 'wb') as f:
                            f.write(requests.get(file_url).content)

                        print(f"File '{file_name}' berhasil diunduh ke '{directory}'")

        except Exception as e:
            print(f"Error processing URL: {url}")
            print(str(e))

if __name__ == "__main__":
    # Minta input domain dari pengguna
    domain = input("Masukkan domain situs (misalnya jakarta.go.id): ")

    # Dapatkan hasil pencarian dari Google berdasarkan domain
    search_results = google_search_jakarta_dork(domain)
    
    if search_results:
        print("Hasil pencarian ditemukan:")
        for url in search_results:
            print(url)

        # Unduh file-file yang ditemukan
        download_files(search_results, "downloaded_files")
    else:
        print("Tidak ada hasil pencarian yang ditemukan.")
