## Podstawowe warstwy ochrony sklepu online

### Zabezpieczenie infrastruktury technicznej

Fundamenty bezpieczeństwa buduje się od podstaw. To znaczy od serwera, na którym stoi twój sklep.

#### Certyfikat SSL/TLS - fundament bezpieczeństwa

SSL to absolutne minimum. Bez niego Google oznacza twoją stronę jako niebezpieczną, a klienci uciekają przed dokończeniem zakupu.

Ale nie każdy SSL jest równy. Certyfikaty domenowe (DV) zapewniają podstawowe szyfrowanie. Kosztują grosze i są gotowe w kilka minut. To wystarczy dla małego sklepu.

Certyfikaty organizacyjne (OV) wymagają weryfikacji firmy. Dają więcej wiarygodności, ale procedura trwa dni. Extended Validation (EV) to najwyższy poziom - pokazuje nazwę firmy w pasku adresu. Banki i wielkie sklepy często go wybierają.

Sprawdź swój certyfikat już dziś. W przeglądarce kliknij kłódkę przy adresie. Data ważności, algorytm szyfrowania, wystawca - wszystko powinno być aktualne.

Automatyczne odnawianie to must-have. Wygasły certyfikat blokuje dostęp do sklepu natychmiast. Let's Encrypt oferuje darmowe certyfikaty z auto-renewal. Większość hostingów ma to już wbudowane.

#### Hosting i serwer - wybór ma znaczenie

Tani hosting to fałszywa ekonomia. Serwery współdzielone oznaczają, że los twojego sklepu zależy od sąsiadów. Jeden zhakowany sklep może zagrozić całemu serwerowi.

VPS lub serwer dedykowany daje kontrolę. Możesz skonfigurować firewall dokładnie pod swoje potrzeby. Zablokować niepotrzebne porty. Ograniczyć dostęp do panelu administracyjnego tylko dla swojego IP.

Firewall to pierwszy strażnik. Podstawowe reguły: zablokuj wszystko, otwórz tylko to, co niezbędne. Port 80 i 443 dla ruchu WWW. Port 22 dla SSH, ale tylko z określonych adresów IP. Port 25 dla emaili - często niepotrzebny.

Aktualizacje systemu operacyjnego to rutyna, którą musisz wdrożyć. Ubuntu, CentOS czy Debian wypuszczają łatki bezpieczeństwa regularnie. Automatyczne aktualizacje bezpieczeństwa to rozsądny kompromis między stabilnością a ochroną.

Nie wszystkie aktualizacje można automatyzować. Duże zmiany wersji kernela czy Apache wymagają testowania. Ale łatki bezpieczeństwa? Te instaluj od razu.