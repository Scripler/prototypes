#!/usr/bin/python
#coding=latin-1

textfile = open('Test.txt', 'w+')

print textfile.name

textfile.write('Det her skal nok blive godt men gad vide hvordan python hÅndterer specialtegn...\n')
textfile.write('Fint! Det kræver bare at man sætter coding=latin-1\n')

textfile.close()