from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
from typing import List, Dict
import uuid

app = FastAPI()


# ---------- Aika-apufunktio ----------

def now_utc() -> datetime:
    return datetime.now(timezone.utc)


# ---------- Pydantic-mallit ----------

class BookingCreate(BaseModel):
    room_id: str
    start_time: datetime
    end_time: datetime


class Booking(BaseModel):
    id: str
    room_id: str
    start_time: datetime
    end_time: datetime


# ---------- Varauslogiikka ----------

class BookingService:
    def __init__(self):
        # room_id -> list of bookings
        self.bookings: Dict[str, List[Booking]] = {}

    def create_booking(self, booking: BookingCreate) -> Booking:
        if booking.start_time >= booking.end_time:
            raise HTTPException(
                status_code=400,
                detail="Start time must be before end time"
            )

        if booking.start_time < now_utc():
            raise HTTPException(
                status_code=400,
                detail="Booking cannot be in the past"
            )

        room_bookings = self.bookings.get(booking.room_id, [])

        for existing in room_bookings:
            if not (
                booking.end_time <= existing.start_time
                or booking.start_time >= existing.end_time
            ):
                raise HTTPException(
                    status_code=400,
                    detail="Booking overlaps with existing booking"
                )

        new_booking = Booking(
            id=str(uuid.uuid4()),
            room_id=booking.room_id,
            start_time=booking.start_time,
            end_time=booking.end_time,
        )

        room_bookings.append(new_booking)
        self.bookings[booking.room_id] = room_bookings
        return new_booking

    def list_bookings(self, room_id: str) -> List[Booking]:
        return self.bookings.get(room_id, [])

    def delete_booking(self, booking_id: str) -> None:
        for room_bookings in self.bookings.values():
            for booking in room_bookings:
                if booking.id == booking_id:
                    room_bookings.remove(booking)
                    return

        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )


# ---------- Service-instanssi ----------

booking_service = BookingService()


# ---------- API-endpointit ----------

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
