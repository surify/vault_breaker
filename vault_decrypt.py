#!/usr/bin/python3


"""
AUTHOR: P SURYA TEJA
LAST MODIFIED(DD-MM-YYYY): 17-01-2018

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
"""


from binascii import hexlify, unhexlify
import os


def extractName(file_name):
    """this function takes a filename with extension and
    returns the filename after removing the extension.

    For example it takes 'earth.jpg' and returns 'earth'

    this function first reverses the file name, removes the extension,
    and then reverses it again.

    I decided to do the extraction of filename this way because, even if
    in future vault app names their encrypted files like
    filename.bin(i.e. retaining the original filename for encrypted files
    rather than using a random name like 2345334333.bin and the original
    filename contains '.', the function works as expected).

    """
    return file_name[::-1].split('.', 1)[1][::-1]


def isBinary(filename):
    """this function takes a filename and checks whether it is a file
    and ends with '.bin' and returns True if both conditions pass.
    """
    return True if (os.path.isfile(filename) and
                    filename.endswith('.bin')) else False


def main():
    # THESE STRINGS WILL BE APPENDED TO THE RESPECTIVE DECRYPTED FILES
    image_type = 'image_'
    video_type = 'video_'
    audio_type = 'audio_'
    pdf_type = 'pdf_'

    while True:
        source_dir = input("enter the folder path where encrypted files are stored: ")
        if os.path.exists(source_dir):
            break
        else:
            print("Error: Invalid path or Permission denied.\n")

    # CHANGING THE PATH TO THE source_dir DIRECTORY
    os.chdir(source_dir)

    # AFTER DECRYPTING, FILES ARE STORED IN 'destination_dir'
    destination_dir = input("enter directory path to store decrypted files: ")

    # IF THE 'destination_dir' DOESN'T EXIST, THE PROGRAM CREATES IT.
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # ALL FILE NAMES IN THE 'encrypted' DIRECTORY ARE STORED IN 'all_files'
    all_files = os.listdir()
    no_of_files = len(all_files)
    print("TRAVERSING ALL FILES IN THE FOLDER....\n")

    # IF THERE ARE NO FILES IN THE 'encrypted' DIRECTORY, THE PROGRAM EXITS
    if os.listdir() == []:
        print("NO FILES IN THE 'ENCRYPTED' FOLDER. \nEXITING THE PROGRAM....")
        exit()

    # THE FILETYPE IS DETERMINED IN THE FOLLOWING 'for' LOOP
    for i in range(no_of_files):
        # IF THE FILE IS NOT A BINARY FILE, WE NEED NOT DECRYPT IT
        if not isBinary(all_files[i]):
            continue
        file = open(all_files[i], 'rb')

        # READING THE CONTENT OF THE BINARY FILE
        bin_content = file.read()
        file.close()

        # CONVERTING THE BINARY CONTENT TO 'str'
        str_content = hexlify(bin_content).decode('utf-8')

        # 'one, two AND three' ARE FIRST THREE HEXADECIMAL BITS OF THE FILE TO DETERMINE THE FILE TYPE AND KEY
        one = int(str_content[0:2], 16)
        two = int(str_content[2:4], 16)
        three = int(str_content[4:6], 16)
        four = int(str_content[6:8], 16)
        nine = int(str_content[16:18], 16)
        ten = int(str_content[18:20], 16)
        eleven = int(str_content[20:22], 16)
        twelve = int(str_content[22:24], 16)
        print('BRUTEFORCING BEGINS....: {}'.format(all_files[i]))
        key = 0

        # 'file_type' IS THE TYPE OF THE FILE.(.JPG, .PNG, .MP4, etc.,)
        file_type = ''
        while key <= 255:
            # COMBINATION OF FIRST 3 HEX DIGITS WHICH INDICATE THE IMAGE TYPE
            first_three = (hex(one ^ key)[2:] +
                           hex(two ^ key)[2:] +
                           hex(three ^ key)[2:])

            # 9, 10 AND 11 HEX DIGITS ARE REQUIRED TO DETERMINE MP4 AND 3GP
            nine_ten_eleven = (hex(nine ^ key)[2:] +
                               hex(ten ^ key)[2:] +
                               hex(eleven ^ key)[2:]).upper()

            # IF IT IS '.jpg'
            if first_three == "ffd8ff":
                file_type = '.jpg'
                break

            # IF IT IS '.png'
            elif first_three == '89504e':
                file_type = '.png'
                break

            # IF IT IS '.gif'
            elif first_three == '474946':
                file_type = '.gif'
                break

            # IF IT IS '.tif'
            elif first_three in ['49492A', '4D4D0']:
                file_type = '.tif'
                break

            # IF IT IS '.webp' IMAGE
            # 57454250 IN HEX REPRESENTS WEBP IN ASCII
            elif nine_ten_eleven + hex(twelve ^ key)[2:].upper() == '57454250':
                file_type = '.webp'
                break

            # IF IT IS MP4
            elif nine_ten_eleven in ['6D7034', '69736F']:
                file_type = '.mp4'
                break

            # IF IT IS 3GP
            elif nine_ten_eleven == '336770':
                file_type = '.3gp'
                break

            # THE BELOW CODE IS COMMENTED BECAUSE VAULT APP DOESN'T OFFER TO HIDE MP3 AND PDF FILES

            # IF IT IS '.mp3'
            # elif first_three == '494433':
            #   file_type = '.mp3'
            #   break
            # IF IT IS '.pdf' AS FIRST FOUR CHARACTERS ARE '%PDF'
            # elif first_three + hex(four ^ key)[2:] = '25504446':
            #       file_type = '.pdf'
            #       break
            # IF NO FORMAT MATCHES MAY BE KEY IS WRONG, SO WE INCREMENT THE KEY
            else:
                key += 1

        # INITIALLY file_type IS EMPTY. IF IT IS NOT EMPTY NOW,
        # IT MEANS IT MATCHED SOME FORMAT.
        if file_type is not '':
            print('KEY FOUND: {}'.format(key))

        # IF NO FORMAT HAS MATCHED, THEN THE FILE TYPE MAY BE
        # SOME OTHER FORMAT WE HAVEN'T ADDED.
        else:
            print('FAILURE for {}.\n'.format(all_files[i]))
            continue
        print("DECRYPTION BEGINS....")

        # REPLACING THE FIRST 256 CHARACTERS(128 HEXADECIMAL BITS) OF THE FILE WITH ORIGINAL FILE CONTENTS
        # AS THE REMAINING LINES ARE UNCHANGED BY THE VAULT APP
        # 'replacement' is the content to be replaced at the
        replacement = []

        # 'first' CONTAINS THE ENCRYPTED CONTENT THAT NEED TO BE DECRYPTED.
        first = str_content[:256]

        # 'last' CONTAINS THE UNENCRYPTED CONTENT THAT HAVE TO BE COPIES AS IS.
        last = str_content[256:]
        j = 0

        # THE BELOW 'while' LOOP DECRYPTS THE CONTENT AND APPENDS IT TO THE 'replacement' LIST.
        # WE ARE PERFORMING THE DECODING ON FIRST 256 BITS ONLY AS THE REMAINING ARE UNCHANGED
        # BY THE VAULT APP.
        while j < 256:
            data = hex(int(first[j : j + 2], 16) ^ key)[2:4]
            # IF THE data IS SINGLE DIGIT LIKE 0 OR 2 OR 5 OR A OR C
            # WE HAVE TO APPEND IT IN THE FILE AS 00 OR 02 OR 0A etc.,
            if len(data) == 1:
                data = '0'+ data
            replacement.append(data)
            j += 2

        # ORIGINAL CONTENT IS FORMED
        original_content = ''.join(replacement) + last
        print('WRITING THE ORIGINAL CONTENT TO THE FILE')
        new_file_name = extractName(all_files[i]) + file_type
        with open(os.path.join(destination_dir, new_file_name), 'wb') as file:
            file.write(unhexlify(original_content.encode('utf-8')))

        # DELETING THE ENCRYPTED FILE AFTER SUCCESSFUL DECRYPTION
        # os.remove(all_files[i])
        print("FILE {} DECRYPTED\n".format(all_files[i]))


if __name__ == '__main__':
    main()
