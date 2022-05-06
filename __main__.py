"""
Bei der Erzeugung einer Timetable Klasse kann auch der Name eines schon erstellten Stundenplans (ohne prof_raw
etc.) eingegeben werden. Dann wird dieser geladen und die Fächer geprinted.
Bei der Eingabe einer neuen Stunde werden bereits erstellte angezeigt. Zum Löschen dann einfach den Text in den
Textfeldern löschen (und "OK" drücken). Stundenpläne werden in /Documents/SavedTimetables/{titel} gespeichert,
wobei titel der Name ist, der dem Stundenplan gegeben wird.
"""
import Stundenplan

print(__doc__)
titel = "Name"  # Name des zu erstellenden Stundenplans
# hier kann auch der Name eines schon erstellten Stundenplans (ohne prof_raw etc.) eingegeben werden. Dann wird dieser
# geladen. Bei der Eingabe
stundenplan = Stundenplan.Timetable(titel)
stundenplan.draw_timetable(titel)
