#!/usr/bin/python
#coding=latin-1

textfile = open('Test.txt', 'w+')

print textfile.name

textfile.write('Det her skal nok blive godt men gad vide hvordan python h�ndterer specialtegn...\n')
textfile.write('Fint! Det kr�ver bare at man s�tter coding=latin-1\n')

textfile.close()