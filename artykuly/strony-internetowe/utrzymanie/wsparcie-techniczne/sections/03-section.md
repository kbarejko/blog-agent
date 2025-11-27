## Modele współpracy i SLA w wsparciu technicznym

Modele współpracy i SLA w wsparciu technicznym decydują o tym, jak szybko i przewidywalnie reagujesz na awarie — oraz ile za to płacisz. W praktyce najczęściej spotkasz trzy modele rozliczeń: abonament ryczałtowy (miesięczny fee z określonym zakresem i pulą godzin), pakiety godzin (kupujesz bloczki godzin do wykorzystania) i pay‑as‑you‑go (płacisz za faktyczny czas pracy). Abonament daje spokój i priorytet; pakiety są dobre dla firm z umiarkowanym, ale przewidywalnym obciążeniem; pay‑as‑you‑go sprawdza się przy sporadycznych potrzebach.

Decyzja o modelu wiąże się też z wyborem organizacyjnym: outsourcing (zewnętrzny partner), zespół in‑house lub model hybrydowy. Outsourcing obniża koszty stałe i zapewnia dostęp do specjalistów; in‑house daje pełną kontrolę i szybsze iteracje; hybryda łączy zalety obu — np. wewnętrzny product owner i zewnętrzny on‑call. Dla sklepu sezonowego lepszy będzie partner z gwarantowanym SLA; dla rozwijającego się startupu — elastyczny pakiet godzin.

SLA to szczegóły: czas reakcji (acknowledgement) vs. czas przywrócenia (RTO). Typowe wartości: dostępność 99,9% dla krytycznych usług, RTO 2–4 h dla P1, a czas odpowiedzi na P1: 15–60 min. Okna serwisowe (maintenance windows) definiują kiedy można planować deployy bez naruszania SLA.

Priorytety i eskalacje (P1–P4) trzeba zdefiniować w SOW/OLA. Przykład klasyfikacji:
- P1 — awaria produkcyjna blokująca sprzedaż/przychód, natychmiastowa eskalacja on‑call.
- P2 — poważne degradacje (checkout działa, ale z błędami), szybka interwencja w godzinach.
- P3 — drobne błędy funkcjonalne, planowane poprawki.
- P4 — zadania rozwojowe/optimizacje w backlogu.

Zakres odpowiedzialności powinien jasno rozgraniczać linie wsparcia (1/2/3), kto rozwiązuje routing incydentów i kiedy angażować devów. Helpdesk (Jira, Zendesk) plus kanały pilne (telefon on‑call, Slack, SMS) oraz publiczny Status Page upraszczają komunikację.

Raportowanie miesięczne musi zawierać SLA, MTTD/MTTR, backlog i rekomendacje. Transparentność pracy — changelogi, release notes i dzienniki zmian — to obowiązek: ułatwiają audyt i transfer usług. Na końcu umowy warto doprecyzować klauzule wyłączeń, limity godzin, zasadę „fair use” i sposób rozliczenia pracy poza SLA (stawki on‑call, nadgodziny). Bez tych reguł SLA pozostaje tylko deklaracją.