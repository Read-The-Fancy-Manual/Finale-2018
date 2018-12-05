# Solution for securecorp

## Step 1: breaking the keyboard

 * Keys are randomized, so you need to get the keyboard layout
 * Access code is fixed-length, shorter or longer ones won't work
 * Access code is checked digit by digit, which takes time => time attack

## Step 2: finding the hidden room

 * There are 3 rooms, only two with readable label
 * These labels base64_decode to numbers between 1 and 100
 * Testing all labels between 1 and 100 will get you the "DEBUG" room

## Step 3: getting the admin token

 * Using the DEBUG room, you can see what your token decodes into when there is an error
 * Using this, you can use AES bitflipping to make yourself an admin token
