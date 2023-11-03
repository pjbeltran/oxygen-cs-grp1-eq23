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

<p align="justify">Pour faire marcher le projet, nous avions premièrement changer les variables du code source. Ces variables étaient `HOST` (le url pour accéder à la simulation), `TOKEN` (le token donné par le chargé de laboratoire pour avoir accès aux données), `T_MAX` (la température maximum, en degré celsius, avant que l'air climatisé (AC) embarque), `T_MIN` (la température minimum, en degré celsius, avant que le chauffage embarque) et `DATABASE` (la base de données utilisée pour stocker les données de la simulation).</p>

```python
if __name__ == "__main__":
    main = Main(
        host="https://hvac-simulator-a23-y2kpq.ondigitalocean.app",
        token="WeVCNw8DOZ",
        tickets=2,
        t_max=30,
        t_min=18,
        database="log680",
    )
    main.start()
```

<p align="justify">Nous avons décidé de choisir `30` comme température maximale et `18` comme température minimale. Ce choix a été fait en prenant compte des températures moyenne du Québec en 2023.</p>

### Ajout de la base de données du code source

Pour faire marcher la base de données, veuillez premièrement installer [psycopg2](https://pypi.org/project/psycopg2/) : 
```
pip install psycopg2-binary
```
<p align="justify">Pour enregistrer les données de la simulation, nous avons choisi de prendre la même base de données pour le premier laboratoire. De plus, nous avons créer 2 tables pour supporter celles-ci, pour accéder et/ou modifier les tables, se référer aux projet https://github.com/pjbeltran/metrics-grp1-eq23-a23/tree/develop/ dans les fichiers pour la bd https://github.com/pjbeltran/metrics-grp1-eq23-a23/blob/develop/oxygen/src/bd/create-tables.ts#L17 </p>

<p align="justify">La décision de séparer les données en 2 tables a été faite afin de facilité l'affichage graphique des données lors des prochains laboratoire avec Grafana. Pour faire rouler l'application, premièrement inscrire cette commande `pipenv install` pour s'assurer d'avoir les dépendances du projet requises et `pipenv run start` pour faire marcher la simulation.</p>

<p align="center">
  <img src="./app_start.png" width="650" height="300">
</p>

<p align="justify">La première table intitulée `sensor_data_event` sert à stocker les données (date et l'événement) lorsque la température est au-dessous de `18` degré celsius ou au-dessus de `30` degrés celsius.</p>

<p align="center">
  <img src="./event.png" width="400" height="600">
</p>

La deuxième table intilutée `sensor_data_temp` sert à stocker **TOUTES** les données (date et température) que la simulation capte.

<p align="center">
  <img src="./temp.png" width="400" height="600">
</p>

<p align="justify">La même démarche que dans le laboratoire 1 pour faire refaire la base de données et les tables sont nécessaire pour faire marcher l'application : https://github.com/pjbeltran/metrics-grp1-eq23-a23/tree/develop#base-de-données </p>

**Prendre note que les captures d'écran pour les tables de la base de données ne correspondent pas à 100% à l'image de l'application qui marche.**

### Tests et modification

<p align="justify">Pour ce qui est des tests, nous avons opter pour https://docs.pytest.org/en/7.4.x/ (pytest) pour effectuer ceux-ci. Les tests consistent de s'assurer que lorsque nous créons le `main`. Nous testons si les variable `HOST`, `TOKEN`, `T_MAX`, `T_MIN` et `DATABASE` sont les bonnes.</p>

```python
def test_host_variable():
    mockMain = main.Main(
        host="test-host",
        token="test-token",
        tickets=2,
        t_max=30,
        t_min=18,
        database="test-database"
    )

    assert "test-host", f"{mockMain.HOST}"
```

<p align="justify">Ensuite, pour rouler les tests, il suffit de faire la commande `pytest test.py`. Le fichier `test.py` est le nom du fichier de tests et il est <b>important de se situer dans le répertoire de test avant de lancer la commande.</b></p>

## Intégration continue

### Création d'image Docker Metrics

### Création d'image Docker HVAC optimisée

### Pipeline repository Metrics

### Pipeline repository HVAC

## Métriques DevOps

### Métriques CI

<p align="justify">Nous avons décidé de choisir une nouvelle option pour recueillir les données du CI. En effet, au lieu d'utilisé `Graphql`, nous avons utilisé l'api de GitHub. L'url pour recevoir ces données est celui-ci : https://api.github.com/repos/pjbeltran/oxygen-cs-grp1-eq23/actions/runs. En effet, ce lien affiche toutes les données nécessaires à la cueillete d'informations. Pour ce qui est des métriques, nous avons opté pour ajouter 7 nouvelles métriques pour suivre l'intégration continu. Les voici :</p>

1. http://localhost:3000/api/getBuildsCI : Cette métrique compte le nombre de "workflows" qui ont été lancés.

```typescript
 await fetch('https://api.github.com/repos/pjbeltran/oxygen-cs-grp1-eq23/actions/runs')
  .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
    data=myJson
    const valueToStore = parseInt(Object.values(data)[0], 10);

    const currentTimestamp = new Date();

    const insertQuery = 'INSERT INTO ci_builds (timestamp, count) VALUES ($1, $2) RETURNING id';
    const values = [ currentTimestamp, valueToStore];

    pool.query(insertQuery, values, (err, result) => {
      if (err) {
        console.error('Error inserting data into the database:', err);
        res.status(500).json({ error: 'Error inserting data into the database' });
      } else {
        const insertedId = result.rows[0].id;
        res.status(200).json(valueToStore);
      }
    });
```

2. http://localhost:3000/api/getBuildsCIAuthor : Cette métrique affiche les noms des développeurs qui ont "trigger" les "workflows" et le nombre de fois.

```typescript
  await fetch('https://api.github.com/repos/pjbeltran/oxygen-cs-grp1-eq23/actions/runs')
  .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
    let a = "";
    var arr = [];
    for (var key in myJson.workflow_runs){
      arr.push(myJson.workflow_runs[key].actor.login);
    }

    const actors = getActorCounts(myJson);
      insertActorData(actors)
        .then(() => {
          res.status(200).json(countOccurrences(arr));
        })
        .catch((error) => {
          console.error('Error inserting data into the database:', error);
          res.status(500).json({ error: 'Error inserting data into the database' });
        });
```

3. http://localhost:3000/api/getBuildsCIAverageTime : Cette métrique calcule la moyenne de temps des "workflows".

```typescript
  fetch('https://api.github.com/repos/pjbeltran/oxygen-cs-grp1-eq23/actions/runs')
  .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
    let a = "";
    var arr = [];
    for (var key in myJson.workflow_runs){
      const date1 = new Date(myJson.workflow_runs[key].updated_at);
      const date2 = new Date(myJson.workflow_runs[key].created_at);

      const difference = date1.getTime() - date2.getTime();

      const hours = Math.floor(difference / 3600000); 
      const minutes = Math.floor((difference % 3600000) / 60000); 
      const seconds = Math.floor((difference % 60000) / 1000); 

      arr.push(`${hours}:${minutes}:${seconds}`);
    }

    insertAverageTime(calculateAverageTime(arr))
        .then(() => {
          return res.status(200).json(calculateAverageTime(arr));
        })
        .catch((error) => {
          console.error('Error inserting data into the database:', error);
          res.status(500).json({ error: 'Error inserting data into the database' });
        });
```

4. http://localhost:3000/api/getBuildsCIConclusion : Cette métrique indique le nombre de "workflows" qui ont passé les tests (success ou failure).

```typescript
await fetch('https://api.github.com/repos/pjbeltran/oxygen-cs-grp1-eq23/actions/runs')
  .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
    let a = "";
    var arr = [];
    for (var key in myJson.workflow_runs){
      arr.push(myJson.workflow_runs[key].conclusion);
    }

    const actors = getActorCounts(myJson);
      insertActorData(actors)
        .then(() => {
          res.status(200).json(countOccurrences(arr));
        })
        .catch((error) => {
          console.error('Error inserting data into the database:', error);
          res.status(500).json({ error: 'Error inserting data into the database' });
        });
```

5. http://localhost:3000/api/getBuildsCIEvent : Cette métrique indique l'action qui a "trigger" le workflow à se lancer (push, pull request, etc..).

```typescript
await fetch('https://api.github.com/repos/pjbeltran/oxygen-cs-grp1-eq23/actions/runs')
  .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
    let a = "";
    var arr = [];
    for (var key in myJson.workflow_runs){
      arr.push(myJson.workflow_runs[key].event);
    }

    const actors = getActorCounts(myJson);
      insertActorData(actors)
        .then(() => {
          res.status(200).json(countOccurrences(arr));
        })
        .catch((error) => {
          console.error('Error inserting data into the database:', error);
          res.status(500).json({ error: 'Error inserting data into the database' });
        });
```

6. http://localhost:3000/api/getBuildsCIName : Cettre métrique indique le nom des "workflows" qui ont éte "trigger" et compte leur occurence.

```typescript
await fetch('https://api.github.com/repos/pjbeltran/oxygen-cs-grp1-eq23/actions/runs')
  .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
    let a = "";
    var arr = [];
    for (var key in myJson.workflow_runs){
      arr.push(myJson.workflow_runs[key].name);
    }

    const actors = getActorCounts(myJson);
      insertActorData(actors)
        .then(() => {
          res.status(200).json(countOccurrences(arr));
        })
        .catch((error) => {
          console.error('Error inserting data into the database:', error);
          res.status(500).json({ error: 'Error inserting data into the database' });
        });
```
7. http://localhost:3000/api/getBuildsCIStatus : Cette métrique indique les status des "workflows" qui ont été lancés (completed, etc..).

```typescript
await fetch('https://api.github.com/repos/pjbeltran/oxygen-cs-grp1-eq23/actions/runs')
  .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
    let a = "";
    var arr = [];
    for (var key in myJson.workflow_runs){
      arr.push(myJson.workflow_runs[key].name);
    }

    const actors = getActorCounts(myJson);
      insertActorData(actors)
        .then(() => {
          res.status(200).json(countOccurrences(arr));
        })
        .catch((error) => {
          console.error('Error inserting data into the database:', error);
          res.status(500).json({ error: 'Error inserting data into the database' });
        });
```

