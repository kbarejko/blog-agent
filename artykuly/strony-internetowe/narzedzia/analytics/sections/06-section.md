## Jakość danych, atrybucja i integracje z reklamą oraz CRM

Skoro masz zgodę i uporządkowany stack, czas zadbać o „paliwo” dla decyzji. Najpierw higiena ruchu: odfiltruj wejścia pracowników (lista IP to za mało przy pracy hybrydowej – ustaw cookie/tryb „employee=true” i filtruj po parametrze) oraz boty (filtry GA4 + reguły w WAF/CDN). Jeśli użytkownik przechodzi między subdomenami lub domenami (np. sklep → płatności), włącz cross-domain measurement i wyklucz własne domeny z refererów, by nie pompować „direct”.

Debugowanie to codzienność. Podgląd GTM + DebugView GA4 powinny być pierwszym krokiem przy każdym deployu. Sprawdzaj, czy event ma komplet parametrów (value, currency, item_id, coupon, event_id/transaction_id), czy waluty są zgodne z kontem Ads, oraz czy purchase odpala się raz – po status=paid z backendu.

Duplikacje zjadają zaufanie. Stabilny identyfikator zamówienia/leadów (transaction_id, lead_id) musi pochodzić z backendu i być wspólny dla GA4, Ads i Meta. Wysyłaj eventy server-side z event_id i włącz deduplikację po parze event_name+event_id. Formularze? Form_submit tylko po 200 OK; odświeżenie strony nie może wywołać drugiej konwersji.

Leady żyją w CRM, więc importuj konwersje z Salesforce/HubSpot (Offline Conversions do Google Ads; CAPI do Meta) po zmapowaniu external_id (hash e‑mail/telefon za zgodą) i timestampu. Ustal jeden etap do optymalizacji (np. SQL lub Won) i deduplikuj go względem ga4_generate_lead, żeby nie liczyć „dwóch zwycięstw”.

Poprawa dopasowań to szybki zysk. Enhanced Conversions w Google Ads i Conversions API w Meta zwykle podnoszą match rate o 5–20%, co stabilizuje bidding. Warunek: zgoda, poprawne haszowanie i zgodność event_id między przeglądarką a serwerem.

Automatyzacja stawek potrzebuje jakościowych sygnałów. Przekazuj wartości konwersji zbliżone do marży (value adjusted: brutto – rabaty – średnie zwroty – koszty logistyczne) albo wartość predykcyjną (score→value). Unikaj „pustych” konwersji bez value.

Atrybucja w GA4: data‑driven do alokacji budżetu i oceny wsparcia górnego lejka; last click do sanity checków, SEO brand i rozliczeń taktycznych. Gdy rosną wydatki „brand”, sięgnij po MMM – nawet lekkie, oparte o tygodniowe dane i koszt mediów – by oszacować wpływ offline i kanałów bez klików.

Inkrementalność potwierdzisz testami geograficznymi/lift studies: regiony test vs kontrola, jasno zdefiniowane KPI i minimalny efekt istotny. Równolegle łącz BigQuery z ERP/księgowością: marże, zwroty, koszty wysyłek. To baza do LTV i LTV:CAC per segment/produkt i oceny paybacku.

Ustal widełki zgodności: ruch i sesje ±5–10%, przychód/zakupy vs ERP ±5–15% (Consent Mode zwiększa różnice), leady kwalifikowane vs CRM ±0–5%. Jeśli odchylenia rosną – szukaj duplikacji lub braków w imporcie. A które kanały naprawdę dowożą? Wyłącz na tydzień kampanię w kilku miastach i zobacz, czy sprzedaż spada poza szum. To prosty, ale uczciwy test inkrementalności.