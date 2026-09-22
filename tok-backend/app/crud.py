from typing import Optional, Any
from sqlalchemy.orm import Session
from app import models

def get_or_create_vendor(
    db: Session, 
    phone_number: str, 
    name: Optional[str] = "Demo Vendor"
) -> models.Vendor:
    """
    Checks if a vendor exists by phone number. 
    If not, creates and returns a new vendor record.
    """
    vendor = db.query(models.Vendor).filter(models.Vendor.phone_number == phone_number).first()
    if not vendor:
        vendor = models.Vendor(phone_number=phone_number, name=name)
        db.add(vendor)
        db.commit()
        db.refresh(vendor)
    return vendor

def create_vendor_listing(
    db: Session, 
    vendor_id: Any, 
    item_name: str, 
    price: float, 
    raw_transcript: str
) -> models.Listing:
    """
    Saves extracted voice note data directly into the listings table.
    """
    db_listing = models.Listing(
        vendor_id=vendor_id,
        item_name=item_name,
        price=price,
        raw_transcript=raw_transcript,
        is_available=True
    )
    db.add(db_listing)
    db.commit()
    db.refresh(db_listing)
    return db_listing