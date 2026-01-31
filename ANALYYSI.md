1. MITÄ TEKOÄLY TEKI HYVIN?

Tekoäly tuotti nopeasti ja suhteellisen helposti toimivan perusratkaisun, joka täytti tehtävän keskeisimmät vaatimukset. Tuotettu rajapinta sisälsi kaikki vaaditut toiminnot (varauksen luonti, poisto ja listaus) ja perusliiketoimintasäännöt kuten päällekkäisten varausten estäminen oli huomioitu.
Pyysin tekoälyä heti alussa käyttämään Python ja FastAPI komboa, jonka avulla ratkaisua lähdettiin rakentamaan. Olen aikaisemmin törmännyt tilanteeseen, missä auttava tekoälymalli on yhtäkkiä vaihtanut ohjelmointikieltä kesken projektin, mikä ei tietenkään ole toimiva ratkaisu.

3. MITÄ TEKOÄLY TEKI HUONOSTI?

Tekoälyn tuottamassa koodissa oli useita ongelmia, mitkä eivät näkynyt päälle päin pelkästään koodia lukemalla.
- Aikavyöhykkeiden käsittely oli toteutettu huonosti, mikä johti siihen, että varausjärjestelmä ei toiminut lainkaan.
- Liiketoimintalogiikka ja HTTP-rajapinta olivat kytkeytyneet toisiinsa.
- Dataa käsiteltiin suoraan globaalisti ilman minkäänlaista kapselointia.
- Syötevalidointi ja liiketoimintasäännöt olivat sekoittuneet.
- Virheenkäsittely oli epätarkkaa ja HTTP-statuskoodit olivat "laiskasti" toteutettu, kaikki käyttivät samaa virhekoodia.

5. MITKÄ OLIVAT TÄRKEIMMÄT PARANNUKSET, JOTKA TEIT TEKOÄLYN TUOTTAMAAN KOODDIN JA MIKSI?

- Kaikkien aikamuuttujien vaihtaminen UTC:hen poisti kriittiset ajonaikaiset virheet ja teki järjestelmän käyttämisestä yleisesti sujuvampaa. Tarvittaessa tätä toiminnallisuutta pystyy myös muokkaamaan tulevaisuudessa tiettyyn aikavyöhykkeeseen tarpeen mukaan.
- Varauslogiikan eriyttäminen omaksi luokaksi (BookingService) paransi yleisesti koodin luettavuutta ja ylläpitämistä. Se myös helpotti toiminnallisuuksien testaamisessa huomattavasti.
- Syötevalidoinnin siirtäminen Pydanticille ja virheviestien tarkentaminen teki koodista siistimpää ja käyttäjäystävällisempää. On kätevää, kun virheilmoitukset oikeasti kertovat, missä virhe tapahtui.

Yleisesti, tekemäni refaktorointi ja parantelu teki tekoälyn tuottamasta raakaversiosta selkeämmän sekä paremmin ylläpidettävän ja muokattavan kokonaisuuden.
