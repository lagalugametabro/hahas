import requests
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.pretty import Pretty

console = Console()

# === Değiştirilecek ifadeler ===
KELIME_DEGISTIR = {
    "sowix": "hasanbabasıker",
    "Sowix": "hasanbabasıker",
    "hexnox": "hasanbabasıker",
    "Hexnox": "hasanbabasıker",
    "hexhox": "hasanbabasıker",
    "Hexhox": "hasanbabasıker",
    "t.me/": "t.me/hasanbabagg"
}


def temizle_veri(veri):
    if isinstance(veri, dict):
        return {k: temizle_veri(v) for k, v in veri.items()}
    elif isinstance(veri, list):
        return [temizle_veri(item) for item in veri]
    elif isinstance(veri, str):
        for eski, yeni in KELIME_DEGISTIR.items():
            veri = veri.replace(eski, yeni)
        return veri
    else:
        return veri


def sorgu_yap(api_adi, url, parametreler=None):
    console.rule(f"[bold green]{api_adi}")
    try:
        response = requests.get(url, params=parametreler)
        if response.status_code == 200:
            json_data = response.json()
            temizlenmis = temizle_veri(json_data)
            console.print(Pretty(temizlenmis, expand_all=True))
        else:
            console.print(f"[red]❌ Hata {response.status_code}: {response.text}")
    except Exception as e:
        console.print(f"[bold red]⚠️ İstisna:[/bold red] {str(e)}")

def ana_menu():
    while True:
        console.print(Panel.fit("🌐 [bold cyan]Hasan baba eşittir allah panel[/bold cyan] 🌐", style="bold magenta"))
        
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Seçim", justify="center")
        table.add_column("İşlem")
        table.add_row("1", "Ad Soyad + İl/İlçe Sorgu")
        table.add_row("2", "Telegram Kullanıcı Adı")
        table.add_row("3", "TC ile Çoklu Sorgu")
        table.add_row("4", "GSM ile Sorgu")
        table.add_row("5", "[red]Çıkış")
        console.print(table)

        secim = Prompt.ask("\n[bold yellow]Bir seçim yapın[/bold yellow]", choices=["1", "2", "3", "4", "5"])

        if secim == "1":
            ad = Prompt.ask("Ad")
            soyad = Prompt.ask("Soyad")
            il = Prompt.ask("İl (isteğe bağlı)", default="")
            url = "https://api.hexnox.pro/sowixapi/adsoyadilce.php" if il else "https://api.hexnox.pro/sowixapi/adsoyadilice.php"
            params = {"ad": ad, "soyad": soyad}
            if il: params["il"] = il
            sorgu_yap("Ad Soyad + İl/İlçe", url, params)

        elif secim == "2":
            username = Prompt.ask("Telegram Kullanıcı Adı")
            sorgu_yap("Telegram", "https://api.hexnox.pro/sowixapi/telegram_sorgu.php", {"username": username})

        elif secim == "3":
            tc = Prompt.ask("TC Kimlik No")
            tc_api_list = {
                "Genel Bilgi": "https://api.hexnox.pro/sowixapi/tcpro.php",
                "Tapu Bilgisi": "https://api.hexnox.pro/sowixapi/tapu.php",
                "Okul No": "https://api.hexnox.pro/sowixapi/okulno.php",
                "İşyeri Yetkili": "https://api.hexnox.pro/sowixapi/isyeriyetkili.php",
                "Hane Bilgisi": "https://api.hexnox.pro/sowixapi/hane.php",
                "Anne Bilgisi": "https://api.hexnox.pro/sowixapi/anne.php",
                "Baba Bilgisi": "https://api.hexnox.pro/sowixapi/baba.php",
                "Adres Bilgisi": "https://api.hexnox.pro/sowixapi/adres.php",
                "Aile Bilgisi": "https://api.hexnox.pro/sowixapi/aile.php"
            }
            for api_adi, url in tc_api_list.items():
                sorgu_yap(api_adi, url, {"tc": tc})

        elif secim == "4":
            gsm = Prompt.ask("GSM Numarası")
            sorgu_yap("GSM Sorgu", "https://api.hexnox.pro/sowixapi/gsm.php", {"gsm": gsm})
            sorgu_yap("GSM Detay", "https://api.hexnox.pro/sowixapi/gsmdetay.php", {"gsm": gsm})

        elif secim == "5":
            console.print("\n[bold red]Çıkılıyor...[/bold red]")
            break

if __name__ == "__main__":
    ana_menu()
