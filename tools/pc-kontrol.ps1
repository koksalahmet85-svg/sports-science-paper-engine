# Genel PC saglik kontrolu (Windows 10/11, PowerShell 5.1+)
# Calistirma (yonetici PowerShell onerilir):
#   powershell -ExecutionPolicy Bypass -File "$HOME\Desktop\pc-kontrol.ps1"
# Rapor Masaustu'ne pc-rapor-<tarih>.txt olarak kaydedilir. Hicbir seyi degistirmez/silmez.

$ErrorActionPreference = 'SilentlyContinue'
$rapor = "$HOME\Desktop\pc-rapor-$(Get-Date -Format 'yyyyMMdd-HHmm').txt"
Start-Transcript -Path $rapor | Out-Null
$uyarilar = New-Object System.Collections.Generic.List[string]
function Baslik($t) { Write-Host "`n=== $t ===" -ForegroundColor Cyan }
function Uyari($t) { $uyarilar.Add($t); Write-Host "  [!] $t" -ForegroundColor Yellow }
function Tamam($t) { Write-Host "  [OK] $t" -ForegroundColor Green }

$admin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $admin) { Write-Host "Not: Yonetici olarak calistirilmadi; disk sagligi gibi bazi kontroller eksik kalabilir." -ForegroundColor Yellow }

# 1. Sistem
Baslik "SISTEM"
$os = Get-CimInstance Win32_OperatingSystem
$cs = Get-CimInstance Win32_ComputerSystem
$bios = Get-CimInstance Win32_BIOS
$uptime = (Get-Date) - $os.LastBootUpTime
"  Model     : $($cs.Manufacturer) $($cs.Model)"
"  Windows   : $($os.Caption) (surum $($os.Version))"
"  BIOS      : $($bios.SMBIOSBIOSVersion) ($($bios.ReleaseDate.ToString('yyyy-MM-dd')))"
"  Acik kalma: $([int]$uptime.TotalDays) gun $($uptime.Hours) saat"
if ($os.Caption -match 'Windows 10') { Uyari "Windows 10 destegi Ekim 2025'te bitti; guvenlik guncellemesi gelmiyor." }
if ($uptime.TotalDays -gt 7) { Uyari "Bilgisayar $([int]$uptime.TotalDays) gundur yeniden baslatilmamis." }

# 2. Islemci ve bellek
Baslik "ISLEMCI VE BELLEK"
$cpu = Get-CimInstance Win32_Processor
$ramTop = [math]::Round($os.TotalVisibleMemorySize / 1MB, 1)
$ramBos = [math]::Round($os.FreePhysicalMemory / 1MB, 1)
$ramYuzde = [math]::Round((1 - $os.FreePhysicalMemory / $os.TotalVisibleMemorySize) * 100)
"  CPU       : $($cpu.Name) | yuk: %$($cpu.LoadPercentage)"
"  RAM       : $ramTop GB toplam, $ramBos GB bos (%$ramYuzde dolu)"
Get-CimInstance Win32_PhysicalMemory | ForEach-Object { "  RAM yuvasi: $($_.BankLabel) $([math]::Round($_.Capacity/1GB)) GB $($_.Speed) MHz" }
if ($ramYuzde -gt 85) { Uyari "RAM %$ramYuzde dolu; acik programlari azaltin veya RAM ekleyin." }
"  En cok RAM kullanan 5 islem:"
Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 5 | ForEach-Object { "    {0,-28} {1,6} MB" -f $_.ProcessName, [math]::Round($_.WorkingSet64 / 1MB) }

# 3. Disk
Baslik "DISK"
Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Used -gt 0 } | ForEach-Object {
    $top = ($_.Used + $_.Free) / 1GB
    $bos = $_.Free / 1GB
    "  {0}: {1:N0} GB / {2:N0} GB bos (%{3:N0})" -f $_.Name, $bos, $top, ($bos / $top * 100)
    if ($bos -lt 20) { Uyari "$($_.Name): surucusunde yalnizca $([math]::Round($bos)) GB bos (hedef >= 20 GB)." }
}
Get-PhysicalDisk | ForEach-Object {
    $r = $_ | Get-StorageReliabilityCounter
    $ek = ""
    if ($r.Wear -ne $null) { $ek += " | asinma: %$($r.Wear)" }
    if ($r.Temperature) { $ek += " | sicaklik: $($r.Temperature) C" }
    "  $($_.FriendlyName) ($($_.MediaType), $([math]::Round($_.Size/1GB)) GB) saglik: $($_.HealthStatus)$ek"
    if ($_.HealthStatus -ne 'Healthy') { Uyari "Disk sagligi: $($_.HealthStatus). Verileri hemen yedekleyin." }
    if ($r.Wear -gt 80) { Uyari "SSD asinmasi %$($r.Wear); degisim planlayin." }
}
$temp = (Get-ChildItem $env:TEMP -Recurse -File -Force | Measure-Object Length -Sum).Sum / 1GB
"  Gecici dosyalar: $([math]::Round($temp, 2)) GB"
if ($temp -gt 1) { Uyari "Gecici dosyalar $([math]::Round($temp,1)) GB; temizlenebilir." }
$hiber = Test-Path C:\hiberfil.sys
"  Hazirda bekletme dosyasi: $(if ($hiber) {'var'} else {'kapali'})"

