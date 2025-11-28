## Operacje i skalowanie: workflow, design system, governance, migracje

Przechodzimy od decyzji technologicznej do codziennej pracy zespołu. Tu rozstrzyga się, czy builder naprawdę przyspieszy wydania, czy stanie się źródłem bałaganu. Klucz to proste, powtarzalne procesy.

#### Workflow: staging → review → production, role i uprawnienia
Każda zmiana musi przechodzić przez staging. Tam robi się QA, SEO i testy a11y. Role: content editor (tworzy treści), designer (szablony), developer (blok‑y i integracje), release manager (akceptuje). Ogranicz uprawnienia edytorów — pozwól na edycję treści, nie na zmiany komponentów.

#### Szablony stron i “guardrails” dla spójności brandu
Zdefiniuj szablony: home, landing, produkt, blog. Wprowadź guardrails — ograniczenia dostępnych widgetów, maksymalna liczba kolumn, zasady typografii. To zapobiega „kreatywnemu chaosowi” i zmniejsza regresje wizualne.

#### Biblioteka sekcji: hero, CTA, formularze, FAQ, case studies
Zbuduj bibliotekę gotowych sekcji. Każda sekcja ma wersje i opis użycia. Marketing wybiera gotowe bloki zamiast kopiować layouty. To przyspiesza pracę i upraszcza refaktory.

#### Style globalne, tokens (kolory, typografia, spacing)
Wprowadź tokens: kolory, skale typograficzne, spacing. Trzymaj je w jednym miejscu. Aktualizacja tokena powinna propagować się automatycznie. To największa korzyść przy rebrandingu.

#### Reużywalne komponenty vs. “kopiuj‑wklej”
Wymuszaj użycie komponentów. Kopiuj‑wklej generuje drift stylów i zwiększa czas utrzymania. Każdy komponent ma wersję i changelog.

#### Dokumentacja i zasady naming convention
Dokumentuj komponenty, ich warianty i przypadki użycia. Naming: [component]__[variant]--v1. To pomaga w debugowaniu i migracji.

#### Checkpointy SEO/a11y/CWV przed publikacją
Przed publikacją: meta/OG, struktura nagłówków, alt‑text, aria, Lighthouse threshold (np. performance ≥ 80). Automatyczne skany plus manualne sprawdzenie klawiaturą.

#### Testy regresji wizualnej i monitorowanie wydajności
Wprowadź visual regression (np. Percy). Dodaj RUM i syntetyczne testy CWV. Alerty przy spadku wskaźników.

#### Polityka aktualizacji i roll‑back
Aktualizacje co ustalony cykl. Najpierw canary na stagingu, potem production. Miej rollback plan — snapshot/staging i 301 maps gotowe na wypadek awarii.

#### Plan migracji bez utraty SEO
Mapuj URL, przygotuj 301, zaktualizuj sitemapę i przetestuj indeksację (Fetch as Google). Migrację wykonuj etapami, monitorując ruch i pozycje.

#### Ekstrakcja do customu i architektura headless
Kiedy wypakować komponent do kodu? Gdy komponent obniża CWV, wymaga niestandardowej logiki albo skaluje się poza możliwości buildera. Headless to kolejny etap: separacja treści i frontu ułatwia wielokanałowość.

#### Własność i metryki
Właścicielem biblioteki powinna być rola DesignOps lub Frontend Lead. Mierzymy jakość: % przejść QA, liczba regresji wizualnych, średni czas cyklu (idea → live). Gdy aktualizacja psuje layout — szybki rollback, hotfix, analiza przyczyn i aktualizacja testów oraz dokumentacji.