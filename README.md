# YOUTUBE SINGLE CHANNEL UPLOADER
### Aplikacija, ki omogoča nalaganja urejenih kompilacij skladb na portal Youtube. Samodejno pridobivanje povezav za prenos posameznih skladb in generiranje Youtube poglavij.

Iz poljubno določenega direktorija se dinamično preberejo datoteka, na podlagi katerih se tvori imenik. S knjižnico Selenium se nato pridobijo povezave do posameznih skladb ter skrajšajo s pomočjo klica oddaljene funkcije URL Shortener-ja. Sledi branje dolžine MP3 datotek iz direktorija, na podlagi katerih se naredijo Youtube poglavja, zraven njih pa se doda še pripadajoča skrajšana povezava do skladbe. Iz vseh prej omenjenih komponent se zgradi Youtube opis, prav tako pa se preveri, v kateri žaner spada kompilacija na podlagi imena datoteke videa v direktoriju. Tako se lahko začne samo nalaganje na Youtube z pomočjo Youtube API-ja.

### Tehnološki sklad

* Python
* Youtube API 
* URL Shortener 
* Selenium

### Vpostavitev aplikacije:

* Prenos paketa.
* Prenos selenium knjižnice ter youtube API knjižnice.
* Pridobitev potrebnih youtube akreditacij
* Zagon
