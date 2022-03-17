# Ready Aim Fire Tournament (Pour ALGO)

[Inspiration par ici](https://github.com/carykh/PrisonersDilemmaTournament).

## Règles pour "R.A.F."

Le jeu est assez simple puisque pour un tour vous ne pouvez faire qu'une seule chose : tirer !
Sois tu tires sur quelqu'un puis il meurt.
Sois tu te tires dessus et donc tu meurt SAUF si on te tire dessus (auquel cas tout tes attaquants meurent).
Ou tu tires en l'air

## Comment que ça marche ?

Quand tu exécutes le fichier `readyAimFire.py`, il va regarder tout les fichiers qui se situent dans le dossier `strats`. Ensuite le jeu fera se combattre aléatoirement toutes les stratégies sur beaucoup de parties (pour moyenner). Une fois que c'est finis, les résultats seront dans le fichier `results.txt`.

## Comment que on ajoute une stratégie ?

Il suffit de rajouter ton fichier `.py` dans le sous-dossier `strats` bien sûr ! Regarde les exemples fournis car tu devras suivre la même structure.

## Comment que les points fonctionnent ?

C'est assez simple : 
- 2 points par tours survécus.
- 4 points par victoire.
- 1 point par victimes.

## Comment qu'on participe ?

Et bien c'est [ici](https://forms.gle/2iufXNGSCMzxV6Cm6).

## Règles

- Les imports doivent être sur ma machine, donc restez soft et pas de tensorflow par exemple.
- Un programme visant à ralentir le tournois (en exécution notemment)
- Vous pouvez envoyer plusieurs codes (et modifier vos réponse si je me trompe pas)