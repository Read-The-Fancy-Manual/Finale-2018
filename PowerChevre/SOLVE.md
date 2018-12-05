Après avoir téléchargé l'archive du challenge et après l'avoir décompressé,  on obtient 8 executables.

On va commencer par faire un file sur le premier fichier:

```
file ast.exe
ast.exe: PE32 executable (console) Intel 80386 Mono/.Net assembly, for MS Windows
```

Comme il s'agit d'un fichier en .Net assembly, on va pouvoir l'ouvrir avec DotPeek pour voir le fichier plus clairement:

![ast.exe](https://wiki.rtfm.re/sigsegv.ctf/ctf.reverse_6/raw/master/solve/ast_first.png)

On voit là qu'il s'agit d'un script PowerShell transformé en executable avec PS2EXE.
Maintenant on va pouvoir extraire simplement les scripts PowerShell de cette manière:

```
./ast.exe -Extract:ps1/ast.ps1
./lst.exe -Extract:ps1/lst.ps1
./mnt.exe -Extract:ps1/mnt.ps1
./mst.exe -Extract:ps1/mst.ps1
./til.exe -Extract:ps1/til.ps1
./ut.exe -Extract:ps1/ut.ps1
./wst.exe -Extract:ps1/wst.ps1
./xpo.exe -Extract:ps1/xpo.ps1
```

Bingo on a nos scripts dans le dossier ps1.

ast.ps1
```
Function idot()
{
    write-host "https://www.youtube.com/watch?v=3rfuffQUhfQ"
}
```

lst.ps1
```
Function ipot()
{
    write-host "https://www.youtube.com/watch?v=R2ZW_94DyYM"
}
```

mnt.ps1
```
add-type -assemblyName "Microsoft.VisualBasic"
$ErrorActionPreference= 'silentlycontinue'
. $PSScriptRoot"/til.ps1"
. $PSScriptRoot"/xpo.ps1"
. $PSScriptRoot"/ut.ps1"
. $PSScriptRoot"/mst.ps1"
. $PSScriptRoot"/ast.ps1"
. $PSScriptRoot"/wst.ps1"
. $PSSCriptRoot"/lst.ps1"

$bliu = bliu
$im = [Microsoft.VisualBasic.Interaction]::InputBox("What is the flag ?", "Flag")
$fst = en $im
$i = 0
$fin = ""
& GetFlag
idot
while($i -lt $fst.length)
{
        $io = en $bliu[$i]
        $fin += $fst[$i]+$io
        ++$i

}
$final = bs $fin.replace(" ", "") 
$flag = "NjM2ODY5NjU2RTc2MzY4NjE3NDM2QzZGNzU3MDZDNkY3NTY5NzM2Njg2MTYzNkI5NjM2ODY1NzY3MjY1NjI3MjY1NjI2OTczNjczNzE2QzY5NzYyNkM2OTZFNjQ2MTczNkM3Mjc3MDZGNzc2RTM3MDZGNzc2NTcyNzM2ODY1NkM2QzRENjk2MzcyNkY3MzZGNjY3NDY3MjYxNkU2NDU2QzY5NzM3NDcwNzI2RjY2QzZGNzU3NjY1NzZDNjk2RjZFNkM2OTZGNkU2RTY1NzY3NkY3NDY3MDc5NzQ2ODZGNkU3MDY1NzI2Qzc2M0I2QTYxNzY2MTYzNkY2MjZGNkM1NjM2OTczNjM2RjA3MDY5N0E3QTYxNjg2NTZDNkMzNjU2RTY2NjU3MjA2ODYxNjM2QjY1NzI2NDY5NzM2MzZGNzI2NDc2ODYxNjM2QjYxNzQ2ODZGNkU3NjU2RTY2NjE2RTc0NjM2ODY5NkU2RjY5NzMzNzI3NTczNzM2NTM3MDZGNzU3NDY5NkU2NTc0NzI3NTZENzA1NjE2QzY2NzI2NTczNjM2RjI3MzY4NjE3MjY1NzA2RjY5NkU3NDZBNjU2NTQ3MjZGNzA2MzY4NjE2OTZFMzZENjk2NzZFNkY2RTczNjU3ODc5NjczNkM3NTcyNzA4Njk2RTY2NjE3NTc4NzM2NTYzNjk2RTY5NzQ2OTYxNkM2OTczNjU3MkU2RjZCODZFNkY2RTZGNzU2OTU3MDY5NjU2NDY2MzY4NjE3NTczNzM3NTcyNjU2QzY5NzQ3NjM2ODYxNjk3MzY1MjY2NjE3NTc0NjU3NTY5NkM3NDYxNjI2QzY1MzczNzE2QzM2RDZGNkU2NzZGNjQ2MjZENzk3MzcxNkM0NkY3MjYxNjM2QzY1NjYxNzY2OTZGNkU3NjZGNjk3NDc1NzI2NTM2RDZGNzQ2RjA3Mzc1N0E3NTZCNjk2MjZENzc3NkY3MjY0Njk2RTYxNzQ2NTc1NzIyNjc3MzZENjM3OTYyNjU3MjU2NDY5Njc2OTc0NjE2QzA2NDYxNkQ3MzZGNzY2MTZDNjQzNkY3MjY1NkM3MzYxNkUwNjk2RTY2NjU2Mzc0NjU2NDczNjg2NTZDNkM3NkY3NTYxNjk3NjE3MDcwNkM2NTZDNjk2RTc1NzgzNjE3MjYzNjgzNkQ2MTZCNjk3Mzc1NzM2ODY5NTYyNjk2NTcyNjUyNjg2Rjc1NjI2QzZGNkU0MzZGNzU2MzZGNzU0NEM2Rjc1Njk3Mzg1MjZGNjk1MjY1NkU2RTY1MzQ2NjE2RTY2NzI2NTZDNzU2MzY4NjUzNzM2RjYzNkI2NTc0NjM2ODYxNzU3MzczNjU3NDc0NjUzNDM2NTZDNjU3Mzc0Njk2RTE2MjcyNkY2MzYxNkU3NDY1NjI3MjY1NjI2OTczNDczNkY3NTcwNjVDNjM2ODZGNzU2QzY1NzY3MjY1NTYyNjE2OTczNjU3MkY2NTZENjI3MjYxNzM3MzY1NzI2NDZGNzI2RDY5NzIyNjI2RjY5NzI2NTE2QTY1NjE2RTZENkY3NTZDNjk2RTc2ODYxNzI3Mjc5RDcwNkY3NDc0NjU3Mg=="  
if ($final -eq $flag)
{
    Write-Host "Bravo tu as trouvé le flag"
    ilot
}
else
{
    Write-Host "Meh"
    ipot
    
}
```
mst.ps1
```
Function GetFlag()
{
    $raw = (invoke-webrequest -uri "https://pastebin.com/raw/pfBh2LAs").content
    return $raw
}
```

til.ps1
```
Function bliu()
{
    $raw = (invoke-webrequest -uri "https://pastebin.com/raw/HuKuR4TZ").content
    $raw = $raw.split(";")
    return $raw
}
```

ul.ps1
```
function bs($po)
{
    $rt = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($po))
    return $rt
}
```

wst.ps1
```
Function ilot()
{
    write-host "https://www.youtube.com/watch?v=04854XqcfCY"
}
```
xpo.ps1
```
Function en($a)
{
    $b = $a.ToCharArray();
    Foreach ($element in $b) {$c = $c + " " + [System.String]::Format("{0:X}", [System.Convert]::ToUInt32($element))}
    $c
}
```

En analysant un peu les différents script on remarque que le script principal est mnt.ps1 qui appel tous les autres scripts:

```
. $PSScriptRoot"/til.ps1"
. $PSScriptRoot"/xpo.ps1"
. $PSScriptRoot"/ut.ps1"
. $PSScriptRoot"/mst.ps1"
. $PSScriptRoot"/ast.ps1"
. $PSScriptRoot"/wst.ps1"
. $PSSCriptRoot"/lst.ps1"
```

Dans un premier temps, il enregistre le retour de la fonction bliu contenu dans til.ps1 dans une variable $bliu:

```
$bliu = bliu
```

Si on regarde la fonction bliu on recupère simplement le contenu de https://pastebin.com/raw/HuKuR4TZ et ajoute les différents mots dans un tableau.

```
Function bliu()
{
    $raw = (invoke-webrequest -uri "https://pastebin.com/raw/HuKuR4TZ").content
    $raw = $raw.split(";")
    return $raw
}
```

Ensuite le script ouvre une inputbox et enregistre l'entrée de l'utilisateur dans la variable $im.
À la ligne suivante la valeur de cette variable est encodée avec la fonction en.

```
$im = [Microsoft.VisualBasic.Interaction]::InputBox("What is the flag ?", "Flag")
$fst = en $im
```

La fonction en va juste passer la chaîne en hexadecimal:

```
Function en($a)
{
    $b = $a.ToCharArray();
    Foreach ($element in $b) {$c = $c + " " + [System.String]::Format("{0:X}", [System.Convert]::ToUInt32($element))}
    $c
}
```

Dans la suite du code on a d'autres fonctions useless puis une boucle qui va récupèrer chaque mot de notre array $bliu, le convertir en hexdecimal et le concaténer avec une partie de l'hexa du flag.
Cette chaine est ensuite encodée en base 64.

```
while($i -lt $fst.length)
{
        $io = en $bliu[$i]
        $fin += $fst[$i]+$io
        ++$i

}
$final = bs $fin.replace(" ", "") 
```

Pour récupèrer le flag il faut tout simplement faire l'exercice inverse sur:

```
NjM2ODY5NjU2RTc2MzY4NjE3NDM2QzZGNzU3MDZDNkY3NTY5NzM2Njg2MTYzNkI5NjM2ODY1NzY3MjY1NjI3MjY1NjI2OTczNjczNzE2QzY5NzYyNkM2OTZFNjQ2MTczNkM3Mjc3MDZGNzc2RTM3MDZGNzc2NTcyNzM2ODY1NkM2QzRENjk2MzcyNkY3MzZGNjY3NDY3MjYxNkU2NDU2QzY5NzM3NDcwNzI2RjY2QzZGNzU3NjY1NzZDNjk2RjZFNkM2OTZGNkU2RTY1NzY3NkY3NDY3MDc5NzQ2ODZGNkU3MDY1NzI2Qzc2M0I2QTYxNzY2MTYzNkY2MjZGNkM1NjM2OTczNjM2RjA3MDY5N0E3QTYxNjg2NTZDNkMzNjU2RTY2NjU3MjA2ODYxNjM2QjY1NzI2NDY5NzM2MzZGNzI2NDc2ODYxNjM2QjYxNzQ2ODZGNkU3NjU2RTY2NjE2RTc0NjM2ODY5NkU2RjY5NzMzNzI3NTczNzM2NTM3MDZGNzU3NDY5NkU2NTc0NzI3NTZENzA1NjE2QzY2NzI2NTczNjM2RjI3MzY4NjE3MjY1NzA2RjY5NkU3NDZBNjU2NTQ3MjZGNzA2MzY4NjE2OTZFMzZENjk2NzZFNkY2RTczNjU3ODc5NjczNkM3NTcyNzA4Njk2RTY2NjE3NTc4NzM2NTYzNjk2RTY5NzQ2OTYxNkM2OTczNjU3MkU2RjZCODZFNkY2RTZGNzU2OTU3MDY5NjU2NDY2MzY4NjE3NTczNzM3NTcyNjU2QzY5NzQ3NjM2ODYxNjk3MzY1MjY2NjE3NTc0NjU3NTY5NkM3NDYxNjI2QzY1MzczNzE2QzM2RDZGNkU2NzZGNjQ2MjZENzk3MzcxNkM0NkY3MjYxNjM2QzY1NjYxNzY2OTZGNkU3NjZGNjk3NDc1NzI2NTM2RDZGNzQ2RjA3Mzc1N0E3NTZCNjk2MjZENzc3NkY3MjY0Njk2RTYxNzQ2NTc1NzIyNjc3MzZENjM3OTYyNjU3MjU2NDY5Njc2OTc0NjE2QzA2NDYxNkQ3MzZGNzY2MTZDNjQzNkY3MjY1NkM3MzYxNkUwNjk2RTY2NjU2Mzc0NjU2NDczNjg2NTZDNkM3NkY3NTYxNjk3NjE3MDcwNkM2NTZDNjk2RTc1NzgzNjE3MjYzNjgzNkQ2MTZCNjk3Mzc1NzM2ODY5NTYyNjk2NTcyNjUyNjg2Rjc1NjI2QzZGNkU0MzZGNzU2MzZGNzU0NEM2Rjc1Njk3Mzg1MjZGNjk1MjY1NkU2RTY1MzQ2NjE2RTY2NzI2NTZDNzU2MzY4NjUzNzM2RjYzNkI2NTc0NjM2ODYxNzU3MzczNjU3NDc0NjUzNDM2NTZDNjU3Mzc0Njk2RTE2MjcyNkY2MzYxNkU3NDY1NjI3MjY1NjI2OTczNDczNkY3NTcwNjVDNjM2ODZGNzU2QzY1NzY3MjY1NTYyNjE2OTczNjU3MkY2NTZENjI3MjYxNzM3MzY1NzI2NDZGNzI2RDY5NzIyNjI2RjY5NzI2NTE2QTY1NjE2RTZENkY3NTZDNjk2RTc2ODYxNzI3Mjc5RDcwNkY3NDc0NjU3Mg==
```



On fait un base64 decode et on obtient:

```
636869656E76368617436C6F75706C6F75697366861636B9636865767265627265626973673716C697626C696E6461736C727706F776E3706F7765727368656C6C4D6963726F736F6674672616E6456C69737470726F66C6F75766576C696F6E6C696F6E6E657676F746707974686F6E7065726C763B6A617661636F626F6C5636973636F070697A7A6168656C6C3656E66657206861636B6572646973636F726476861636B6174686F6E7656E66616E746368696E6F6973372757373653706F7574696E657472756D705616C66726573636F27368617265706F696E746A65654726F70636861696E36D69676E6F6E736578796736C7572708696E66617578736563696E697469616C69736572E6F6B86E6F6E6F756957069656466368617573737572656C697476368616973652666175746575696C7461626C65373716C36D6F6E676F64626D7973716C46F7261636C6566176696F6E766F697475726536D6F746F073757A756B69626D7776F7264696E6174657572267736D637962657256469676974616C064616D736F76616C6436F72656C73616E0696E6665637465647368656C6C76F75616976170706C656C696E757836172636836D616B697375736869562696572652686F75626C6F6E436F75636F7544C6F7569738526F6952656E6E65346616E6672656C756368653736F636B657463686175737365747465343656C657374696E162726F63616E74656272656269734736F757065C63686F756C657672655626169736572F656D62726173736572646F726D69722626F69726516A65616E6D6F756C696E76861727279D706F74746572
```

Maintenant il suffit de retirer l'hexadecimal de chaque mot provenant de https://pastebin.com/raw/HuKuR4TZ et de recupèrer les caractères entre chaque mot.

Enfin on a le code hexadecimal de notre flag, il ne reste plus qu'à le décoder.
