PROMPTI 1

Toteuta yksinkertainen kokoushuoneiden varaus-API Pythonilla FastAPIa käyttäen.

Vaatimukset:
- API:n tulee tukea varauksen luontia, varauksen peruutusta ja huoneen varausten listausta
- Varaukset eivät saa mennä päällekkäin saman huoneen sisällä
- Varaus ei saa olla menneisyydessä
- Aloitusajan täytyy olla ennen lopetusaikaa
- Voidaan käyttää in-memory tietorakennetta (ei tietokantaa)

Tee ratkaisu mahdollisimman yksinkertaisena, jotta se on helppo ajaa lokaalisti.



VASTAUS 1

    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    from datetime import datetime
    from typing import List, Dict
    import uuid

    app = FastAPI()

    # In-memory storage
    bookings: Dict[str, List[dict]] = {}


    class BookingCreate(BaseModel):
        room_id: str
        start_time: datetime
        end_time: datetime


    class Booking(BaseModel):
        id: str
        room_id: str
        start_time: datetime
        end_time: datetime


    "app.post("/bookings", response_model=Booking)
    def create_booking(booking: BookingCreate):
    if booking.start_time >= booking.end_time:
        raise HTTPException(status_code=400, detail="Start time must be before end time")

    if booking.start_time < datetime.now():
        raise HTTPException(status_code=400, detail="Booking cannot be in the past")

    room_bookings = bookings.get(booking.room_id, [])

    for existing in room_bookings:
        if not (
            booking.end_time <= existing["start_time"]
            or booking.start_time >= existing["end_time"]
        ):
            raise HTTPException(status_code=400, detail="Booking overlaps with existing booking")

    booking_id = str(uuid.uuid4())
    new_booking = {
        "id": booking_id,
        "room_id": booking.room_id,
        "start_time": booking.start_time,
        "end_time": booking.end_time,
    }

    room_bookings.append(new_booking)
    bookings[booking.room_id] = room_bookings

    return new_booking


    @app.get("/rooms/{room_id}/bookings", response_model=List[Booking])
    def list_bookings(room_id: str):
        return bookings.get(room_id, [])


    @app.delete("/bookings/{booking_id}")
    def delete_booking(booking_id: str):
        for room_id, room_bookings in bookings.items():
            for booking in room_bookings:
                if booking["id"] == booking_id:
                    room_bookings.remove(booking)
                    return {"message": "Booking deleted"}
        raise HTTPException(status_code=404, detail="Booking not found")


PROMPTI 2

Kokeilin antamaasi ratkaisua, mutta sain tulosteeksi virheen "can't compare offset-naive and offset-aware datetimes". Korjaa datetime-osio toimivaksi.

VASTAUS 2

Nopein ja järkevin fix

Tee aikavertailu timezone-aware-muodossa:

    from datetime import datetime, timezone

ja muuta vertailu:

    if booking.start_time < datetime.now(timezone.utc):
    raise HTTPException(status_code=400, detail="Booking cannot be in the past")

Tämä toimii, koska:

Pydantic käyttää ISO 8601 -aikoja

ne ovat yleensä UTC-offsetilla varustettuja




PROMPTI 3

Refaktoroi varauslogiikka omaksi luokaksi.


VASTAUS 3 


    class BookingService:
        def __init__(self):
            self.bookings: Dict[str, List[dict]] = {}
    
        def create_booking(self, booking: BookingCreate) -> dict:
            if booking.start_time >= booking.end_time:
                raise HTTPException(status_code=400, detail="Start time must be before end time")
    
            if booking.start_time < now_utc():
                raise HTTPException(status_code=400, detail="Booking cannot be in the past")
    
            room_bookings = self.bookings.get(booking.room_id, [])
    
            for existing in room_bookings:
                if not (
                    booking.end_time <= existing["start_time"]
                    or booking.start_time >= existing["end_time"]
                ):
                    raise HTTPException(status_code=400, detail="Booking overlaps with existing booking")
    
            new_booking = {
                "id": str(uuid.uuid4()),
                "room_id": booking.room_id,
                "start_time": booking.start_time,
                "end_time": booking.end_time,
            }
    
            room_bookings.append(new_booking)
            self.bookings[booking.room_id] = room_bookings
            return new_booking
    
        def list_bookings(self, room_id: str) -> List[dict]:
            return self.bookings.get(room_id, [])
    
        def delete_booking(self, booking_id: str) -> None:
            for room_bookings in self.bookings.values():
                for booking in room_bookings:
                    if booking["id"] == booking_id:
                        room_bookings.remove(booking)
                        return
            raise HTTPException(status_code=404, detail="Booking not found")

Instanssi serviceä varten

Ylös tiedostoon:

    booking_service = BookingService()


Siivoa endpointit

Korvaa endpointit näin:

    @app.post("/bookings", response_model=Booking)
    def create_booking(booking: BookingCreate):
        return booking_service.create_booking(booking)


    @app.get("/rooms/{room_id}/bookings", response_model=List[Booking])
    def list_bookings(room_id: str):
        return booking_service.list_bookings(room_id)


    @app.delete("/bookings/{booking_id}")
    def delete_booking(booking_id: str):
        booking_service.delete_booking(booking_id)
        return {"message": "Booking deleted"}


Endpointit ovat nyt ohuita ja luettavia.
