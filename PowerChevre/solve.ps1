$burp = "636869656E76368617436C6F75706C6F75697366861636B9636865767265627265626973673716C697626C696E6461736C727706F776E3706F7765727368656C6C4D6963726F736F6674672616E6456C69737470726F66C6F75766576C696F6E6C696F6E6E657676F746707974686F6E7065726C763B6A617661636F626F6C5636973636F070697A7A6168656C6C3656E66657206861636B6572646973636F726476861636B6174686F6E7656E66616E746368696E6F6973372757373653706F7574696E657472756D705616C66726573636F27368617265706F696E746A65654726F70636861696E36D69676E6F6E736578796736C7572708696E66617578736563696E697469616C69736572E6F6B86E6F6E6F756957069656466368617573737572656C697476368616973652666175746575696C7461626C65373716C36D6F6E676F64626D7973716C46F7261636C6566176696F6E766F697475726536D6F746F073757A756B69626D7776F7264696E6174657572267736D637962657256469676974616C064616D736F76616C6436F72656C73616E0696E6665637465647368656C6C76F75616976170706C656C696E757836172636836D616B697375736869562696572652686F75626C6F6E436F75636F7544C6F7569738526F6952656E6E65346616E6672656C756368653736F636B657463686175737365747465343656C657374696E162726F63616E74656272656269734736F757065C63686F756C657672655626169736572F656D62726173736572646F726D69722626F69726516A65616E6D6F756C696E76861727279D706F74746572"

$babe = "chien;chat;loup;louis;chevre;brebis;sqli;blind;aslr;pown;powershell;Microsoft;rand;list;pro;louve;lionne;lion;got;python;perl;java;cobol;cisco;pizza;enfer;hacker;discord;hackathon;enfant;chinois;russe;poutine;trump;alfresco;sharepoint;jee;ropchain;mignon;sexy;slurp;infauxsec;initialiser;ok;non;pied;chaussure;lit;chaise;fauteuil;table;mongodb;mysql;oracle;avion;voiture;moto;suzuki;bmw;ordinateur;gsm;cyber;digital;damso;vald;orelsan;infected;shell;ouai;apple;linux;arch;maki;sushi;biere;houblon;Coucou;Louis;Roi;Renne;Fanfreluche;socket;chaussette;Celestin;brocante;brebis;soupe;chou;levre;baiser;embrasser;dormir;boire;jean;moulin;harry;potter;ecole;sorcier;hack;sql;hell;oui;c"

$babe = $babe.split(";")
Function en($a)
{
    $b = $a.ToCharArray();
    Foreach ($element in $b) {$c = $c + " " + [System.String]::Format("{0:X}", [System.Convert]::ToUInt32($element))}
    $c
}

foreach($b in $babe)
{
   $hex = en $b
   $hex = $hex.replace(" ", "")
   $burp = $burp.replace($hex, "")
   
}
#On rétablie un caractère
$burp = $burp.replace("40", "4630")
$flag = "$($burp-replace'(..)','[char]0x$1;'|iex)".replace(" ", "")
Write-Host "hex :" $burp "Flag :" $flag
