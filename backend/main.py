from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI(
    title="Johannesburg Real Estate Digital Twin API"
)


# Frontend running through VS Code Live Server.
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PropertyEnquiry(BaseModel):
    building_name: str
    building_type: str
    building_height: str
    location: str
    enquiry: str


def classify_enquiry(enquiry: str) -> dict:
    """
    Simulated AI enquiry classification.

    This currently uses rule-based keyword matching.
    It can later be replaced with an actual AI model or API.
    """

    enquiry_text = enquiry.lower()

    if any(word in enquiry_text for word in [
        "interested",
        "buy",
        "purchase",
        "looking for",
        "property",
    ]):
        return {
            "intent": "Property Information",
            "lead_type": "Potential Buyer",
            "priority": "Medium",
            "next_action": (
                "Request contact details and provide verified "
                "property information."
            ),
        }

    if any(word in enquiry_text for word in [
        "rent",
        "lease",
        "rental",
    ]):
        return {
            "intent": "Rental Enquiry",
            "lead_type": "Potential Tenant",
            "priority": "Medium",
            "next_action": (
                "Request contact details and verify rental "
                "availability."
            ),
        }

    if any(word in enquiry_text for word in [
        "price",
        "cost",
        "value",
    ]):
        return {
            "intent": "Pricing Enquiry",
            "lead_type": "Potential Buyer",
            "priority": "High",
            "next_action": (
                "Verify current property pricing and contact "
                "the prospective client."
            ),
        }

    return {
        "intent": "General Enquiry",
        "lead_type": "Unclassified Lead",
        "priority": "Low",
        "next_action": (
            "Review the enquiry and determine the appropriate "
            "follow-up action."
        ),
    }


def create_crm_lead(
    data: PropertyEnquiry,
    ai_result: dict,
) -> dict:
    """
    Creates a CRM-ready lead object.

    This does not currently send data to a real CRM.
    """

    return {
        "status": "New",
        "property": data.building_name,
        "location": data.location,
        "enquiry": data.enquiry,
        "intent": ai_result["intent"],
        "lead_type": ai_result["lead_type"],
        "priority": ai_result["priority"],
        "next_action": ai_result["next_action"],
    }


@app.get("/")
async def root():
    return {
        "message": (
            "Johannesburg Real Estate Digital Twin API "
            "is running"
        )
    }


@app.post("/property-enquiry")
async def property_enquiry(data: PropertyEnquiry):

    # Simulated AI classification.
    ai_result = classify_enquiry(
        data.enquiry
    )

    # Create a CRM-ready lead object.
    crm_lead = create_crm_lead(
        data,
        ai_result
    )

    return {
        "status": "processed",

        "property": {
            "building_name": data.building_name,
            "building_type": data.building_type,
            "building_height": data.building_height,
            "location": data.location,
        },

        "enquiry": data.enquiry,

        "ai_processing": {
            "mode": "simulation",
            **ai_result,
        },

        "crm_lead": {
            "mode": "simulation",
            **crm_lead,
        },
    }