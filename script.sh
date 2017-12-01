mkdir test
cp archive.zip test
cp create.sql test
cd test
unzip archive.zip
rm archive.zip
unzip '*.zip'
for f in *.csv; do sed 1d "$f" >tmpfile; mv tmpfile "$f"; done
cat *.csv > sqlite.final
sed -i.bak '1i\
SYMBOL,SERIES,OPEN,HIGH,LOW,CLOSE,LAST,PREVCLOSE,TOTTRDQTY,TOTTRDVAL,TIMESTAMP,TOTALTRADES,ISIN,
' sqlite.final
rm *.csv
rm *.zip
sqlite3 final.sqlite < create.sql