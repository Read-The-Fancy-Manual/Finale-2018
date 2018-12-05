.ROMDMG
.NAME "NCLOCKED"
.CARTRIDGETYPE 0
.RAMSIZE 0
.COMPUTEGBCHECKSUM
.COMPUTEGBCOMPLEMENTCHECK
.LICENSEECODENEW "00"
.EMPTYFILL $00

.MEMORYMAP
SLOTSIZE $4000
DEFAULTSLOT 0
SLOT 0 $0000
SLOT 1 $4000
.ENDME
 
.ROMBANKSIZE $4000
.ROMBANKS 2
.BANK 0 SLOT 0

.ENUM $C000
Random_Seed DB
Level DB
PlayerX DB
PlayerY DB
Text_NoControls DSB 33
Text_NoScrolling DSB 47
Text_Panel DSB 35
Text_WrongCode DSB 48
.ENDE


.ORG $0040
call VBlank
reti


.ORG $0100
nop
jp start


.ORG $0104
.DB $CE,$ED,$66,$66,$CC,$0D,$00,$0B,$03,$73,$00,$83,$00,$0C
.DB $00,$0D,$00,$08,$11,$1F,$88,$89,$00,$0E,$DC,$CC,$6E,$E6
.DB $DD,$DD,$D9,$99,$BB,$BB,$67,$63,$6E,$0E,$EC,$CC,$DD,$DC
.DB $99,$9F,$BB,$B9,$33,$3E


