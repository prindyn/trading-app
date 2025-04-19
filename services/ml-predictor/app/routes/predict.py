from fastapi import APIRouter, HTTPException
from app.database.schemas import PredictionRequest, PredictionResponse
from app.services.feature_engineer import extract_features
from app.models.predictor import model

router = APIRouter()


@router.post("/", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        features = extract_features(request.candles)
        proba = model.predict_proba(features)[0]
        label = model.predict(features)[0]

        return PredictionResponse(
            expected_gain=round(float(proba[1] * 5.0), 2),
            confidence=round(float(proba[1] * 100), 2),
            direction="long" if label == 1 else "short",
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {e}")
