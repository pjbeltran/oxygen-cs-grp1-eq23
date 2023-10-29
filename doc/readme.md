# oxygen-cs-grp1-eq23

# Table des matières 

- [Oxygen-CS](#oxygen-cs)
  - [Modification des variables du code source](#modification-des-variables-du-code-source)
  - [Ajout de la base de données du code source](#ajout-de-la-base-de-données-du-code-source)
  - [Tests et modification](#tests-et-modification)
- [Intégration continue](#intégration-continue)
  - [Création d'image Docker Metrics](#création-dimage-docker-metrics)
  - [Création d'image Docker HVAC optimisée](#création-dimage-docker-hvac-optimisée)
  - [Pipeline repository Metrics](#pipeline-repository-metrics)
  - [Pipeline repository HVAC](#pipeline-repository-hvac)
- [Métriques DevOps](#métriques-devops)
  - [Métriques CI](#métriques-ci)
 
## Oxygen-CS

### Modification des variables du code source

Pour faire marcher le projet, nous avions premièrement changer les variables du code source. Ces variables étaient `"HOST"` (le url pour accéder à la simulation),
`"TOKEN"` (le token donné par le chargé de laboratoire pour avoir accès aux données), `"T_MAX"` (la température maximum, en degré celsius, avant que l'air climatisé (AC) embarque), `"T_MIN"` (la température minimum, en degré celsius, avant que le chauffage embarque) et `"DATABASE"` (la base de données utilisée pour stocker les données de la simulation).



### Ajout de la base de données du code source

Pour faire marcher la base de données, veuillez premièrement installer psycopg2 : 
```
pip install psycopg2-binary
```

## Intégration continue

### Création d'image Docker Metrics

### Création d'image Docker HVAC optimisée

### Pipeline repository Metrics

### Pipeline repository HVAC

## Métriques DevOps

### Métriques CI