.org $0150
start:
	di
	ld sp,$FFF4 ;SP=$FFF4

	; Couper le son
	xor a ;A=0
	ldh ($26),a ;($FF26)=A

	; Attendre la fin du vblank
	call waitvbl

	; Eteindre l'écran
	xor a ;A=0
	ldh ($40),a ;($FF40)=A

	; Copier les sprites de la ROM vers la VRAM
	ld bc,$9E*8*2
	ld de,Tiles ;DE=Adresse du label "Tiles", pointeur ROM
	ld hl,$8000 ;HL=$8000, pointeur VRAM
	ldt:
		ld a,(de) ;A=(DE)
		ldi (hl),a ;(HL)=A et incrémenter HL
		inc de ;Incrémenter DE
		dec bc ;Décrémenter BC (compteur d'itérations)
		ld a,c
		or b
		jr nz,ldt ;Sauter à ldt si BC différent de 0
		
	; Effacer le Background
	ld de,32*32 ;DE=1024
	ld hl,$9800 ;HL=$9800
	clmap:
		xor a ;A=0
		ldi (hl),a ;(HL)=A et incrémenter HL
		dec de ;Décrémenter DE
		ld a,e ;A=E
		or d ;A=A OR D (soit A=E OR D)
		jr nz,clmap ;Sauter à clmap si DE différent de 0
		
	call initMap01
		
	; Effacer l'OAM (position des sprites, etc)
	ld hl,$FE00 ;HL=$FE00
	ld b,40*4 ;B=160
	clspr:
		ld (hl),$00 ;(HL)=0
		inc l ;Incrémenter L
		dec b ;Décrementer B
		jr nz,clspr ;Sauter à clspr si B différent de 0

	; Mettre les scrolls du Background à 0
	xor a ;A=0
	ldh ($42),a ;($FF42)=A
	ldh ($43),a ;($FF43)=A

	; Placement des sprites dans l'OAM
	ld hl,$FE00 ;HL=$FE00
	; Player Top ($10)
	ld (hl),$80 ;(HL)=$80 OAM sprite Y
	inc l ;Incrémenter L
	ld (hl),$08 ;(HL)=$80 OAM sprite X
	inc l ;Incrémenter L
	ld (hl),$1D ;(HL)=2 OAM sprite tile
	inc l ;Incrémenter L
	ld (hl),$00 ;(HL)=0 OAM sprite attribut
	inc l ;Incrémenter L
	; Player Bottom ($04)
	ld (hl),$88 ; Y
	inc l ;Incrémenter L
	ld (hl),$08 ; X
	inc l ;Incrémenter L
	ld (hl),$1E ; Tile
	inc l ;Incrémenter L
	ld (hl),$00 ; Attribut
	
	; Initialisation des variables
	ld a,$01
	ld (Level),a
	ld a,$2E
	ld (PlayerX),a
	ld a,$88
	ld (PlayerY),a
	call inittexts
	
	; Initialisation de la palette
	ld a,%11100100 ;11=Noir 10=Gris foncé 01=Gris clair 00=Blanc/transparent
	ldh ($47),a ; Palette BG
	ldh ($48),a ; Palette sprite 0
	ldh ($49),a ; Palette sprite 1 (ne sert pas)
	ld a,%10010011 ; Ecran on, Background on, tiles à $8000
	ldh ($40),a
	ld a,%00010000 ; Interruptions VBlank activées
	ldh ($41),a
	ld a,%00000001 ; Interruptions VBlank activées (double activation à la con)
	ldh ($FF),a
	ei ;Activer la prise en charge des interruptions
	loop:
		jr loop ;Boucle infinie


VBlank:
	push af ;Empiler AF
	push hl ;Empiler HL
	
	ld a,(Level)
	dec a
	jr nz,nolvl1
		call level1
		jr nz,end
	nolvl1:
	dec a
	jr nz,nolvl2
		call level2
		jr nz,end
	nolvl2:
	dec a
	jr nz,nolvl3
		call level3
		jr nz,end
	nolvl3:
	end:

	pop hl ;Dépiler HL
	pop af ;Dépiler AF
	ret

	
playermovright:
	ld hl,Text_NoControls
	push hl
	call printtext
	playermovright_lp:
		jr playermovright_lp
	ld a,(PlayerX)
	; inc a
	nop
	ld (PlayerX),a
	ret

	
playermovleft:
	ld hl,Text_NoControls
	push hl
	call printtext
	playermovleft_lp:
		jr playermovleft_lp
	ld a,(PlayerX)
	; dec a
	nop
	ld (PlayerX),a
	ret
	
scrolling:
	ld a,(PlayerX)
	cp $A9
	jr c,scrolling_end
		ld hl,Text_NoScrolling
		push hl
		call printtext
		scrolling_lp:
			jr scrolling_lp
	scrolling_end:
	; ld a,(PlayerX)
	; cp $4C*3/2
	; jr c,noscrollr
		; dec a
		; ld (PlayerX),a
		; ld hl,$FF43
		; ld a,(hl)
		; inc a
		; ld (hl),a
	; noscrollr:
	; ld a,(PlayerX)
	; cp $48*1/2
	; jr nc,noscrolll
		; inc a
		; ld (PlayerX),a
		; ld hl,$FF43
		; ld a,(hl)
		; dec a
		; ld (hl),a
	; noscrolll:
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	ret

rnd:
	ld hl,$FF04
	ld a,(hl)
	add 9
	rnd_lp:
		sub 9
		cp 10
		jr nc,rnd_lp
	ld b,a
	ld a,(Random_Seed)
	inc a
	ld (Random_Seed),a
	; add 3
	; rnd_lp:
		; sub 4
		; cp 4
		; jr nc,rnd_lp
	; cp 0
	; jr nz,rnd_no_a
		; ld b,1
	; rnd_no_a:
	; dec a
	; jr nz,rnd_no_b
		; ld b,3
	; rnd_no_b:
	; dec a
	; jr nz,rnd_no_c
		; ld b,3
	; rnd_no_c:
	; dec a
	; jr nz,rnd_no_d
		; ld b,7
	; rnd_no_d:
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	ret


level1:
	; Lire les touches directionnelles
	ld a,%00100000 ; Selection touches de direction
	call readkeys

	; Si "Droite", PlayerX++
	bit $0,b
	jr nz,lvl1_nor
		call playermovright
	lvl1_nor:

	; Si "Gauche", PlayerX--
	bit $1,b
	jr nz,lvl1_nol
		call playermovleft
	lvl1_nol:
	
	; Si "Haut", Passer la porte
	bit $2,b
	jr nz,lvl1_nou
		ld hl,$FF43
		ld a,(hl)
		ld b,a
		ld a,(PlayerX)
		add b
		cp $88
		jr z,lvl1_nou
		jr c,lvl1_nou
		cp $90
		jr nc,lvl1_nou
		call fadeout
		; call initMap02
		; ld a,2
		nop
		nop
		call initMap03
		ld a,3
		nop
		nop
		ld (Level),a
		ld a,$00
		ldh ($43),a
		call fadein
	lvl1_nou:
	
	call scrolling
	
	; Lire les boutons (A, B, Start, Select)
	; ld a,%00010000
	; call readkeys
	
	call drawplayer
	ret


level2:
	; Lire les touches directionnelles
	ld a,%00100000 ; Selection touches de direction
	call readkeys

	; Si "Droite", PlayerX++
	bit $0,b
	jr nz,lvl2_nor
		call playermovright
	lvl2_nor:

	; Si "Gauche", PlayerX--
	bit $1,b
	jr nz,lvl2_nol
		call playermovleft
	lvl2_nol:
	
	; Si "Haut", Passer la porte
	bit $2,b
	jp nz,lvl2_nou
		; Test de la porte
		ld hl,$FF43
		ld a,(hl)
		ld b,a
		ld a,(PlayerX)
		add b
		cp $C8
		jr z,lvl2_nou_ndoor
		jr c,lvl2_nou_ndoor
		cp $D0
		jr nc,lvl2_nou_ndoor
		; Si Le code est bon
		ld a,($9934)
		cp $8A
		jr nz,lvl2_wrgcd
		ld a,($9937)
		cp $8C
		jr nz,lvl2_wrgcd
		ld a,($993A)
		cp $8C
		jr nz,lvl2_wrgcd
		ld a,($993D)
		cp $90
		jr nz,lvl2_wrgcd
		call fadeout
		call showPwd
		lvl2_wrgcd:
		; Sinon
		ld hl,Text_WrongCode
		push hl
		call printtext
		lvl2_wrgcd_lp:
			ld a,%00100000
			call readkeys
			bit $2,b
			jr z,lvl2_wrgcd_lp
		lvl2_wrgcd_lp2:
			ld a,%00010000
			call readkeys
			bit $0,b
			jr nz,lvl2_wrgcd_lp2
		ld a,$77
		call cleartext
		; Test du panneau
		lvl2_nou_ndoor:
		ld hl,$FF43
		ld a,(hl)
		ld b,a
		ld a,(PlayerX)
		add b
		cp $90
		jr z,lvl2_nou
		jr c,lvl2_nou
		cp $98
		jr nc,lvl2_nou
		ld hl,Text_Panel
		push hl
		call printtext
		lvl2_panel_lp:
			ld a,%00100000
			call readkeys
			bit $2,b
			jr z,lvl2_panel_lp
		lvl2_panel_lp2:
			ld a,%00010000
			call readkeys
			bit $0,b
			jr nz,lvl2_panel_lp2
		ld a,$77
		call cleartext
	lvl2_nou:
	
	call scrolling
	
	; Lire les boutons (A, B, Start, Select)
	ld a,%00010000
	call readkeys
	
	bit $0,b
	jr nz,lvl2_noa
		; Réinitialiser le seed (désactivé)
		; ld a,$00
		; ld (Random_Seed),a
		ld c,4
		ld d,$34
		lvl2_noa_lp:
			call rnd
			ld h,$99
			ld l,d
			ld a,b
			add $89
			ldi (hl),a
			inc d
			inc d
			inc d
			dec c
			jr nz,lvl2_noa_lp
			lvl2_noa_rls:
				call readkeys
				bit $0,b
				jr z,lvl2_noa_rls
	lvl2_noa:
	
	call drawplayer
	ret


level3:
	; Lire les touches directionnelles
	ld a,%00100000 ; Selection touches de direction
	call readkeys

	; Si "Droite", PlayerX++
	bit $0,b
	jr nz,lvl3_nor
		ld a,(PlayerX)
		cp $1C
		jr nc,lvl3_nol
		call playermovright
	lvl3_nor:

	; Si "Gauche", PlayerX--
	bit $1,b
	jr nz,lvl3_nol
		ld a,(PlayerX)
		cp $14
		jr z,lvl3_nol
		jr c,lvl3_nol
		call playermovleft
	lvl3_nol:
	
	; call scrolling
	
	; Lire les boutons (A, B, Start, Select)
	; ld a,%00010000
	; call readkeys
	
	call drawplayer
	ret

	
showPwd:
	; Effacer le Background
	ld de,32*32 ;DE=1024
	ld hl,$9800 ;HL=$9800
	showPwdclmap:
		call waitvbl
		xor a ;A=0
		ldi (hl),a ;(HL)=A et incrémenter HL
		dec de ;Décrémenter DE
		ld a,e ;A=E
		or d ;A=A OR D (soit A=E OR D)
		jr nz,showPwdclmap ;Sauter à clmap si DE différent de 0
		
	; Effacer le joueur
	ld hl,$FE00
	ld c,8
	showPwdclplr:
		ld a,$00
		ldi (hl),a
		dec c
		jr nz,showPwdclplr
	
	; Réinitialiser le scroll
	ld a,$00
	ldh ($43),a
	
	; Afficher le text
	call waitvbl
	ld hl,$9A41
	ld a,$35
	ldi (hl),a
	ld a,$5B
	ldi (hl),a
	ld a,$5A
	ldi (hl),a
	ld a,$53
	ldi (hl),a
	ld a,$5E
	ldi (hl),a
	ld a,$4D
	ldi (hl),a
	ld a,$60
	ldi (hl),a
	ld a,$61
	ldi (hl),a
	ld a,$58
	ldi (hl),a
	ld a,$4D
	ldi (hl),a
	ld a,$60
	ldi (hl),a
	ld a,$55
	ldi (hl),a
	ld a,$5B
	ldi (hl),a
	ld a,$5A
	ldi (hl),a
	ld a,$5F
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$6C
	ldi (hl),a
	ldi (hl),a
	call waitvbl
	ld hl,$9A60
	ld a,$4B
	ldi (hl),a
	ld a,$5B
	ldi (hl),a
	ld a,$61
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$5E
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$4D
	ldi (hl),a
	ld a,$4F
	ldi (hl),a
	ld a,$54
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$60
	ldi (hl),a
	ld a,$54
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$5A
	ldi (hl),a
	ld a,$50
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$5B
	ldi (hl),a
	ld a,$52
	ldi (hl),a
	call waitvbl
	ld hl,$9A81
	ld a,$60
	ldi (hl),a
	ld a,$54
	ldi (hl),a
	ld a,$55
	ldi (hl),a
	ld a,$5F
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$4D
	ldi (hl),a
	ld a,$63
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$5F
	ldi (hl),a
	ld a,$5B
	ldi (hl),a
	ld a,$59
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$53
	ldi (hl),a
	ld a,$4D
	ldi (hl),a
	ld a,$59
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$67
	ldi (hl),a
	call waitvbl
	ld hl,$9AA1
	ld a,$3A
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$5E
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$55
	ldi (hl),a
	ld a,$5F
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$60
	ldi (hl),a
	ld a,$54
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$52
	ldi (hl),a
	ld a,$58
	ldi (hl),a
	ld a,$4D
	ldi (hl),a
	ld a,$53
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$69
	ldi (hl),a
	
	; Old Pass : 1Mm4_6B_45m_Pr()_!
	; Tiles (Rev) :		6C 28 74 73 5E 42 28 59 2E 2D 28 34 2F 28 2D 59 3F 2A
	; rnd :				03 01 07 03 03 01 07 03 03 01 07 03 03 01 07 03 03 01
	; Xor rnd :			6F 29 73 70 5D 43 2F 5A 2D 2C 2F 37 2C 29 2A 5A 3C 2B
	; Mov :				56 54 56 54 56 54 56 54 56 54 56 54 56 54 56 54 56 54
	; Xor mov :			39 7D 25 24 0B 17 79 0E 7B 7A 79 63 7A 7D 7C 0E 6A 7F
	
	; Old New Pass : K3wl_c_3nf1n_f1ni!
	; Tiles (Rev) :		6C 55 5A 2A 52 28 5A 2A 52 5A 2C 28 4F 28 58 63 2C 3D
	; rnd :				03 01 07 03 03 01 07 03 03 01 07 03 03 01 07 03 03 01
	; Xor rnd :			6F 54 5D 29 51 29 5D 29 51 5B 2B 2B 4C 29 5F 60 2F 3C
	; Mov :				56 54 56 54 56 54 56 54 56 54 56 54 56 54 56 54 56 54
	; Xor mov :			39 00 0B 7D 07 7D 0B 7D 07 0F 7D 7F 1A 7D 09 34 79 68
	
	; Génération du pass
	ld a,$23
	push af
	ld a,$39
	push af
	ld a,$1B
	push af
	ld a,$27
	push af
	ld a,$0F
	push af
	ld a,$02
	push af
	ld a,$7D
	push af
	ld a,$7F
	push af
	ld a,$6F
	push af
	ld a,$33
	push af
	ld a,$24
	push af
	ld a,$35
	push af
	ld a,$06
	push af
	ld a,$04
	push af
	ld a,$0E
	push af
	ld a,$04
	push af
	ld a,$00
	push af
	ld a,$0A
	push af
	
	; Calcul et affichage du pass
	ld a,$00
	ld (Random_Seed),a
	ld hl,$9AE1
	ld c,9
	spwd_ppwd:
		ld a,$55
		ld (PlayerX),a
		call playermovleft
		ld a,(PlayerX)
		ld b,a
		pop af
		xor b
		push af
		call rnd
		pop af
		xor b
		call waitvbl
		ldi (hl),a
		ld a,$55
		ld (PlayerX),a
		call playermovright
		ld a,(PlayerX)
		ld b,a
		pop af
		xor b
		push af
		call rnd
		pop af
		xor b
		call waitvbl
		ldi (hl),a
		dec c
		jr nz,spwd_ppwd
	
	; Inverser la palette
	ld a,%00011011
	ldh ($47),a
	ldh ($48),a
	
	spwd_end:
		ld a,($FF42)
		inc a
		ldh ($42),a
		ld c,$FF
		spwd_end_lp:
			call waitvbl
			dec c
			jr nz,spwd_end_lp
		jr spwd_end
	ret

	
initMap01:
	; Dessiner le sol
	ld c,32
	ld hl,$9A00
	ld a,$01
	imap01flr:
		ldi (hl),a
		dec c
		jr nz,imap01flr
	ld c,32
	ld hl,$9A20
	ld a,$02
	imap01flr2:
		ldi (hl),a
		dec c
		jr nz,imap01flr2
	; Dessiner le batiment
	ld b,6
	ld hl,$9946
	ld e,l
	imap01bat:
		ld a,$04
		ldi (hl),a
		ld c,11
		imap01bat2:
			ld a,$03
			ldi (hl),a
			dec c
			jr nz,imap01bat2
		ld a,$05
		ldi (hl),a
		ld a,$20
		add e
		ld e,a
		ld l,e
		dec b
		jr nz,imap01bat
	ld c,11
	ld hl,$9926
	ld a,$07
	ldi (hl),a
	ld a,$06
	imap01bat3:
		ldi (hl),a
		dec c
		jr nz,imap01bat3
	ld a,$08
	ldi (hl),a
	ld hl,$99F0
	ld a,$09
	ldi (hl),a
	ld a,$0A
	ldi (hl),a
	ld hl,$99D0
	ld a,$09
	ldi (hl),a
	ld a,$0A
	ldi (hl),a
	ld hl,$99B0
	ld a,$0B
	ldi (hl),a
	ld a,$0C
	ldi (hl),a
	ld b,4
	ld hl,$9969
	ld e,l
	ld d,$0D
	imap01logo:
		ld c,4
		imap01logo2:
			ld a,d
			ldi (hl),a
			inc d
			dec c
			jr nz,imap01logo2
		ld a,$20
		add e
		ld e,a
		ld l,e
		dec b
		jr nz,imap01logo
	ret

initMap02:
	; Replacer le joueur
	ld a,$14
	ld (PlayerX),a
	ld a,$80
	ld (PlayerY),a

	; Dessiner les bords et le fond
	ld hl,$9800
	ld c,7
	imap02brd:
		ld d,32
		call waitvbl
		ld a,$77
		imap02brd2:
			ldi (hl),a
			dec d
			jr nz,imap02brd2
		dec c
		jr nz,imap02brd
	ld c,8
	imap02bck:
		ld d,32
		call waitvbl
		ld a,$78
		imap02bck2:
			ldi (hl),a
			dec d
			jr nz,imap02bck2
		dec c
		jr nz,imap02bck
	ld c,17
	imap02brd3:
		ld d,32
		call waitvbl
		ld a,$77
		imap02brd4:
			ldi (hl),a
			dec d
			jr nz,imap02brd4
		dec c
		jr nz,imap02brd3
	; Dessiner les portes
	ld b,0
	ld c,2
	imap02door:
		ld hl,$99C1
		ld a,b
		add l
		ld l,a
		ld a,$79
		ldi (hl),a
		ld a,$7A
		ldi (hl),a
		ld hl,$99A1
		ld a,b
		add l
		ld l,a
		ld a,$79
		ldi (hl),a
		ld a,$7A
		ldi (hl),a
		ld hl,$9981
		ld a,b
		add l
		ld l,a
		ld a,$7B
		ldi (hl),a
		ld a,$7C
		ldi (hl),a
		ld a,0
		add $17
		ld b,a
		dec c
		jr nz,imap02door
	; Dessiner les lampes
	ld hl,$9901
	ld c,3
	imap02lmp:
		ld a,$7F
		ldi (hl),a
		inc a
		ldi (hl),a
		ld a,5
		add l
		ld l,a
		dec c
		jr nz,imap02lmp
	ld hl,$9921
	ld c,3
	imap02lmp2:
		ld a,$7D
		ldi (hl),a
		inc a
		ldi (hl),a
		ld a,5
		add l
		ld l,a
		dec c
		jr nz,imap02lmp2
	; Dessiner les cadres
	ld hl,$9913
	ld c,4
	imap02cdr:
		call waitvbl
		ld a,$81
		ldi (hl),a
		inc a
		ldi (hl),a
		inc a
		ldi (hl),a
		dec c
		jr nz,imap02cdr
	ld a,$00
	ld (Random_Seed),a
	ld hl,$9933
	ld c,4
	imap02cdr2:
		call waitvbl
		ld a,$84
		ldi (hl),a
		push hl
		call rnd
		call waitvbl
		pop hl
		ld a,b
		add $89
		ldi (hl),a
		ld a,$85
		ldi (hl),a
		dec c
		jr nz,imap02cdr2
	ld hl,$9953
	ld c,4
	imap02cdr3:
		call waitvbl
		ld a,$86
		ldi (hl),a
		inc a
		ldi (hl),a
		inc a
		ldi (hl),a
		dec c
		jr nz,imap02cdr3
	; Dessiner le panneau
	ld hl,$99B1
	ld a,$94
	ldi (hl),a
	inc a
	ldi (hl),a
	ret

initMap03:
	; Replacer le joueur
	ld a,$18
	ld (PlayerX),a
	ld a,$80
	ld (PlayerY),a
		
	; Effacer le Background
	ld de,32*32 ;DE=1024
	ld hl,$9800 ;HL=$9800
	imap03clmap:
		call waitvbl
		xor a ;A=0
		ldi (hl),a ;(HL)=A et incrémenter HL
		dec de ;Décrémenter DE
		ld a,e ;A=E
		or d ;A=A OR D (soit A=E OR D)
		jr nz,imap03clmap ;Sauter à clmap si DE différent de 0
	
	; Dessiner le sol
	ld hl,$99E0
	ld a,$01
	ld c,32
	imap03flrlp:
		call waitvbl
		ldi (hl),a
		dec c
		jr nz,imap03flrlp
	ld hl,$9A00
	ld a,$02
	ld c,32
	imap03flrlp2:
		call waitvbl
		ldi (hl),a
		dec c
		jr nz,imap03flrlp2
	ld hl,$9A20
	ld a,$02
	ld c,32
	imap03flrlp3:
		call waitvbl
		ldi (hl),a
		dec c
		jr nz,imap03flrlp3
	
	; Dessiner la prison
	call waitvbl
	ld hl,$9981
	ld a,$07
	ldi (hl),a
	ld a,$06
	ldi (hl),a
	ld a,$08
	ldi (hl),a
	ld hl,$99A1
	ld a,$22
	ldi (hl),a
	inc l
	xor $01
	ldi (hl),a
	ld hl,$99C1
	xor $01
	ldi (hl),a
	inc l
	xor $01
	ldi (hl),a
	
	; Texte Level 03
	call waitvbl
	ld hl,$9805
	ld a,$3E
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$62
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$58
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$29
	ldi (hl),a
	ld a,$2C
	ldi (hl),a
	
	; Helptext
	call waitvbl
	ld hl,$9861
	ld a,$49
	ldi (hl),a
	ld a,$4D
	ldi (hl),a
	ld a,$55
	ldi (hl),a
	ld a,$60
	ldi (hl),a
	ld a,$67
	ldi (hl),a
	ldi (hl),a
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$3B
	ldi (hl),a
	ld a,$6D
	ldi (hl),a
	ld a,$59
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$5A
	ldi (hl),a
	ld a,$5B
	ldi (hl),a
	ld a,$60
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$55
	ldi (hl),a
	ld a,$5A
	ldi (hl),a
	ld hl,$9880
	ld a,$60
	ldi (hl),a
	ld a,$54
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$4F
	ldi (hl),a
	ld a,$5B
	ldi (hl),a
	ld a,$5E
	ldi (hl),a
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$4F
	ldi (hl),a
	ld a,$60
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$5C
	ldi (hl),a
	ld a,$58
	ldi (hl),a
	ld a,$4D
	ldi (hl),a
	ld a,$4F
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$6C
	ldi (hl),a
	ld hl,$98A0
	ld a,$46
	ldi (hl),a
	ld a,$54
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$50
	ldi (hl),a
	ld a,$5B
	ldi (hl),a
	ldi (hl),a
	ld a,$5E
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$55
	ldi (hl),a
	ld a,$5F
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$5C
	ldi (hl),a
	ld a,$5E
	ldi (hl),a
	ld a,$5B
	ldi (hl),a
	ld a,$4E
	ldi (hl),a
	ld a,$4D
	ldi (hl),a
	ld a,$4E
	ldi (hl),a
	ld a,$58
	ldi (hl),a
	ld a,$65
	ldi (hl),a
	ld hl,$98C3
	ld a,$4E
	ldi (hl),a
	ld a,$5E
	ldi (hl),a
	ld a,$5B
	ldi (hl),a
	ld a,$57
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$5A
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$4E
	ldi (hl),a
	ld a,$61
	ldi (hl),a
	ld a,$60
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$3B
	ldi (hl),a
	ld a,$6D
	ldi (hl),a
	ld a,$59
	ldi (hl),a
	ld hl,$98E0
	ld a,$5F
	ldi (hl),a
	ld a,$61
	ldi (hl),a
	ld a,$5E
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$55
	ldi (hl),a
	ld a,$60
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$4F
	ldi (hl),a
	ld a,$4D
	ldi (hl),a
	ld a,$5A
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$4E
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$52
	ldi (hl),a
	ld a,$55
	ldi (hl),a
	ld a,$64
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$50
	ldi (hl),a
	ld hl,$9905
	ld a,$51
	ldi (hl),a
	ld a,$4D
	ldi (hl),a
	ld a,$5F
	ldi (hl),a
	ld a,$55
	ldi (hl),a
	ld a,$58
	ldi (hl),a
	ld a,$65
	ldi (hl),a
	ld a,$67
	ldi (hl),a
	ldi (hl),a
	ldi (hl),a
	ret

printtext:
	ld hl,$FF43
	ld a,(hl)
	add 4
	and $F8
	ldh ($43),a
	
	sra a
	sra a
	sra a
	and $1F
	ld hl,$9800
	add l
	ld l,a
	ld a,(hl)
	add $1F
	call bginchl
	ld c,$12
	inc a
	printtext_lp:
		call waitvbl
		call bginchl
		dec c
		jr nz,printtext_lp
	inc a
	call bginchl
	ld c,4
	printtext_lp2:
		push af
		ld b,c
		sla b
		sla b
		sla b
		sla b
		sla b
		ld hl,$FF43
		ld a,(hl)
		sra a
		sra a
		sra a
		and $1F
		ld h,$98
		ld l,b
		add l
		ld l,a
		pop af
		ld a,(hl)
		add $22
		call waitvbl
		call bginchl
		ld d,$12
		ld a,$00
		printtext_lp3:
			call waitvbl
			call bginchl
			dec d
			jr nz,printtext_lp3
		ld a,(hl)
		add $23
		call bginchl
		dec c
		jr nz,printtext_lp2
	call waitvbl
	ld hl,$FF43
	ld a,(hl)
	sra a
	sra a
	sra a
	and $1F
	ld hl,$98A0
	add l
	ld l,a
	ld a,(hl)
	add $24
	call bginchl
	ld c,$12
	inc a
	printtext_lp4:
		call waitvbl
		call bginchl
		dec c
		jr nz,printtext_lp4
	inc a
	call bginchl
	
	pop bc
	pop hl
	push bc
	ld c,(hl)
	ld d,c
	printtext_lp5:
		inc l
		ld a,0
		adc h
		ld h,a
		ld a,(hl)
		push af
		dec c
		jr nz,printtext_lp5
	ld c,d
	ld hl,$FF43
	ld a,(hl)
	sra a
	sra a
	sra a
	and $1F
	ld hl,$9821
	add l
	ld l,a
	printtext_lp6:
		call waitvbl
		pop af
		call bginchl
		push hl
		ld hl,$FF43
		ld a,(hl)
		sra a
		sra a
		sra a
		and $1F
		pop hl
		ld e,a
		ld a,l
		sub e
		and $1F
		cp $13
		jr nz,printtext_lp6_nnl
			ld a,$0E
			push af
			ld a,l
			and $1F
			cp $0C
			jr nc,printtext_lp6_mnl
				pop af
				add $20
				push af
			printtext_lp6_mnl:
			pop af
			add l
			ld l,a
		printtext_lp6_nnl:
		dec c
		jr nz,printtext_lp6
	ret

bginchl:
	push af
	push bc
	push de
	ld (hl),a
	ld a,l
	and $E0
	ld b,a
	inc l
	ld a,l
	and $1F
	or b
	ld l,a
	pop de
	pop bc
	pop af
	ret
	
cleartext: ; Param : a -> tile index
	ld hl,$9800
	ld c,10
	cleartext_lp:
		ld d,$14
		ld e,a
		call waitvbl
		ld a,e
		cleartext_lp2:
			ldi (hl),a
			dec d
			jr nz,cleartext_lp2
		dec c
		jr nz,cleartext_lp
	ret


fadeout:	
	ld a,%11100100
	fdo:
		sra a
		sra a
		or $C0
		ldh ($47),a
		ldh ($48),a
		ld c,$7F
		fdo_lp:
			call waitvbl
			dec c
			jr nz,fdo_lp
		cp %11111111
		jr nz,fdo
	ret
	
fadein:
	ld a,%11111110
	ldh ($47),a
	ldh ($48),a
	ld c,$7F
	lvl1_fdo_lp:
		call waitvbl
		dec c
		jr nz,lvl1_fdo_lp
	ld a,%11111001
	ldh ($47),a
	ldh ($48),a
	ld c,$7F
	lvl1_fdo_lp2:
		call waitvbl
		dec c
		jr nz,lvl1_fdo_lp2
	ld a,%11100100
	ldh ($47),a
	ldh ($48),a
	ld c,$7F
	lvl1_fdo_lp3:
		call waitvbl
		dec c
		jr nz,lvl1_fdo_lp3
	ret
	

drawplayer:
	; Dessiner le player
	ld hl,$FE00
	ld a,(PlayerY)
	sub 8
	ld (hl),a ; OAM player Y
	inc l
	ld a,(PlayerX)
	ld (hl),a ; OAM player X
	ld hl,$FE04
	ld a,(PlayerY)
	ld (hl),a ; OAM player Y
	inc l
	ld a,(PlayerX)
	ld (hl),a ; OAM player X
	ret

	
readkeys:
	ldh ($00),a
	ld b,60
	rloop:
		ldh a,($00)
		dec b
		jr nz,rloop
	ld b,a
	ret


waitvbl:
	push af
	push bc
	wvbllp:
		ldh a,($44) ;A=($FF44)
		cp 144 ;Comparer A avec 144
		jr c, wvbllp ;Sauter à wvbllp si A<144
	pop bc
	pop af
	ret
	
	
inittexts:
	ld hl,Text_NoControls
	ld a,32
	ldi (hl),a
	ld a,$6C
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$62
	ldi (hl),a
	ld a,$5B
	ldi (hl),a
	ld a,$59
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$60
	ldi (hl),a
	ld a,$6D
	ldi (hl),a
	ld a,$5A
	ldi (hl),a
	ld a,$4D
	ldi (hl),a
	ld a,$4F
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$3B
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ldi (hl),a
	ldi (hl),a
	ld a,$6C
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$59
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$5C
	ldi (hl),a
	ld a,$58
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$3A
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$6C
	ldi (hl),a
	ld a,$6B
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$54
	ldi (hl),a
	ld a,$47
	ldi (hl),a
	ld hl,Text_NoScrolling
	ld a,46
	ldi (hl),a
	ld a,$6B
	ldi (hl),a
	ld a,$6C
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$5F
	ldi (hl),a
	ld a,$61
	ldi (hl),a
	ld a,$5B
	ldi (hl),a
	ld a,$55
	ldi (hl),a
	ld a,$5E
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$5F
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ldi (hl),a
	ldi (hl),a
	ld a,$53
	ldi (hl),a
	ld a,$5A
	ldi (hl),a
	ld a,$55
	ldi (hl),a
	ld a,$57
	ldi (hl),a
	ld a,$4F
	ldi (hl),a
	ld a,$72
	ldi (hl),a
	ld a,$52
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$61
	ldi (hl),a
	ld a,$5B
	ldi (hl),a
	ld a,$65
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$5E
	ldi (hl),a
	ld a,$33
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ldi (hl),a
	ld a,$6B
	ldi (hl),a
	ldi (hl),a
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$53
	ldi (hl),a
	ld a,$5A
	ldi (hl),a
	ld a,$55
	ldi (hl),a
	ld a,$58
	ldi (hl),a
	ldi (hl),a
	ld a,$5B
	ldi (hl),a
	ld a,$5E
	ldi (hl),a
	ld a,$4F
	ldi (hl),a
	ld a,$5F
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$5B
	ldi (hl),a
	ld a,$40
	ldi (hl),a
	ld hl,Text_Panel
	ld a,34
	ldi (hl),a
	ld a,$67
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$50
	ldi (hl),a
	ld a,$5B
	ldi (hl),a
	ld a,$4F
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$5F
	ldi (hl),a
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$4F
	ldi (hl),a
	ldi (hl),a
	ld a,$4D
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$54
	ldi (hl),a
	ld a,$60
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$53
	ldi (hl),a
	ld a,$5A
	ldi (hl),a
	ld a,$4D
	ldi (hl),a
	ld a,$54
	ldi (hl),a
	ld a,$4F
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$5B
	ldi (hl),a
	ld a,$60
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$33
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$5F
	ldi (hl),a
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$5E
	ldi (hl),a
	ld a,$42
	ldi (hl),a
	ld hl,Text_WrongCode
	ld a,47
	ldi (hl),a
	ld a,$6C
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$59
	ldi (hl),a
	ld a,$55
	ldi (hl),a
	ld a,$60
	ldi (hl),a
	ld a,$65
	ldi (hl),a
	ld a,$5E
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$62
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ldi (hl),a
	ldi (hl),a
	ld a,$67
	ldi (hl),a
	ldi (hl),a
	ldi (hl),a
	ld a,$30
	ldi (hl),a
	ld a,$2C
	ldi (hl),a
	ldi (hl),a
	ld a,$2A
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$65
	ldi (hl),a
	ld a,$4D
	ldi (hl),a
	ld a,$58
	ldi (hl),a
	ld a,$5C
	ldi (hl),a
	ld a,$5F
	ldi (hl),a
	ld a,$55
	ldi (hl),a
	ld a,$50
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ldi (hl),a
	ldi (hl),a
	ldi (hl),a
	ldi (hl),a
	ld a,$60
	ldi (hl),a
	ld a,$5F
	ldi (hl),a
	ld a,$61
	ldi (hl),a
	ld a,$59
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$58
	ldi (hl),a
	ldi (hl),a
	ld a,$4D
	ldi (hl),a
	ld a,$63
	ldi (hl),a
	ld a,$27
	ldi (hl),a
	ld a,$51
	ldi (hl),a
	ld a,$54
	ldi (hl),a
	ld a,$46
	ldi (hl),a
	ret


.ORG $1000
Tiles:
.incbin "sprites.gb"