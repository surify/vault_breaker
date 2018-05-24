This program decrypts image, audio, video, pdf files encrypted by vault by bruteforcing the key and replacing the
encrypted contents of the file with original contents.

HOW DOES THE PROGRAM DECRYPTS:

this program reads the binary file encrypted by vault and finds which key is used to encrypt(ROFL) it by bruteforcing all 256 possible keys.
then it replaces the encrypted content with original content by XOR ing the first 256 characters(128 hex digits)
of the binary content of the encrypted file with key and saves it with the file's original extension.

GUIDELINES:
1) Run the script
2) put all the encrypted files(.bin files) in a folder and enter its path when prompted
3) give a valid separate folder to store decrypted files
4) uncomment code at line 223 if you want to delete encrypted files after successful decryption