# 4. Pil
Baslik "PIL"
$tasarim = (Get-CimInstance -Namespace root\wmi -ClassName BatteryStaticData).DesignedCapacity
$tam = (Get-CimInstance -Namespace root\wmi -ClassName BatteryFullChargedCapacity).FullChargedCapacity
if ($tasarim -and $tam) {
    $saglik = [math]::Round($tam / $tasarim * 100)
    "  Pil sagligi: %$saglik (tasarim $tasarim mWh, simdi $tam mWh)"
    if ($saglik -lt 60) { Uyari "Pil kapasitesi %$saglik'e dusmus; pil degisimi dusunulebilir." }
} else { "  Pil bilgisi okunamadi (yonetici gerekebilir)." }

# 5. Guvenlik
Baslik "GUVENLIK"
$mp = Get-MpComputerStatus
if ($mp) {
    "  Antivirus: $(if ($mp.AntivirusEnabled) {'acik'} else {'KAPALI'}) | gercek zamanli koruma: $(if ($mp.RealTimeProtectionEnabled) {'acik'} else {'KAPALI'})"
    "  Tanim guncellemesi: $($mp.AntivirusSignatureLastUpdated) | son tam tarama: $(if ($mp.FullScanEndTime) {$mp.FullScanEndTime} else {'yok'})"
    if (-not $mp.RealTimeProtectionEnabled) { Uyari "Gercek zamanli koruma kapali." }
    if ($mp.AntivirusSignatureAge -gt 7) { Uyari "Virus tanimlari $($mp.AntivirusSignatureAge) gunluk." }
}
$tehdit = Get-MpThreatDetection
if ($tehdit) {
    Uyari "$(@($tehdit).Count) tehdit kaydi bulundu:"
    $tehdit | ForEach-Object { "    $($_.InitialDetectionTime) | basarili temizlik: $($_.ActionSuccess) | $($_.Resources -join ', ')" }
} else { Tamam "Tehdit kaydi yok." }
Get-NetFirewallProfile | ForEach-Object {
    "  Guvenlik duvari ($($_.Name)): $(if ($_.Enabled) {'acik'} else {'KAPALI'})"
    if (-not $_.Enabled) { Uyari "Guvenlik duvari $($_.Name) profili kapali." }
}
$sonGuncelleme = Get-HotFix | Where-Object InstalledOn | Sort-Object InstalledOn -Descending | Select-Object -First 1
if ($sonGuncelleme) {
    $gun = [int]((Get-Date) - $sonGuncelleme.InstalledOn).TotalDays
    "  Son Windows guncellemesi: $($sonGuncelleme.HotFixID) ($gun gun once)"
    if ($gun -gt 45) { Uyari "Son guncelleme $gun gun once yuklenmis." }
}
$bekleyen = (Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired') -or
            (Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending')
if ($bekleyen) { Uyari "Guncelleme icin yeniden baslatma bekleniyor." }

# 6. Baslangic programlari ve sistem hatalari
Baslik "BASLANGIC VE HATALAR"
$bas = Get-CimInstance Win32_StartupCommand
"  Baslangicta acilan program sayisi: $(@($bas).Count)"
$bas | ForEach-Object { "    - $($_.Name)" }
if (@($bas).Count -gt 8) { Uyari "Baslangicta $(@($bas).Count) program aciliyor; acilis yavaslar (Gorev Yoneticisi > Baslangic)." }
$hatalar = Get-WinEvent -FilterHashtable @{ LogName = 'System'; Level = 1, 2; StartTime = (Get-Date).AddDays(-7) }
"  Son 7 gunde kritik/hata olay sayisi: $(@($hatalar).Count)"
$hatalar | Group-Object ProviderName | Sort-Object Count -Descending | Select-Object -First 5 | ForEach-Object { "    {0,4} x {1}" -f $_.Count, $_.Name }

# 7. Makale sistemi icin araclar
Baslik "ARASTIRMA ARACLARI"
foreach ($arac in 'git', 'python', 'quarto', 'code', 'claude', 'R') {
    $c = Get-Command $arac
    if ($c) { Tamam "$arac kurulu ($($c.Source))" } else { "  [ ] $arac kurulu degil" }
}

# Ozet
Baslik "OZET"
if ($uyarilar.Count -eq 0) { Tamam "Kritik sorun bulunmadi." }
else { "  $($uyarilar.Count) uyari:"; $uyarilar | ForEach-Object { "   - $_" } }
Stop-Transcript | Out-Null
Write-Host "`nRapor kaydedildi: $rapor" -ForegroundColor Cyan
