#!/bin/bash

rm -rf ZADATAK
mkdir ZADATAK
cd ZADATAK

indeks=$( dialog --inputbox "Unesite broj indeksa:" 8 35 --output-fd 1 )
clear

wget -q "https://zadatak.singidunum.ac.rs/app/os/ispit/i.php?o=$indeks" -O $indeks.data

cat $indeks.data |      

for tablica in $( cat .tablice ); do
    broj=$( echo $tablica | sed -E 's/^[A-Z]{2}-//; s/-[A-Z]{2}$//' )
    link="https://zadatak.singidunum.ac.rs/app/os/links/$broj.txt"

    wget -q $link -O file$broj
done

ls file$broj | tail > .najvecibroj

cp file234 maxFileSize

cat maxFileSize | grep -E '^[a-z]+.[a-z]+.[0-9]{2,3}@singimail.rs$' | sort -ru > mejlovi.txt

tar -czf "$indeks.tar.gz" ../program.sh maxFileSize mejlovi.txt
