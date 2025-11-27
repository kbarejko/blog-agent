## Od celu do implementacji: plan pomiaru, KPI i taksonomia danych

Przekładamy pytania na plan pomiaru. Zacznij od OKR-ów i ułóż piramidę KPI: na szczycie North Star (np. „przychód na aktywnego użytkownika” lub „LTV na klienta”), niżej sub‑KPI wspierające cel (CAC per kanał, retencja 30‑dniowa, ROAS, czas do pierwszej wartości), na dole wskaźniki taktyczne (CVR formularza, share of returning, scroll >75%, CTR kreacji). Do każdego wskaźnika dopisz definicję (dokładna formuła), próg/target i częstotliwość monitoringu: guardraile dziennie, KPI tygodniowo, deep‑dive miesięcznie. Właściciel KPI to konkretna osoba.

Taksonomia zdarzeń to klej. Przyjmij prosty standard: eventy i parametry w języku angielskim, snake_case, czasownik + rzeczownik (view_item, add_to_cart, begin_checkout, generate_lead). Parametry: value, currency, item_id, item_name, price, quantity, coupon, form_id, form_step, lead_score. Jeden słownik dla całej firmy i partnerów. Zakazane są synonimy (purchase vs order_complete – wybierz jedno). Zadbaj o changelog i wersjonowanie.

Plan data layer opisuje, co strona „wypluwa” do warstwy danych w kluczowych momentach. Przykłady:
- Logowanie: event login z parametrami user_id (jeśli użytkownik się zgodził), auth_method.
- Koszyk/checkout: add_to_cart/begin_checkout/purchase z ecommerce.items (item_id, item_name, price, quantity) oraz value i currency.
- Lead form: form_start, form_submit, generate_lead oraz pola pomocnicze: form_id, form_step, error_count.

Kryteria akceptacji to „kiedy zaliczamy event”. Np. purchase tylko po status=paid i unikalnym transaction_id; generate_lead po odpowiedzi 200 z backendu i (opcjonalnie) double opt‑in; add_to_cart tylko raz na klik, bez duplikacji przy odświeżeniu. Zapisz te reguły w QA checklist.

UTM-y trzymaj w ryzach. Controlled list dla medium (cpc, email, social, affiliate, referral). Source małe litery (meta, linkedin, newsletter_aug). Kampanie w schemacie rok‑miesiąc_cel_segment (2025‑03_brand_pl, 2025‑Q2_retention_vip). content/term dla kreacji i słów kluczowych. Google Ads: auto‑tagowanie (gclid), inne platformy – makra dynamiczne i walidacja linków.

Wybór sygnałów: „twarde” (purchase, qualified_lead, subscription_started) uczą algorytmy najlepiej; „miękkie” (scroll, video_play, add_to_wishlist) pomagają diagnozować, ale nie powinny być primary conversions. W Google Ads ustaw Primary: purchase/qualified_lead z wartością; Secondary: add_to_cart, form_submit do obserwacji. W Meta ustaw zdarzenia o najwyższej jakości (np. qualified_lead nad lead) i włącz CAPI/Enhanced Conversions.

Na koniec dwa pytania kontrolne:
- Czy nasze KPI są policzalne w obecnym stosie (GA4/CRM/BI)? Jeśli nie, czego brakuje: parametru, integracji, modelu danych?
- Czy nazewnictwo jest spójne i zrozumiałe dla zespołów? Jeśli ktoś nowy potrafi zdefiniować purchase i CAC bez dopytywania – wygrałeś taksonomię.