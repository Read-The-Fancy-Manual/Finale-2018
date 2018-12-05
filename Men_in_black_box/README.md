# Boolean-based Blind SQLi with WAF

## Information

Information displayed for CTF players:

+ **Name of the challenge** / **Nom du challenge**: `Men in black box`
+ **Category** / **Catégorie**: `Web` / `Web`
+ **Internet**: not needed
+ **Difficulty** / **Difficulté**: hard / difficile
+ **Author**: noraj

### Description

English:

```
Automated tools don't prevent manual testing.
<URL_of_the_server_here>
```

French:

```
Les outils automatiques n'empêche pas de faire des tests manuels.
<URL_du_server_ici>
```

### Hints

- Hint1: sqli
- Hint2: blacklist = ['ABORT','ACTION','ADD','AFTER','ALL','ALTER','ANALYZE','AND','AS','ASC','ATTACH','AUTOINCREMENT','BEFORE','BEGIN','BETWEEN','BY','CASCADE','CASE','CAST','CHECK','COLLATE','COLUMN','COMMIT','CONFLICT','CONSTRAINT','CREATE','CROSS','CURRENT','CURRENT_DATE','CURRENT_TIME','CURRENT_TIMESTAMP','DATABASE','DEFAULT','DEFERRABLE','DEFERRED','DELETE','DESC','DETACH','DISTINCT','DO','DROP','EACH','ELSE','END','ESCAPE','EXCEPT','EXCLUSIVE','EXISTS','EXPLAIN','FAIL','FILTER','FOLLOWING','FOR','FOREIGN','FROM','FULL','GLOB','GROUP','HAVING','IF','IGNORE','IMMEDIATE','IN','INDEX','INDEXED','INITIALLY','INNER','INSERT','INSTEAD','INTERSECT','INTO','IS','ISNULL','JOIN','KEY','LEFT','LIKE','LIMIT','MATCH','NATURAL','NO','NOT','NOTHING','NOTNULL','NULL','OF','OFFSET','ON','OR','ORDER','OUTER','OVER','PARTITION','PLAN','PRAGMA','PRECEDING','PRIMARY','QUERY','RAISE','RANGE','RECURSIVE','REFERENCES','REGEXP','REINDEX','RELEASE','RENAME','REPLACE','RESTRICT','RIGHT','ROLLBACK','ROW','ROWS','SAVEPOINT','SELECT','SET','TABLE','TEMP','TEMPORARY','THEN','TO','TRANSACTION','TRIGGER','UNBOUNDED','UNION','UNIQUE','UPDATE','USING','VACUUM','VALUES','VIEW','VIRTUAL','WHEN','WHERE','WINDOW','WITH','WITHOUT','abort','action','add','after','all','alter','analyze','and','as','asc','attach','autoincrement','before','begin','between','by','cascade','case','cast','check','collate','column','commit','conflict','constraint','create','cross','current','current_date','current_time','current_timestamp','database','default','deferrable','deferred','delete','desc','detach','distinct','do','drop','each','else','end','escape','except','exclusive','exists','explain','fail','filter','following','for','foreign','from','full','glob','group','having','if','ignore','immediate','in','index','indexed','initially','inner','insert','instead','intersect','into','is','isnull','join','key','left','like','limit','match','natural','no','not','nothing','notnull','null','of','offset','on','or','order','outer','over','partition','plan','pragma','preceding','primary','query','raise','range','recursive','references','regexp','reindex','release','rename','replace','restrict','right','rollback','row','rows','savepoint','select','set','table','temp','temporary','then','to','transaction','trigger','unbounded','union','unique','update','using','vacuum','values','view','virtual','when','where','window','with','without']

## Integration

This challenge require a Docker Engine and Docker Compose. (Contact author if you plan to use it in another way).

Builds, (re)creates, starts, and attaches to containers for a service:

```
$ docker-compose up --build webserver_7
```

Add `-d` if you want to detach the container.

The challenge is using the following images:

- debian:stretch-20180831

## Solving

1. Try some random credentials => `Wrong credentials!`
2. `' OR 1=1-- -` => `Naughty hacker` => There must be a WAF
3. `' oR 1=1-- -` => `Wrong credentials!` => WAF bypassed but SQLi not triggered
4. `" oR 1=1-- -` => Logged in!
5. More tests => blind SQLi
6. Boolean-based blind SQLi
7. recon => get table schema
8. dump only the right table and column to speed up the process
9. flag

### Author solution

See `solve.sh`.

## Flag

Flag: `sigsegv{N0rAj_d3_MA_SqL1_d3S_Fam1lL3S}`

```
$ printf %s 'sigsegv{N0rAj_d3_MA_SqL1_d3S_Fam1lL3S}' | md5sum
73a604a180220562deeca0322bc7c34d  -

$ printf %s 'sigsegv{N0rAj_d3_MA_SqL1_d3S_Fam1lL3S}' | sha1sum
0f09773cbcd9c199608a14e376d81a225d0149af  -

$ printf %s 'sigsegv{N0rAj_d3_MA_SqL1_d3S_Fam1lL3S}' | sha256sum
510a2b5ca6147bcb69f0ffa1d0b404e3fa392ac319c24e758f27bad7076a52ac  -

$ printf %s 'sigsegv{N0rAj_d3_MA_SqL1_d3S_Fam1lL3S}' | b2sum
39372a3ee2efe85fb0507b96f6e33fa4bb80a4920b14a9c4f100ad65640cc09eade8995641d3d30f652a45d3836c861eeb320721fb9a81de403f1c44f2b9a724  -

$ printf %s 'sigsegv{N0rAj_d3_MA_SqL1_d3S_Fam1lL3S}' | keccaksum -l
a34a206a5995b2a523a375b5e90be2ed27706a32108cfb98c3827c249e803c648d8ada8135f9e022ca6f19eed3062a1ba603e718e75e28b3b4505852893b2600  -
```
