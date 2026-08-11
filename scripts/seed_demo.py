#!/usr/bin/env python3
"""Seed TourSafe dev environment with demo data."""
import asyncio
import os
from datetime import datetime, timedelta, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import GEOSPHERE

MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/toursafe")


def make_point(lat: float, lng: float):
    return {"type": "Point", "coordinates": [lng, lat]}


async def seed():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client["toursafe"]

    await db.travelers.delete_many({})
    await db.trips.delete_many({})
    await db.geo_fences.delete_many({})
    await db.emergency_resources.delete_many({})
    await db.agencies.delete_many({})

    traveler = {
        "did": "did:polygon:0xDemoTraveler",
        "wallet_address": "0xDemoTraveler",
        "public_key_hash": "0x" + "00" * 32,
        "name": "Arun Kumar",
        "email": "arun.demo@example.com",
        "phone": "+91-9876543210",
        "date_of_birth": "1995-03-15",
        "home_country": "India",
        "nationality": "Indian",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
        "is_active": True,
    }
    traveler_result = await db.travelers.insert_one(traveler)
    traveler_id = traveler_result.inserted_id

    trip = {
        "traveler_id": traveler_id,
        "name": "Kodaikanal Trek",
        "destination": "Kodaikanal, Tamil Nadu",
        "destination_geo": {"lat": 10.2381, "lng": 77.4892},
        "start_date": datetime.now(timezone.utc),
        "end_date": datetime.now(timezone.utc) + timedelta(days=3),
        "status": "ACTIVE",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }
    await db.trips.insert_one(trip)

    fences = [
        {
            "fence_id": "fence-demo-cliff",
            "name": "Demo Cliff Edge",
            "type": "HAZARD",
            "severity": "HIGH",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [77.485, 10.235],
                        [77.490, 10.235],
                        [77.490, 10.240],
                        [77.485, 10.240],
                        [77.485, 10.235],
                    ]
                ],
            },
            "dwell_threshold_minutes": 10,
            "jurisdiction": "Tamil Nadu",
            "active": True,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
    ]
    await db.geo_fences.insert_many(fences)

    resources = [
        {
            "resource_id": "res-police-001",
            "type": "POLICE",
            "name": "Kodaikanal Police Station",
            "lat": 10.2390,
            "lng": 77.4880,
            "address": "Kodaikanal",
            "phone": "+91-4542-...",
            "api_endpoint": "http://localhost:9001/api/fir",
            "jurisdiction": "Tamil Nadu",
            "active": True,
        },
        {
            "resource_id": "res-hospital-001",
            "type": "HOSPITAL",
            "name": "Kodaikanal Government Hospital",
            "lat": 10.2360,
            "lng": 77.4920,
            "address": "Kodaikanal",
            "phone": "+91-4542-...",
            "api_endpoint": "http://localhost:9002/api/emergency",
            "jurisdiction": "Tamil Nadu",
            "active": True,
        },
    ]
    await db.emergency_resources.insert_many(resources)
    await db.emergency_resources.create_index([("location", GEOSPHERE)])

    agencies = [
        {
            "agency_id": "agency-police-tn",
            "name": "Tamil Nadu Police",
            "type": "POLICE",
            "wallet_address": "0xDemoAgencyPolice",
            "emergency_access_key": "<encrypted>",
            "jurisdiction": "Tamil Nadu",
            "active": True,
            "created_at": datetime.now(timezone.utc),
        }
    ]
    await db.agencies.insert_many(agencies)

    print("Demo data seeded successfully.")
    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
