
FR

	- Nom: Une histoire de bits
	- Description: "il est possible qu'un fichier soit caché dans cette image"
	- Hints: "LSB"
	- Flag: sigsegv{l5b_15_r34lly_c00l}
	- Auteur: jenaye

EN

	- Name: "A history of bits"  
	- Description: "it is possible that a file is hidden in this image"
	- Hint: "LSB"
	- Flag: sigsegv{l5b_15_r34lly_c00l}
	- Author: jenaye


# How to solve 

>easiest way is to clone https://github.com/RobinDavid/LSB-Steganography


```
python LSBSteg.py decode -i Encoded -o flag.txt
```
