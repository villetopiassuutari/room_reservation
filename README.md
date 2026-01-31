**Kokoushuoneiden varausrajapinta**

- Kaikki ajat käsitellään UTC-aikavyöhykkeessä.
- Yksi varaus koskee aina yhtä huonetta.
- Käyttäjätunnistusta tai autentikointia ei ole mukana.
- In-memory tallennus tyhjentyy sovelluksen uudelleenkäynnistyksen yhteydessä.
- Varausten päällekkäisyys tarkistetaan huonekohtaisesti.


**Ajaminen ja testaaminen paikallisesti:**

Lataa ensin arvittavat kirjastot komennolla

    pip install fastapi uvicorn

Siirry työskentelykansioon ja käynnistä sitten komennolla

    python varaus.py


**Mene selaimella osoitteeseen:**

    http://127.0.0.1:8000/docs
