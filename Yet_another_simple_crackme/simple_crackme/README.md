# simple_crackme

Un simple programme qu'il faut reverse en entrant la bonne chaîne de caractères.

## Résolution
```
$ ./simple_crackme
RTFM little crackme :)
Password : fkeaopkfpoeaf
Nope :(
```

```
$ ./simple_crackme
RTFM little crackme :)
Password : sigsegv{piXis_is_seXy}
Well played :)
```


## Description
Yet another simple crackme chall. Just run it.

## Hints
(publish the source code)

## Flag
sigsegv{piXis_is_seXy}

## But
Trouver la clé du challenge en reversant le binaire.

## Usage
Lancer le binaire sur une architecture x86-64
```
$ ./rtfm
RTFM little crackme :)
Password :
```

## Composition
Le challenge se présente sous la forme d'un binaire ELF 64bits.
La source du challenge est fournie en ASM. Puisque c'est comme ça qu'il a été conçu.
La ligne de compilation est également fournie.
```
$ nasm -f elf64 -o simple_crackme.o simple_crackme.asm
$ ld -o simple_crackme simple_crackme.o
$ file simple_crackme
rtfm: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, not stripped
```


## TODO
Est-ce qu'on le compile en strippé, pour le rendre un peu plus dur ?