# Wo sind die Parteien der Hochschulwahlen 2023 in Göttingen im Vergleich zu Bundestagsparteien auf einer Links-Rechts Skala einzuordnen?
## Hausarbeit im Seminar Textanalyse WiSe 22/23
Die komplette Hausarbeit ist als [Bonnin_Textanalyse_Hausarbeit.pdf](https://github.com/MaximeBonnin/hausarbeit/blob/master/Bonnin_Textanalyse_Hausarbeit.pdf) ebenfalls in diesem Repository zu finden. 
### Methoden
Für die Analyse wird die „Wordscores“ Methode ([Laver et al. 2003](https://www.cambridge.org/core/journals/american-political-science-review/article/extracting-policy-positions-from-political-texts-using-words-as-data/4F4676E80A79E01EAAB88EF3F2D1B733)) verwendet. Dabei handelt es sich um einen Algorithmus, welcher die Häufigkeit, mit welcher die gleichen Worte in verschiedenen Texten vorkommen zählt. Anschließend wird anhand von Referenztexten und -werten – in diesem Fall den Wahlprogrammen der Bundestagsparteien und deren MARPOR Werten – eine Skalierung vorgenommen um die Texte basierend auf ihrer Ähnlichkeit auf einer Ache zu platzieren.

Die technische Umsetzung findet in der Programmiersprache Python statt und basiert stark auf der [Arbeit von Marzagao (2014)](https://thiagomarzagao.com/2013/06/10/wordscores-in-python/). Allerdings wurden einige Anpassungen vorgenommen, um die Funktionalität mit neueren Versionen der Programmiersprache zu ermöglichen. 

Um eine sinnvolle Skalierung vorzunehmen ist die Auswahl der Referenztexte essenziell. Diese müssen möglichst alle relevanten Worte in einem möglichst ähnlichen Kontext wie die zu analysierenden Texte enthalten. Um dies gewähr leisten zu können wurden Wahlprogramme der Parteien der letzten Bundestagswahl als Referenz gewählt. 

Die politische Verortung der Parteien basiert zunächst auf dem Manifesto Research on Political Representation (MARPOR). Dabei werden Wahlprogramme manuell in Teilsätze unterteilt und diese dann bestimmten Themen zugewiesen. Basierend auf den Anteilen der Themen können die Wahlprogramme dann auf einer Achse verortet und in Relation gesetzt werden. Der Datensatz für diese handkodierten Wahlprogramme beinhaltet somit Werte für jede Bundestagspartei.

### Analyse

![Heatmap](https://github.com/MaximeBonnin/hausarbeit/blob/master/graph1_normalisierte_wordscores_werte_komplett_heatmap.png)

![RILE Axis](https://github.com/MaximeBonnin/hausarbeit/blob/master/Vergleich_RILE_MARPOR_vs_FnK.png)

### Ergebnisse

Abschließend ist zu sagen, dass Hochschulgruppen zwar mehr als nur linke Positionen abbilden, Studierende mit ihrem Wahlverhalten aber im Mittel linke Positionen ausdrücken. Die Frage nach ideologischen Problemen an Hochschulen, welche in den Medien aufgeworfen werden, sollten somit nicht ignoriert werden, sind aber in ihrem Ausmaß geringer als oft dargestellt.

Weiterführend wäre eine Analyse von mehr Hochschulgruppen an anderen Universitäten nötig, um die Ergebnisse allgemein zu bestätigen und Aussagen über systemische Probleme zu machen. Zudem ist der kausale Zusammenhang nicht eindeutig: werden Studierende politisch linker oder ziehen sie bereits linke Personen eher an?

